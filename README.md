# 🏥 AI Health Assistant

AI Health Assistant is an experimental multi-agent medical reasoning system that accepts patient symptoms and optional report PDFs, runs a LangGraph-powered agent workflow, and returns structured diagnostic reasoning plus a recommended treatment plan. The system is intended for research and human-in-the-loop experimentation and is not a substitute for professional medical care.

## Tech used
- Python 3.11+
- FastAPI (backend)
- Streamlit (front-end)
- Speech AI (Audio output)
- LangGraph (workflow & HITL) 
- LangChain / Transformers (LLM adapters)
- Unsloth QLoRA (For Fine-Tuned 2x faster)
- Docker for containerization

---
## Output Screenshot
<img width="1679" height="915" alt="Screenshot 2025-08-24 183419" src="https://github.com/user-attachments/assets/70f50ee8-4006-4824-9044-cfb69e8bbdd9" />

---
## 📌 Features
- **Fine-tuned BioMistral-7B** using [Unsloth QLoRA](https://huggingface.co/unsloth) for domain-specific medical reasoning
- **Input** Pateint details, symptoms, report(optional), weather info automatic use if needed 
- **LangGraph Human-in-the-loop cycle** for reasoning with human validation
- **Multi-node LangGraph workflow:** symptom analysis → generated symptoms → patient confirmation (HITL) → diagnosis → treatment plan
- **Disease detection** from symptoms + structured report data
- **Medical advisory recommendations** (non-diagnostic, informational only)
- **FastAPI backend** + **Streamlit frontend**
# AI Health Assistant

---
## 📂 Dataset & Model
- **Dataset:** [Clinical Dataset on Hugging Face](https://huggingface.co/datasets/FreedomIntelligence/medical-o1-reasoning-SFT)
- **Base Model** [[BioMistral-7B Base Model](https://huggingface.co/BioMistral/BioMistral-7B)
- **QLoRA Adapter:** [[BioMistral-7B QLoRA Adapter](https://huggingface.co/PradeepBodhi/BioMistral-7b_Fine-Tuned-QLoRA)
- **Full Fine-Tuned** [[BioMistral-7B QLoRA Adapter + Base Model](https://huggingface.co/PradeepBodhi/BioMistral-7b_Fine-Tuned-FULL)

---
## Project structure

AI-HealthAssistant/
├── Dockerfile                # Docker container definition (runs uvicorn fastapi_app:app)
├── docker-compose.yml        # Example compose file
├── requirements.txt          # Python dependencies
├── pyproject.toml            # Project metadata
├── main.py                   # Simple local entry/test script
├── main_st.py                # Streamlit UI client
├── fastapi_app.py            # FastAPI backend (endpoints and session handling)
├── README.md                 # This file
├── src/
│   ├── main_page.png         # Empty UI Screenshot
│   ├── output.png            # Output UI Screenshot
│   └── image.png             # Langgrpah Flow image
├── agents/
│   ├── diagnosis.py          # diagnosis logic (model prompt + invocation)
│   ├── gen_symptoms.py       # generate/refine symptoms
│   ├── sym_analyzer.py       # symptom analysis
│   └── treatment_plan.py     # produce treatment plan from diagnosis
├── workflow/
│   ├── graph_builder.py      # LangGraph StateGraph definition and compilation
│   ├── agent_nodes.py        # node wrappers that call agent functions
│   ├── append_symptoms.py    # append new symptoms from HITL
│   └── hitl.py               # human-in-the-loop helpers
├── config/
│   ├── config.yaml           # LLM/provider configuration
│   └── settings.py           # other settings
├── core/
│   ├── report_loader.py      # PDF extraction helper
│   └── weather_info.py       # optional weather enrichment
├── utils/
│   ├── model_loader.py       # Fine-Tuned LLM/model initialization and selection
│   └── config_loader.py
└── .env.example              # .env file for api key requirement

--- 
## 🐳 Docker Deployment

Build and run locally:

```powershell
; docker build -t ai-healthassistant .
; docker run -p 8000:8000 --env-file .env ai-healthassistant
```

Using docker-compose:

```powershell
; docker-compose up --build
```

## 📦 Pull from Docker Hub
If you prefer, you can pull the pre-built image from Docker Hub:

```bash
# Pull docker file
docker pull bodhipradeep/ai-health-assistant

# Run docker file
docker run -p 8000:8000 --env-file .env bodhipradeep/ai-health-assistant
```
---
## How it works (detailed flow — based on `workflow/graph_builder.py`)

The LangGraph state graph composes the multi-agent reasoning pipeline as follows:

1. Symptoms_Analysis (node_symptoms_analysis)
2. Generated_Symptoms (node_generated_symptoms)
3. Patient_Confirmation (human_assistance)
4. Conditional branching (human_decision)
5. Need_More_Symptoms (append_symptoms.add_symptoms)
6. Diagnosis (node_diagnosis)
7. Final_Report (node_treatment_plan)
8. End: the graph returns the aggregated messages and final plan to the API caller.

---
## API (quick reference)

- POST `/diagnose/start` — start a new session
  - JSON: `{ "symptoms": [...], "patient_details": {...}, "report": "optional text" }`
  - Returns: `{ "thread_id": "...", "symptoms": [...], "result": "..." }`

- POST `/diagnosis/resume` — resume a session from the UI or via API
  - JSON: `{ "thread_id": "...", "human": "feedback" | "approved", "more_symptoms": [...] }`

---
## Disclaimer

This project is research/educational only and does not provide medical advice. Always consult a licensed healthcare professional for diagnosis and treatment.

## License

MIT License © 2025 Pradeep Kumar

## Author / Contact

Pradeep Kumar

- LinkedIn: [Pradeep Kumar](https://www.linkedin.com/in/bodhi-pradeep/)  
- Email: [Gmail](mailto:pradeep.kmr.pro@gmail.com)




