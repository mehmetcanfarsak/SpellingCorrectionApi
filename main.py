from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel
from typing import List
from textblob import TextBlob

description_of_fastapi = """
## Simple, reliable and free Spelling Correction Api

## 💻 Deployment  
You can deploy your own instance of SpellingCorrectionApi using the button below. You will just need a free [Deta](https://www.deta.sh/) account.  
[![Click Here To Deploy Your Own FreeEmailValidationApi  💻️](https://button.deta.dev/1/svg)](https://go.deta.dev/deploy?repo=https://github.com/mehmetcanfarsak/SpellingCorrectionApi)

### ⌨️ Github Page:

> [https://github.com/mehmetcanfarsak/SpellingCorrectionApi](https://github.com/mehmetcanfarsak/SpellingCorrectionApi "https://github.com/mehmetcanfarsak/SpellingCorrectionApi")

"""
app = FastAPI(title="🔠 Simple Spelling Correction Api", description=description_of_fastapi,
              contact={"url": "https://github.com/mehmetcanfarsak", "Name": "Mehmet Can Farsak"})


class ParagraphModel(BaseModel):
    paragraph: str = "hi how arw yom? thid is my tesy"


class WrongWordModel(BaseModel):
    original_word: str
    corrected_word: str


class CorrectionResultModel(BaseModel):
    original_text: str
    text_after_correction: str
    all_words_before_correction_as_list: list
    all_words_after_correction_as_list: list
    wrong_words_as_list: List[WrongWordModel]


def get_correcttion_results(original_text):
    all_words_before_correction_as_list = original_text.split()
    text_after_correction = ""
    all_words_after_correction_as_list = []
    wrong_words_as_list = []
    for original_word in all_words_before_correction_as_list:
        corrected_word = TextBlob(original_word).correct().string
        all_words_after_correction_as_list.append(corrected_word)
        text_after_correction += " " + corrected_word
        if (corrected_word == original_word):
            continue
        wrong_words_as_list.append(WrongWordModel(original_word=original_word,
                                                  corrected_word=corrected_word))

    return CorrectionResultModel(
        original_text=original_text,
        text_after_correction=text_after_correction,
        all_words_before_correction_as_list=all_words_before_correction_as_list,
        all_words_after_correction_as_list=all_words_after_correction_as_list,
        wrong_words_as_list=wrong_words_as_list
    )


@app.get("/", include_in_schema=False, response_class=RedirectResponse)
def root():
    return RedirectResponse("/docs")


@app.get("/correct-sentence", response_model=CorrectionResultModel, tags=["Correct a word or a sentence"])
def correct_sentence(sentence: str = "hi how arw yom? thid is my tesy"):
    return get_correcttion_results(sentence)


@app.post("/correct-paragraph", response_model=CorrectionResultModel, tags=["Correct any paragraph"])
def correct_paragraph(paragraph: ParagraphModel):
    return get_correcttion_results(paragraph.paragraph)


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")
