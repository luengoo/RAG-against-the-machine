import json
from models import RagDataset


def open_and_return(path: str):
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
            dataset = RagDataset.model_validate(data)

        if not data:
            print("Path's file is empty!")
            return
        else:
            return data
    except Exception as e:
        return f"{e}"
