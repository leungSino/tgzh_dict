from typing import List
from ..models.home_model import TranslateResult
from ..db import translations_col


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

        for t in doc.get("translations", []):
            results.append(
                TranslateResult(
                    translation=t.get("translation", ""),
                    pos=", ".join(t.get("posArray", [])),
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

            for t in doc.get("translations", []):
                if source_text in t.get("searchTexts", []):
                    results.append(
                        TranslateResult(
                            translation=t.get("context", {}).get("source", t.get("translation", "")),
                            pos=", ".join(t.get("posArray", [])),
                            lemma=lemma,
                            root=root,
                            originalSentence=t.get("context", {}).get("source", ""),
                            translatedSentence=t.get("context", {}).get("target", "")
                        )
                    )

    return results
