from utils.model_loader import llm

def more_symptoms(symptoms, patient_details, weather_info, analysis, report=None) -> str:
    prompt = f"""
    You are a MBBS doctor. Suggest additional symptoms that are **medically realistic and commonly associated** with the patient’s suspected condition.  

    ### Instructions
    1. Suggest **4–6 additional symptoms** only.  
    2. Use short **keywords** (e.g., "fatigue", "headache", "nausea").  
    3. Avoid long sentences.  
    4. Exclude rare or unrelated symptoms.  
    5. Always consider the **Patient Disease Analysis (for reference, not final)**:  
    - Suggested symptoms should be **medically consistent** with both the provided symptoms **and** the suspected disease in the analysis.  
    - Example: If analysis suggests *Vitamin B12 deficiency*, include symptoms like "tiredness, weakness, memory loss".  
    - Example: If analysis suggests *diabetes or thyroid disorder*, include symptoms like "increased thirst, weight changes, fatigue".  
    6. Start the output with one short line:  
    **"Based on the provided symptoms and preliminary disease analysis, additional possible symptoms are:"**  
    7. Then provide symptoms as a **bullet-point list**.  

    ---

    ### Few-shot Example
    Input Symptoms: ["fever"]  
    Disease Analysis: *Likely viral infection*  
    Output:  
    Based on the provided symptoms and preliminary disease analysis, additional possible symptoms are:  
    - cough  
    - body ache  
    - headache  
    - weakness  

    ---

    ### Few-shot Example
    Input Symptoms: ["tiredness, leg pain"]  
    Disease Analysis: *Possible Vitamin B12 deficiency*  
    Output:  
    Based on the provided symptoms and preliminary disease analysis, additional possible symptoms are:  
    - fatigue  
    - weakness  
    - memory loss  
    - numbness in hands/feet

    ---

    Patient Details:
    {patient_details}

    Current Weather (ignore if irrelevant to symptoms):
    {weather_info}

    Patient Symptoms:
    {symptoms}

    Patient Disease Analysis (for reference, not final):
    {analysis}

    Patient Report Data:
    optional[{report}]
    
    ### Your Final Answer
    
    """
    return llm.invoke(prompt)