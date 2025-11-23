from typing import List
from ..models.home_model import TranslateResult
from ..db import translations_col
from ..db import lemmas_col
from ..models.lemma_model import LemmaModel


async def home_translate_text(
    source_text: str,
    source_lang: str,
    target_lang: str,
) -> List[TranslateResult]:

    results: List[TranslateResult] = []

    # ===== TG → ZH =====
    if source_lang == "tg" and target_lang == "zh":
        doc = await translations_col.find_one({
            "sourceLang": "tg",
            "targetLang": "zh",
            "sourceText": source_text
        })

        if not doc:
            return []

        lemma = doc.get("lemma", "")
        root = doc.get("root", "")
        description = doc.get("description", "")

        for t in doc.get("translations", []):
            results.append(
                TranslateResult(
                    translation=t.get("translation", ""),
                    pos=", ".join(t.get("posArray", [])),
                    description=description,
                    lemma=lemma,
                    root=root,
                    originalSentence=t.get("context", {}).get("source", ""),
                    translatedSentence=t.get("context", {}).get("target", "")
                )
            )

    # ===== ZH → TG =====
    elif source_lang == "zh" and target_lang == "tg":
        cursor = translations_col.find({
            "targetLang": "zh",
            "translations.searchTexts": source_text
        })

        async for doc in cursor:
            lemma = doc.get("lemma", "")
            root = doc.get("root", "")
            description = doc.get("description", "")
            sourceText = doc.get("sourceText", "")

            for t in doc.get("translations", []):
                if source_text in t.get("searchTexts", []):
                    results.append(
                        TranslateResult(
                            translation=sourceText,
                            pos=", ".join(t.get("posArray", [])),
                            description = description,
                            lemma=lemma,
                            root=root,
                            originalSentence=t.get("context", {}).get("source", ""),
                            translatedSentence=t.get("context", {}).get("target", "")
                        )
                    )

    return results


async def get_lemma_by_lemma_service(lemma: str) -> dict | None:
    result = await lemmas_col.find_one({"lemma": lemma})
    return result
