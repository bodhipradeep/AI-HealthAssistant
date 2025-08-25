from utils.model_loader import llm

def symptoms_analysis(symptoms, patient_details, weather_info, report=None) -> str:
    prompt = f"""
    You are an experienced MBBS doctor. Analyze the patient’s symptoms, report (if available), and weather conditions step by step.  
    Identify the **most likely common diseases** that match, considering seasonal or environment-related factors.  

    ### Instructions
    1. Use patient details (age, gender, location, weather, lifestyle hints if present).  
    2. Integrate report findings if provided.  
    3. Focus on **common, likely diseases**.  
    4. Avoid rare diseases unless symptoms strongly suggest them.  
    5. Output **only a clean bullet list of possible diseases** (no explanations).  

    ### Few-shot Example
    Input Symptoms: ["frequent urination", "thirst", "weight loss"]  
    Output Diseases:  
    - Type 2 Diabetes Mellitus  
    - Urinary Tract Infection  
    - Hyperthyroidism  

    Input Symptoms: ["joint pain", "stiffness", "difficulty walking"]  
    Output Diseases:  
    - Osteoarthritis  
    - Rheumatoid Arthritis  
    - Vitamin D Deficiency 

    Patient Details:
    {patient_details}

    If weather clearly influences the symptoms (e.g., seasonal allergies, heat exhaustion, viral outbreaks), include it.
    Otherwise ignore it completely.
    Current Weather:
    {weather_info}

    Patient Symptoms:
    {symptoms}

    Patient Report Data (if available, use to confirm or reject possibilities):
    {report}
    
    First, analyze each symptom logically.
    Then, combine symptoms into clusters of possible conditions.
    Finally, output ONLY a bullet list of the most likely diseases.

    Your Answer:
    e.g
    - Common Cold = Viral Upper Respiratory Infection
    - Vitamin B12 Deficiency = Fatigue, Weakness
    - Viral Pharyngitis = Sore Throat, Cough
    - Diabetes = Increased Thirst, Frequent Urination
    ....
    """
    return llm.invoke(prompt)
