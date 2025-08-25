from utils.model_loader import llm

def diagnosis(symptoms, patient_details, analysis, report=None) -> str:
    prompt = f"""
You are a highly experienced MBBS & MD physician. Provide a structured **diagnostic reasoning note** based on the patient’s symptoms, report, and preliminary analysis.  

### Instructions
1. Analyze each symptom individually and link to possible conditions.  
2. Cross-check with **patient details** (age, gender, weight, height, location, weather).  
3. Integrate report findings (if available).  
4. Consider at least **2–3 differential diagnoses**.  
5. Eliminate mismatches logically.  
6. Provide one **Primary Diagnosis** and at least two differentials.  

### Few-shot Example
Input Symptoms: ["fever", "cough", "sore throat"]  
Output:  
Primary Diagnosis: Viral Pharyngitis  
Possible Differential Diagnoses:  
- Influenza  
- Bacterial Tonsillitis 

Input Symptoms: ["frequent urination", "thirst", "weight loss"]  
Output:  
Primary Diagnosis: Type 2 Diabetes Mellitus  
Possible Differential Diagnoses:  
- Urinary Tract Infection  
- Hyperthyroidism

Patient Details:
{patient_details}

Symptoms:
{symptoms}

Previous Analysis (for reference, not final):
{analysis}

Patient Report Data (if available, use to confirm or reject possibilities):
{report}

Before giving the final diagnosis, you must think in depth step by step.
<think>
your thinking area
</think>

Provide **one Primary Diagnosis (the most likely)**.  
If two are equally strong, list both together.  

Your Answer:
Primary Diagnosis: <one or two conditions most strongly supported>
Possible Differential Diagnoses:
- Differential 1
- Differential 2
- Differential 3 
"""
    return llm.invoke(prompt)