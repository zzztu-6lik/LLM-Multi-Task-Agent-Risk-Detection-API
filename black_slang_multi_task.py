import json
import os
from fastapi import FastAPI, HTTPException
from langchain_ollama import OllamaLLM
from pydantic import BaseModel
from detect_label.test2detect_label import DetectLabelModel
from detect_category.test2detect_category import DetectCategoryModel
from detect_emotion.detect_emotion import generate_emotion_indicators_from_dialogue,get_emotion_tag_kind
from detect_risk.detect_risk import generate_risk_indicators_from_dialogue,get_judgment_kind
from detect_interpretable_tasks.detect_interpretable_tasks import generate_black_terms_indicators_from_dialogue,get_all_black_terms

app=FastAPI(
    title='黑话接口',
    description='通过对话内容调用黑话检测的模型',
    version='1.0'
)

class FrontendParams(BaseModel):
    dialogue_str: str

class BlackTermsDetectPipeline:

    def __init__(self,base_model_path, model_2_dict_path, tokenizer_2_path, lora_2_weight_path, model_d_dict_path, tokenizer_d_path, lora_d_weight_path,datas,device_index=0):
        print("正在初始化本地检测与分类模型...")
        self.label_detect = DetectLabelModel(base_model_path, model_2_dict_path, tokenizer_2_path,
                                   lora_2_weight_path, 0)

        self.category_detect = DetectCategoryModel(base_model_path,model_d_dict_path,tokenizer_d_path,lora_d_weight_path,0)

        print("正在初始化大语言模型 (Ollama)...")
        self.llm = OllamaLLM(base_url='http://localhost:8080', model='deepseek-r1:14b', temperature=0.6)

        self.data_dialogue = [data["dialogue"] for data in datas]
        self.risk_list = ["high","medium_high","low_or_contextual"]
        self.judgment_list = get_judgment_kind(datas)
        self.emotion_tag_list = get_emotion_tag_kind(datas)
        self.black_terms_list =get_all_black_terms(datas)

    def analyze_dialogue(self, datas):
        """核心调用函数：传入一段对话，输出所有任务的综合分析结果"""

        result_list=[]
        label2category = {
            1: "loan_fraud",
            2: "money_mule_laundering",
            3: "refund_or_impersonation_fraud",
            4: "gambling_slang",
            5: "romance_investment_fraud",
            6: "brushing_fraud",
            7: "legal_or_compliance_consultation",
            8: "anti_fraud_education",
            9: "normal_finance_or_service",
            10: "daily_life_hard_negative",
            11: "research_or_annotation_discussion",
            0: "news_or_case_discussion"
        }

        for data in datas:
            dialogue_str = data['dialogue']
            predict_label_tuple = self.label_detect.predict(dialogue_str)

            predict_label = int(predict_label_tuple[0])
            print('predict_label:')
            print(predict_label)
            if predict_label == 1:
                predict_label_str = "suspicious"
            else:
                predict_label_str = "normal"

            raw_category_id = self.category_detect.predict(dialogue_str)
            predict_category = label2category.get(int(raw_category_id), "unknown_category")

            result_a =generate_risk_indicators_from_dialogue(self.llm,[dialogue_str],self.risk_list,self.judgment_list,temperature=0.6)
            print('result_a')
            print(result_a)
            answer_a = result_a[0]
            _, judgment_list, risk_level, suspicion_score = (
                answer_a["dialogue"],
                answer_a["judgment"],
                answer_a["risk_level"],
                answer_a["suspicion_score"]
            )

            result_b = generate_emotion_indicators_from_dialogue(self.llm,[dialogue_str],self.emotion_tag_list)
            print('result_b')
            print(result_b)
            answer_b = result_b[0]
            _, emotion_tag, sentiment_score, arousal_score = (
                answer_b["dialogue"],
                answer_b["emotion_tag"],
                answer_b["sentiment_score"],
                answer_b["arousal_score"]
            )

            result_c = generate_black_terms_indicators_from_dialogue(self.llm,[dialogue_str],self.black_terms_list)
            print('result_c')
            print(result_c)
            answer_c = result_c[0]
            _, black_terms, rationale = (
                answer_c["dialogue"],
                answer_c["black_terms"],
                answer_c["rationale"],
            )
            if black_terms :
                has_black_terms = 1
            else:
                has_black_terms = 0
            group ={
                "label":predict_label_str,
                "detect_label":predict_label,
                "category":predict_category,
                "risk_level":risk_level,
                "emotion_tag":emotion_tag,
                "sentiment_score":sentiment_score,
                "arousal_score":arousal_score,
                "suspicion_score":suspicion_score,
                "has_black_terms":has_black_terms,
                "black_terms":black_terms,
                "dialogue":dialogue_str,
                "judgment":judgment_list,
                "rationale":rationale

            }
            result_list.append(group)

        return result_list

@app.post('/main',summary='黑话检测（前端调用）')
def main(params:FrontendParams):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_model_path = os.path.join(str(current_dir)[:str(current_dir).find("dmj") + 3],
                                   "models_id")
    dataset_path = os.path.join(str(current_dir)[:str(current_dir).rfind("SF") + 2],
                                "dataset")
    datas = []
    with open(dataset_path, 'r', encoding='utf-8') as f:
        datas.extend(json.load(f))

    # 1.二分类的模型参数地址
    base_two_path = "..."
    output_dir = os.path.join(base_two_path, "model_dict")

    last_model_2_dict_path = os.path.join(output_dir, "last_model_dict/model_dict.bin")
    last_model_2_tokenizer_path = os.path.join(output_dir, "last_model_tokenizer")
    last_model_2_lora_path = os.path.join(output_dir, "last_model_lora")

    # 2.多分类的模型参数地址
    base_d_path = "..."
    output_dir = os.path.join(base_d_path, "model_dict")

    last_model_d_dict_path = os.path.join(output_dir, "last_model_dict/model_dict.bin")
    last_model_d_tokenizer_path = os.path.join(output_dir, "last_model_tokenizer")
    last_model_d_lora_path = os.path.join(output_dir, "last_model_lora")

    detect_way = BlackTermsDetectPipeline(base_model_path, last_model_2_dict_path, last_model_2_tokenizer_path,
                                          last_model_2_lora_path,
                                          last_model_d_dict_path, last_model_d_tokenizer_path, last_model_d_lora_path,
                                          datas)
    dialogue_str = params.dialogue_str
    dia_str = detect_way.analyze_dialogue([{"dialogue": dialogue_str}])
    return {
                "label":dia_str[0]["label"],
                "detect_label":dia_str[0]["detect_label"],
                "category":dia_str[0]["category"],
                "risk_level":dia_str[0]["risk_level"],
                "emotion_tag":dia_str[0]["emotion_tag"],
                "sentiment_score":dia_str[0]["sentiment_score"],
                "arousal_score":dia_str[0]["arousal_score"],
                "suspicion_score":dia_str[0]["suspicion_score"],
                "has_black_terms":dia_str[0]["has_black_terms"],
                "black_terms":dia_str[0]["black_terms"],
                "dialogue":dia_str[0]["dialogue"],
                "judgment":dia_str[0]["judgment"],
                "rationale":dia_str[0]["rationale"]

    }


if __name__ == '__main__':


    import uvicorn

    uvicorn.run(app="black_slang_multi_task:app", host="0.0.0.0", port=3306)
