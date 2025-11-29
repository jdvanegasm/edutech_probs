import json
import random
from fastapi import FastAPI
from typing import Dict, Any
from fastapi.middleware.cors import CORSMiddleware

from models.question_models import (
    ProblemRequest, GeneratedProblem,
    TestRequest, GradeRequest, GradeResponse
)
from solvers import SOLVERS
from utils.clean_params import clean_params

app = FastAPI(title="API Probabilidad", version="0.1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------
# CARGAR QUESTIONS JSON
# ---------------------------------------------------
with open("questions.json", "r") as f:
    QUESTIONS = {q["id"]: q for q in json.load(f)}


# ---------------------------------------------------
# HELPERS
# ---------------------------------------------------
def render_statement(template: str, params: Dict[str, Any]) -> str:
    return template.format(**params)


def generate_params(q):
    params = {}

    for key, rule in q["params"].items():

        # min dinámico
        if isinstance(rule["min"], str) and rule["min"] in params:
            min_v = params[rule["min"]]
        else:
            min_v = rule["min"]

        # max dinámico
        if isinstance(rule["max"], str) and rule["max"] in params:
            max_v = params[rule["max"]]
        else:
            max_v = rule["max"]

        # int o float
        if isinstance(min_v, int) and isinstance(max_v, int):
            params[key] = random.randint(min_v, max_v)
        else:
            params[key] = random.uniform(min_v, max_v)

    return params


def solver_returns_number(solver_fn):
    numeric_solvers = {
        "binomial_exact",
        "poisson_mas_de_un",
        "prob_falla_antes",
        "prob_bateria_operacion",
        "prob_bateria_entre",
        "normal_mayor_que",
        "poisson_exacto",
        "binomial_al_menos",
        "torneo_segundo_gana",
        "utilidad_maxima",
        "proporcion_esferas",
    }
    return solver_fn.__name__ in numeric_solvers


# ---------------------------------------------------
# ENDPOINTS
# ---------------------------------------------------

@app.get("/")
def root():
    return {"message": "Backend de Probabilidad funcionando!"}


# --------------------------
# LIST QUESTIONS (CON DOCS)
# --------------------------
@app.get("/questions")
def list_questions():
    return [
        {
            "id": qid,
            "topic": data["topic"],
            "doc_url": data.get("doc_url"),
            "doc_summary": data.get("doc_summary")
        }
        for qid, data in QUESTIONS.items()
    ]


# --------------------------
# GENERATE PROBLEM (PRACTICE/MODE REPASO)
# Devuelve doc_url y doc_summary
# --------------------------
@app.post("/generate-problem")
def generate_problem(req: ProblemRequest):
    q = QUESTIONS[req.id]

    # parámetros
    params = req.params_override or generate_params(q)
    params = clean_params(params, q["solver"])

    # enunciado
    statement = render_statement(q["template"], params)

    # si es repaso, resolver
    correct_answer = None
    if req.mode == "repaso":
        solver_fn = SOLVERS[q["solver"]]
        correct_answer = solver_fn(**params)

    # devolvemos flexible (NO usamos GeneratedProblem porque no soporta doc_url)
    return {
        "id": req.id,
        "statement": statement,
        "params": params,
        "correct_answer": correct_answer,
        "doc_url": q.get("doc_url"),
        "doc_summary": q.get("doc_summary")
    }


# --------------------------
# GENERATE TEST (sin ayudas)
# --------------------------
@app.post("/generate-test")
def generate_test(req: TestRequest):
    # 1. filtrar solo solvers adecuados para tests (numéricos)
    valid_ids = [
        qid for qid, q in QUESTIONS.items()
        if solver_returns_number(SOLVERS[q["solver"]])
    ]

    if req.num_questions > len(valid_ids):
        raise ValueError(
            f"No hay suficientes preguntas numéricas. "
            f"Solicitaste {req.num_questions}, pero solo hay {len(valid_ids)} disponibles."
        )

    # 2. Selección
    selected = random.sample(valid_ids, req.num_questions)
    questions_output = []

    for qid in selected:
        q = QUESTIONS[qid]

        params = generate_params(q)
        params = clean_params(params, q["solver"])

        statement = render_statement(q["template"], params)
        correct = SOLVERS[q["solver"]](**params)

        spread = abs(correct) * 0.2 if correct != 0 else 0.1
        options = [
            correct,
            correct + random.uniform(-spread, spread),
            correct + random.uniform(-spread, spread),
            correct + random.uniform(-spread, spread)
        ]
        random.shuffle(options)

        questions_output.append({
            "id": qid,
            "topic": q["topic"],
            "statement": statement,
            "options": options,
            "correct": correct,
            "doc_url": q.get("doc_url"),
            "doc_summary": q.get("doc_summary")
        })

    return {"questions": questions_output}


# --------------------------
# GRADE TEST
# --------------------------
@app.post("/grade-test", response_model=GradeResponse)
def grade_test(req: GradeRequest):
    total = len(req.answers)
    correct_count = 0
    details = []

    for ans in req.answers:
        is_correct = abs(ans.selected - ans.correct) < 1e-6
        if is_correct:
            correct_count += 1

        details.append({
            "id": ans.id,
            "selected": ans.selected,
            "correct": ans.correct,
            "is_correct": is_correct
        })

    score = round((correct_count / total) * 100, 2)
    return GradeResponse(score=score, details=details)


# --------------------------
# TOPICS
# --------------------------
@app.get("/topics")
def list_topics():
    topics = sorted(list({q["topic"] for q in QUESTIONS.values()}))
    return {"topics": topics}


# --------------------------
# QUESTIONS BY TOPIC (CON DOCS)
# --------------------------
@app.get("/questions/by-topic/{topic}")
def questions_by_topic(topic: str):
    return [
        {
            "id": qid,
            "topic": data["topic"],
            "doc_url": data.get("doc_url"),
            "doc_summary": data.get("doc_summary")
        }
        for qid, data in QUESTIONS.items()
        if data["topic"].lower() == topic.lower()
    ]


# FULL QUESTIONS
@app.get("/questions/full")
def list_full_questions():
    return list(QUESTIONS.values())