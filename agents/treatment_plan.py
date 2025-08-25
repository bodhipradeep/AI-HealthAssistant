from utils.model_loader import llm

def treatment_plan(diagnosis_result: str) -> str:
    prompt = f"""
You are a Senior MBBS & MD. Based on the **final diagnosis result**, prepare a safe and evidence-based **treatment plan**.  
Be precise, clinically realistic, and patient-friendly. 

Diagnosis Result (to analyze):
{diagnosis_result}


Before giving your plan, think step by step in depth.

<think>
- Recheck the diagnosis against common symptoms
- Consider possible complications
- Identify immediate vs. long-term precautions
- Suggest safe, widely used treatments
- Recommend supportive care (diet, lifestyle)
- Add follow-up tests if uncertainty remains
</think>

For each possible primary diagnosis, suggest a safe treatment plan.
If multiple conditions are possible, outline supportive care that is safe in all.

### Instructions
    1. Diagnosis Result for Making Treatment plan.  
    2. Always Follow serial for each disease plan.  
    3. You can use relevent emoji for beutify.
    
    
### Few-shot Example
### Analysis Diagnosis Result:
e.g.
- Type 2 Diabetes Mellitus
- Vitamin B12 Deficiency
- Viral Fever
- Constipation

---
## Treatment Plan:
### Disease 1: [Name] 
Reason: [Explain briefly why diagnosis is considered]
#### Precautions:
- [Immediate precautions]
- [Lifestyle precautions]
#### Medicines:
- [First-line medications with typical dosing info if relevant]
- [Monitoring instructions]
#### Diet Plan:
- [Recommended foods, avoidances]
#### Suggested Tests:
- [Follow-up labs, imaging, or screenings]
#### Red-Flag Symptoms:
- [Symptoms requiring urgent care]

---
### Disease 2:
#### Precautions:
#### Medicines:
#### Diet Plan:
#### Suggested Tests:
#### Red-Flag Symptoms:

---
### Common Supportive Measures:
- [Hydration, sleep, stress management, gentle exercise, yoga, etc.]

Your Final Output:
"""

    return llm.invoke(prompt)