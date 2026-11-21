from fastapi import APIRouter

from app.nlp.methodology import ALGORITHM_VERSION, FORMULAS, SOURCES
from app.security.auth import DB, Actor
from app.services.access import get_course
from app.services.configuration import analysis_config

router = APIRouter(tags=["Методика перевірки"])


@router.get("/analysis/methodology")
def methodology(db: DB, actor: Actor, course_id: int | None = None):
    course = get_course(db, actor, course_id) if course_id is not None else None
    config = analysis_config(db, course)
    example = {"semantic": 0.85, "lexical": 0.50, "coverage": 0.75}
    return {
        "algorithm_version": ALGORITHM_VERSION,
        "minimum_references": 2,
        "formulas": FORMULAS,
        "sources": SOURCES,
        "configuration": config.model_dump(),
        "example": {
            **example,
            "score": round(
                example["semantic"] * config.semantic_weight
                + example["lexical"] * config.lexical_weight
                + example["coverage"] * config.concept_weight,
                6,
            ),
        },
        "interpretation": "Індекс відповідності не є ймовірністю правильності чи автоматичною оцінкою. "
        "Критична змістова суперечність дає LOW_MATCH; пропущені обов’язкові поняття або "
        "нове заперечення не дозволяють HIGH_MATCH. Остаточне рішення ухвалює викладач.",
        "length_policy": "Довжина використовується лише для перевірки допустимого введення. "
        "Кількість символів не входить до жодної формули індексу відповідності.",
    }
