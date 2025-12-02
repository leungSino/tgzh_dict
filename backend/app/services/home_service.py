from typing import List, Optional
from ..models.home_model import (
    TranslateResult, WordForms, VerbForm, DerivativeForm, Example
)
from ..db import translations_col, lemmas_col


async def home_translate_text(
    source_text: str,
    source_lang: str,
    target_lang: str,
) -> List[TranslateResult]:

    results: List[TranslateResult] = []

    # ===========================================================
    # TG → ZH
    # ===========================================================
    if source_lang == "tg" and target_lang == "zh":

        # ------------------- 1. 查 translations（精确匹配） -------------------
        trans_doc = await translations_col.find_one({
            "sourceLang": "tg",
            "targetLang": "zh",
            "sourceText": source_text
        })

        # ========== 1.1 命中 translations ==========
        if trans_doc:

            # ---------------- 该条为 lemma（需要补全 lemma 信息） ----------------
            if trans_doc.get("isLemma") is True:
                lemma_text = trans_doc.get("lemma")

                lemma_doc = await lemmas_col.find_one({"lemma": lemma_text})
                if not lemma_doc:
                    return []

                examples_list = lemma_doc.get("examples", [])
                examples = [
                    Example(source=e.get("tg", ""), target=e.get("zh", ""))
                    for e in examples_list
                ]

                forms = _build_word_forms(lemma_doc)
                translations = trans_doc.get("translations", [])
                translation = translations[0].get("translation", "")

                results.append(
                    TranslateResult(
                        translation=translation,
                        pos=", ".join(lemma_doc.get("pos", [])),
                        description=trans_doc.get("description", ""),
                        lemma=lemma_doc.get("lemma", ""),
                        root=lemma_doc.get("root", ""),

                        type="lemma",
                        brief=lemma_doc.get("brief", ""),
                        meanings=lemma_doc.get("meanings", []),
                        forms=forms,
                        examples=examples
                    )
                )
                return results

            # ---------------- 非 lemma：正常词条 ----------------
            else:
                lemma = trans_doc.get("lemma", "")
                root = trans_doc.get("root", "")
                description = trans_doc.get("description", "")

                for t in trans_doc.get("translations", []):
                    results.append(
                        TranslateResult(
                            translation=t.get("translation", ""),
                            pos=", ".join(t.get("posArray", [])),
                            description=description,
                            lemma=lemma,
                            root=root,
                            originalSentence=t.get("context", {}).get("source", ""),
                            translatedSentence=t.get("context", {}).get("target", ""),

                            type="word",
                            brief="",
                            meanings=[t.get("translation", "")],
                            forms=None,
                            examples=[]
                        )
                    )

                return results

        # ========== 2. translations 未命中 → 查 lemmas.lemma ==========
        lemma_doc = await lemmas_col.find_one({"lemma": source_text})

        # ========== 3. 若 lemma 仍未命中 → 查 lemmas.root ==========
        if not lemma_doc:
            lemma_doc = await lemmas_col.find_one({"root": source_text})

        if not lemma_doc:
            return []

        examples_list = lemma_doc.get("examples", [])
        examples = [
            Example(source=e.get("tg", ""), target=e.get("zh", ""))
            for e in examples_list
        ]

        forms = _build_word_forms(lemma_doc)

        results.append(
            TranslateResult(
                translation=lemma_doc.get("definition", {}).get("tg", ""),
                pos=", ".join(lemma_doc.get("pos", [])),
                description=lemma_doc.get("brief", ""),
                lemma=lemma_doc.get("lemma", ""),
                root=lemma_doc.get("root", ""),

                type="lemma" if source_text == lemma_doc.get("lemma") else "root",
                brief=lemma_doc.get("brief", ""),
                meanings=lemma_doc.get("meanings", []),
                forms=forms,
                examples=examples,
            )
        )
        return results

    # ===========================================================
    # ZH → TG
    # ===========================================================
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
                            description=description,
                            lemma=lemma,
                            root=root,
                            originalSentence=t.get("context", {}).get("source", ""),
                            translatedSentence=t.get("context", {}).get("target", ""),

                            type="word",
                            brief="",
                            meanings=[sourceText],
                            forms=None,
                            examples=[]
                        )
                    )
        return results

    return results


# ===========================================================
# Helper：构建 WordForms
# ===========================================================
def _build_word_forms(lemma_doc) -> Optional[WordForms]:
    # 使用 conjugations 字段
    conjugations_doc = lemma_doc.get("conjugations", {})

    # 使用 derived 字段
    derived_list = lemma_doc.get("derived", [])

    if not conjugations_doc and not derived_list:
        return None

    # 辅助函数：将动词形式字符串数组转换为 VerbForm 列表
    def _create_verb_forms(form_list: List[str], time_name: str) -> List[VerbForm]:
        forms = []
        # 按照 (ман, ту, ӯ, мо, шумо, онҳо) 的顺序
        persons = ["ман", "ту", "ӯ", "мо", "шумо", "онҳо"]

        for i, form_str in enumerate(form_list):
            person = persons[i] if time_name == 'present' and i < len(persons) else None
            forms.append(
                VerbForm(
                    form=form_str,
                    person=person if person else "",
                    meaning=""  # 无法从数据中获取，留空
                )
            )
        return forms

    return WordForms(
        present=_create_verb_forms(conjugations_doc.get("present", []), 'present') or None,
        past=_create_verb_forms(conjugations_doc.get("past", []), 'past') or None,
        future=_create_verb_forms(conjugations_doc.get("future", []), 'future') or None,

        # 命令式字段在数据结构中不存在，跳过或改为从 forms 中取
        imperative=None,

        # 派生词：将 derived 字符串数组转换为 DerivativeForm 列表
        derivatives=[
                        DerivativeForm(
                            form=d_form,
                            pos="",  # 无法从数据中获取，留空
                            meaning=""  # 无法从数据中获取，留空
                        ) for d_form in derived_list
                    ] or None
    )

# ===== 原型词查询 =====
async def get_lemma_by_lemma_service(lemma: str) -> dict | None:
    return await lemmas_col.find_one({"lemma": lemma})
