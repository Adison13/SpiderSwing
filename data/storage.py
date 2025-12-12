import json
import os
from typing import List, Dict, Any

# Pasta do projeto (um nível acima de /data)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Caminho ABSOLUTO para o scores.json
ARQ_SCORES = os.path.join(BASE_DIR, "data", "scores.json")


def garantir_arquivo():
    pasta_data = os.path.join(BASE_DIR, "data")
    os.makedirs(pasta_data, exist_ok=True)

    if not os.path.exists(ARQ_SCORES):
        with open(ARQ_SCORES, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)


def carregar_scores() -> List[Dict[str, Any]]:
    garantir_arquivo()
    try:
        with open(ARQ_SCORES, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def salvar_scores(lista: List[Dict[str, Any]]):
    garantir_arquivo()
    with open(ARQ_SCORES, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)


def caminho_scores() -> str:
    """Só para debug (se você quiser printar no main)."""
    return ARQ_SCORES

