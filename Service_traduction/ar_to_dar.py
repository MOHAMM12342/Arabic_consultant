#traduction arabe ---> anglais

from transformers import pipeline
ar_to_en = pipeline("translation", model="Helsinki-NLP/opus-mt-ar-en")


#traduction anglais ---> darija
pipe = pipeline("translation", model="BAKKALIAYOUB/DarijaTranslation-V1")



def fct(text):
    text_en=ar_to_en(text)[0]['translation_text']
    text_ar=pipe(text_en)[0]['translation_text']
    return text_ar
