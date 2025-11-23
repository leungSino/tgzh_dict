from pydantic import BaseModel

class TranslateRequest(BaseModel):
    sourceText: str
    sourceLang: str
    targetLang: str
    model: str = "default"  # 可选，默认模型

class TranslateResult(BaseModel):
    translation: str
    description: str = ""
    pos: str = ""
    lemma: str = ""
    root: str = ""
    originalSentence: str = ""
    translatedSentence: str = ""
