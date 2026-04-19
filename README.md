# Industry Slang & Risk Detection API

本项目是一个应用于风控场景的综合性对话与行业黑话检测后端服务。系统融合了本地微调的分类模型与本地部署的大语言模型（基于 Ollama 的 DeepSeek-R1），能够对输入的对话文本进行多维度分析。

## 核心功能
本项目通过 Pipeline 实现了以下多任务检测：
* **二分类与多分类检测**：识别对话是否存在异常风险，并将其归类至具体的诈骗或违规类别（如刷单诈骗、杀猪盘等）。
* **风险等级评估**：结合 LLM 提取风险指标，输出风险等级与嫌疑分数。
* **情感与唤醒度分析**：提取对话中的情感标签，并计算情感极性与唤醒度得分。
* **行业黑话提取**：精准识别对话中的“行业黑话”，并提供可解释性的原理解析。

## 技术栈
* **Web 框架**: FastAPI, Uvicorn
* **大模型框架**: LangChain, Ollama
* **模型**: 本地深度学习模型 + `deepseek-r1:14b`

## 部署与配置
1. **环境依赖**: `pip install fastapi uvicorn pydantic langchain_ollama`（需确保本地已安装引用的 detect 相关模块）。
2. **启动 Ollama 服务**：确保本地或服务器的 `8080` 端口运行着 Ollama，且已拉取对应模型。
3. **配置本地模型路径**：请确保代码中 `main` 函数下的各类模型权重路径（如 LoRA 权重、数据集路径）与你的本地实际文件目录一致。

## 启动服务
使用 Uvicorn 启动 FastAPI 接口：
`python black_slang_multi_task.py`
服务默认运行在 `http://0.0.0.0:3306`

## 接口说明
服务启动后，在浏览器中访问 `http://localhost:3306/docs` 即可查看 Swagger UI 接口文档并进行在线测试。
**API Endpoint**: `POST /main`






