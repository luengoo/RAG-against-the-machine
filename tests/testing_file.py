from src.models import RagDataset
import json
from typing import List
from pydantic import ValidationError


def check_datasets(paths: List[str]):
    for path in paths:
        try:
            with open(path, encoding="utf-8") as file:
                data = json.load(file)
                dataset = RagDataset.model_validate(data)
                if dataset.rag_questions:
                    q = dataset.rag_questions[0]
                print(path)
                print(len(dataset.rag_questions))
                print(type(q).__name__)
        except (ValidationError, json.JSONDecodeError, OSError) as exc:
            print(exc)

def chunk_testing


if __name__ == "__main__":
    check_datasets([
        "data/datasets/AnsweredQuestions/dataset_docs_public.json",
        "data/datasets/AnsweredQuestions/dataset_code_public.json",
        "data/datasets/UnansweredQuestions/dataset_docs_public.json",
        "data/datasets/UnansweredQuestions/dataset_code_public.json"
    ])
