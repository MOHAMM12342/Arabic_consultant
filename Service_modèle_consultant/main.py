from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch

app = FastAPI(title="LLM Consultant API")

# You can change the model_id to any open-source Arabic-capable model
# Examples: "Qwen/Qwen2-7B-Instruct", "core42/jais-13b-chat", "meta-llama/Meta-Llama-3-8B-Instruct"
MODEL_ID = "Qwen/Qwen2-1.5B-Instruct" # Using a small model by default for local testing

print(f"Loading Model {MODEL_ID}...")
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype="auto",
        device_map="auto" # Will use GPU if available
    )
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
except Exception as e:
    print(f"Warning: Failed to load model. Error: {e}")
    generator = None

class GenerateRequest(BaseModel):
    query: str
    context: str

class GenerateResponse(BaseModel):
    response: str

@app.post("/generate", response_model=GenerateResponse)
async def generate_response(request: GenerateRequest):
    if generator is None:
        raise HTTPException(status_code=500, detail="Model is not loaded.")
        
    prompt_template = f"""أنت مستشار قانوني مغربي خبير في مدونة الأسرة.
استخدم المعلومات التالية للإجابة على سؤال المستخدم بدقة. إذا لم تكن المعلومات كافية، قل أنك لا تعرف.

المعلومات (Context):
{request.context}

سؤال المستخدم (Question):
{request.query}

الإجابة (Answer):
"""

    try:
        output = generator(
            prompt_template,
            max_new_tokens=512,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )
        
        # Extract the generated text after the prompt
        full_text = output[0]["generated_text"]
        response = full_text[len(prompt_template):].strip()
        
        return GenerateResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
