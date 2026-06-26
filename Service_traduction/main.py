from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dar_to_ar import affichage
from ar_to_dar import fct

app = FastAPI(title="Translation API")

class TranslationRequest(BaseModel):
    text: str

class TranslationResponse(BaseModel):
    translated_text: str

@app.post("/translate/dar-to-ar", response_model=TranslationResponse)
async def translate_darija_to_arabic(request: TranslationRequest):
    try:
        translated = affichage(request.text)
        return TranslationResponse(translated_text=translated)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/translate/ar-to-dar", response_model=TranslationResponse)
async def translate_arabic_to_darija(request: TranslationRequest):
    try:
        translated = fct(request.text)
        return TranslationResponse(translated_text=translated)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)