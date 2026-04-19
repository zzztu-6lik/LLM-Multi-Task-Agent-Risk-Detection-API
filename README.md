# LLM Multi-Task Agent & Risk Detection API
# 大模型智能体与黑话检测综合项目

本项目包含两个核心模块：基于 ReAct 架构的**多功能旅行/航班推荐智能体**，以及基于 FastAPI 和大模型（Ollama/DeepSeek）构建的**反欺诈黑话与风险检测接口**。

## 📁 项目结构

本项目主要包含以下三个核心脚本：

* **`test1.3.py`**：基础版本的 ReAct 智能体。能够自主规划思考，调用 `wttr.in` 查询天气，以及使用 `Tavily Search API` 搜索景点推荐。
* **`test1.3_m.py`**：进阶版本的 ReAct 智能体。在基础版本上增加了航班查询功能，集成了 `Aviationstack API`，可实现天气查询、航班检索与景点推荐的连贯多步推理。
* **`black_slang_multi_task.py`**：基于 FastAPI 构建的后端接口服务。结合了本地微调分类模型与 Ollama 大模型（deepseek-r1:14b），用于检测对话中的诈骗风险、情绪标签及特定黑话词汇。

## 🚀 核心特性

1.  **ReAct Agent 架构**：纯手工实现的大脑（Thought）与手脚（Action）闭环机制，不依赖臃肿框架，极其适合学习大模型底层工作原理。
2.  **多工具动态调用**：Agent 可根据自然语言指令，自主决定调用天气、航班或搜索引擎工具。
3.  **多任务 NLP 流水线**：`black_slang_multi_task.py` 整合了情感分析、风险定级、意图分类等多项 NLP 任务，提供统一的 API 输出。

## 🛠️ 安装与配置

### 1. 安装依赖

请确保您的环境中安装了以下 Python 库：
```bash
pip install requests tavily-python openai fastapi uvicorn pydantic langchain_ollama# LLM-Multi-Task-Agent-Risk-Detection-API

### 2.环境变量与 API Key 配置
运行智能体脚本（test1.3.py / test1.3_m.py）前，需配置以下服务凭证：

LLM API Key: 兼容 OpenAI 格式的接口（代码中默认使用 yibuapi.com）。

Tavily API Key: 用于搜索引擎工具。

Aviationstack API Key: 用于航班查询工具。

3. 本地模型路径（针对黑话检测接口）
在运行 black_slang_multi_task.py 前，请务必修改代码中的本地模型路径，确保指向您本地实际的目录：

base_two_path 与 base_d_path

数据集路径 dataset_path

Ollama 服务地址（默认配置为 http://localhost:8080）

💻 启动指南
运行旅行智能体：

Bash
python test1.3_m.py

启动黑话检测 FastAPI 服务：

Bash
python black_slang_multi_task.py
# 或使用 uvicorn 启动:
uvicorn black_slang_multi_task:app --host 0.0.0.0 --port 3306

启动后，可通过发送 POST 请求至 http://127.0.0.1:3306/main 进行测试。

⚠️ 注意事项
代码中的 API Key 仅为测试使用。出于安全考虑，强烈建议在实际部署或对外开源时，使用 .env 文件或系统环境变量来管理密钥，切勿将真实秘钥硬编码在代码中。

---

### 📤 新手指南：如何把代码上传到 GitHub？

既然你是第一次上传，我推荐你使用最简单、直观的**网页端上传法**（不需要敲命令行）：

1.  **注册/登录 GitHub**：打开 [GitHub 官网](https://github.com/) 并登录你的账号。
2.  **创建新仓库 (Create a new repository)**：
    * 点击右上角的 `+` 号，选择 **New repository**。
    * **Repository name**：给你的项目起个名字（比如 `LLM-Agent-and-Risk-Detection`）。
    * **Description**：简单写一句话介绍。
    * **Public / Private**：选择公开（别人能看到）还是私有（只有你能看到）。
    * 直接点击最下方的绿色按钮 **Create repository**。
3.  **上传文件**：
    * 在新建成功的页面上，你会看到一个链接：`uploading an existing file`（上传现有文件），点击它。
    * 把你的那 3 个 `.py` 文件，加上刚才保存的 `README.md` 文件，一起拖拽到网页框里。
4.  **提交更改 (Commit changes)**：
    * 文件上传完毕后，在页面下方绿色的 **Commit changes** 按钮处点击。
    * 恭喜！你的代码已经成功托管在 GitHub 上了，README 也会自动展示在项目首页！
