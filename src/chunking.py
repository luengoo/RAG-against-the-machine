import json

class MarkdownStrategy(paths):
    paths = self.paths
    
    def chunker(self):
        for path in self.paths:
            try:
                with open(path, encoding="utf-8") as file:
                    data = json.load(file)
                    for mark in data
            except Exception:
                print("Something went wrong")