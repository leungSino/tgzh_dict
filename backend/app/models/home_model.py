from pydantic import BaseModel
from typing import List, Optional, Literal

class TranslateRequest(BaseModel):
    sourceText: str
    sourceLang: str
    targetLang: str
    model: str = "default"  # 可选，默认模型

class Example(BaseModel):
    source: str
    target: str


class VerbForm(BaseModel):
    form: str
    person: Optional[str] = None
    meaning: Optional[str] = None


class DerivativeForm(BaseModel):
    form: str
    pos: Optional[str] = ""
    meaning: Optional[str] = ""


class WordForms(BaseModel):
    present: Optional[List[VerbForm]] = None
    past: Optional[List[VerbForm]] = None
    future: Optional[List[VerbForm]] = None
    imperative: Optional[List[VerbForm]] = None
    derivatives: Optional[List[DerivativeForm]] = None


class TranslateResult(BaseModel):
    translation: str
    description: str = ""
    pos: str = ""
    lemma: str = ""
    root: str = ""
    originalSentence: str = ""
    translatedSentence: str = ""

    type: Optional[Literal["word", "lemma", "root", "derived"]] = "word"

    brief: Optional[str] = ""                     # 简要解释（词根/lemma 用）
    meanings: Optional[List[str]] = []            # 多释义（普通词多义词）

    forms: Optional[WordForms] = None             # 时态/派生词
    examples: Optional[List[Example]] = []        # 示例句子
