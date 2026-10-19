import sys
from io_utils import open_and_return
from chunking import chunker


def main():
    path = "data/datasets/AnsweredQuestions/dataset_docs_public.json"
    try:
        data = open_and_return(path)
    except Exception as e:
        print(f"Error: {e}")
    chunked_data = chunker(data)


if __name__ == "__main__":
    main()
