# 🏥 AI Health Assistant
## *files & dir not uploaded due to updating some more features*
An **Agentic RAG-powered medical reasoning assistant** fine-tuned on clinical data to analyze medical reports, detect diseases from symptoms & report data, and provide **advisory recommendations** with **human-in-the-loop validation**.

Built using **LangGraph**, **ChromaDB**, **HuggingFace Transformers**, **Unsloth QLoRA**, and a **Streamlit + FastAPI UI**.  
Containerized with **Docker** for cross-platform reproducibility.

---

<div style="display: flex; align-items: flex-start;">
  
  <!-- Left side image -->
  <div style="flex: 1; text-align: left;">
    <h3>Workflow Chart</h3>
    <img src="https://github.com/user-attachments/assets/c7429d88-4273-4f73-8160-932050cb6d59" alt="LangGraph Workflow" width="100%" /> 
  </div>

  <!-- Right side stacked images -->
  <div style="flex: 1; text-align: right;">
    <h3>Result Screenshot</h3>
    <img src="https://github.com/user-attachments/assets/6e843547-20fe-4b3a-8009-4674138a87f7" alt="FastAPI Docs" width="100%" />
    &nbsp;&nbsp;&nbsp;
    <img src="https://github.com/user-attachments/assets/4165ebc5-7e2b-4a41-88cf-4a67fd0eccb9" alt="Details Criteria" width="100%" /> 
    &nbsp;&nbsp;&nbsp;
    <img src="https://github.com/user-attachments/assets/18e333ab-0d20-4dad-bcdf-39a82c6aec06" alt="Result" width="100%" />
  </div>
</div

---

## 📌 Features
- **Fine-tuned BioMistral-7B** using [Unsloth QLoRA](https://huggingface.co/unsloth) for domain-specific medical reasoning  
- **LangGraph Agentic RAG cycle** for reasoning with human validation
- **Disease detection** from symptoms + structured report data
- **Medical advisory recommendations** (non-diagnostic, informational only)
- **FastAPI backend** + **Streamlit frontend**
- **Dockerized** for consistent deployment

---

## 📂 Dataset & Model
- **Dataset:** [Clinical Dataset on Hugging Face](https://huggingface.co/datasets/your-dataset-link)  
- **LoRA Adapter:** [BioMistral-7B LoRA Adapter](https://huggingface.co/your-lora-adapter-link)

---

## 📁 Project Structure
```bash
AI-Health-Assistant/
├── tools/ # Utility scripts for data preprocessing, evaluation
├── llm/ # Model loading, fine-tuning, inference scripts
├── langgraph/ # LangGraph workflow, agent cycle, and RAG implementation
├── Dockerfile # Docker build file
├── requirements.txt # Python dependencies
├── main.py # App entry point (FastAPI + Streamlit integration)
└── README.md # Project documentation
```

---
## 🐳 Docker Deployment
Build and run:
```bash
docker build -t ai-health-assistant .
docker run -p 8000:8000 ai-health-assistant
```

---

## 📦 Pull from Docker Hub
If you prefer, you can pull the pre-built image from Docker Hub:

```bash
# Pull docker file
docker pull bodhipradeep/ai-health-assistant

# Run docker file
docker run -p 8000:8000 --env-file .env bodhipradeep/ai-health-assistant
```

---

## 🧠 How It Works
User uploads medical report / enters symptoms

LangGraph pipeline processes the input:

Extracts structured information

Retrieves relevant domain knowledge via ChromaDB

Performs reasoning using fine-tuned BioMistral-7B LoRA

Human-in-the-loop validation ensures safety and accuracy

Generates advisory output (non-diagnostic)

---

## ⚠️ Disclaimer
This project is for educational and research purposes only.
It does not provide medical advice. Always consult a qualified healthcare professional for diagnosis and treatment.

---

## 📜 License
MIT License © 2025 Pradeep Kumar













