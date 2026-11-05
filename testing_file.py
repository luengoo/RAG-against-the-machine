from src.corpus import iter_corpus_files
vacios = [p for p in iter_corpus_files("data/raw")
          if not open(p, encoding="utf-8").read().strip()]
print(len(vacios), vacios[:5])