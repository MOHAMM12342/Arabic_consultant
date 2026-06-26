from transformers import pipeline
import sys
sys.stdout.reconfigure(encoding='utf-8')

pipe = pipeline("translation", model="saidettousy/AraT5_Darija_to_MSA")


#------------------------------------------------------
#verifier si le texte est ecrit en lettres latines ou arabes
def detect_script(text):
    arabic_count = 0
    latin_count = 0

    for char in text:
        # Arabic Unicode ,
        if (
            '\u0600' <= char <= '\u06FF' or
            '\u0750' <= char <= '\u077F' or
            '\u08A0' <= char <= '\u08FF'
        ):
            arabic_count += 1

        # Latin Unicode 
        elif (
            '\u0041' <= char <= '\u005A' or  # A-Z
            '\u0061' <= char <= '\u007A' or  # a-z
            '\u00C0' <= char <= '\u00FF'     # accented latin letters
        ):
            latin_count += 1

    if arabic_count > latin_count:
        return "arabic"
    else:
        return "Latin"

#----------------------------------------------------------------
#tranformation des lettres latines en lettres arabes 
def latin_to_arabic_darija(text):
    text = text.lower()

    # Combinaisons
    combinations = {
        "ch": "ش",
        "gh": "غ",
        "kh": "خ",
        "sh": "ش",
        "th": "ث",
        "dh": "ذ",

        # combinaisons avec chiffres
        "3a": "عا",
        "3i": "عي",
        "3o": "عو",
    }

    # remplacer les combinaisons
    for latin, arabic in combinations.items():
        text = text.replace(latin, arabic)

    # caractères simples
    mapping = {
        "3": "ع",
        "7": "ح",
        "9": "ق",
        "5": "خ",
        "8": "غ",
        "2": "ء",

        "a": "ا",
        "b": "ب",
        "c": "ك",
        "d": "د",
        "e": "ي",
        "f": "ف",
        "g": "گ",
        "h": "ه",
        "i": "ي",
        "j": "ج",
        "k": "ك",
        "l": "ل",
        "m": "م",
        "n": "ن",
        "o": "و",
        "p": "پ",
        "q": "ق",
        "r": "ر",
        "s": "س",
        "t": "ت",
        "u": "و",
        "v": "ڤ",
        "w": "و",
        "x": "كس",
        "y": "ي",
        "z": "ز",
        " ": " "
    }

    result = ""
    for char in text:
        result += mapping.get(char, char)

    return result

#----------------------------------------------------------------
#afficher le resultat
def affichage(text):
    if detect_script(text)=="arabic":
        translation = pipe(text)[0]['translation_text']
        return translation
    else:
        text=latin_to_arabic_darija(text) 
        translation = pipe(text)[0]['translation_text']
        return translation
