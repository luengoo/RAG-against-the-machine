from typing import List
from pydantic import BaseModel, Field
import uuid


class MinimalSource(BaseModel):
    file_path: str
    first_character_index: int
    last_character_index: int


class Chunk(BaseModel):
    """Un trozo indexado: text[start:end] del fichero file_path."""

    file_path: str
    start: int
    end: int

    def to_source(self) -> MinimalSource:
        """Convierte el chunk en la fuente que espera la moulinette."""
        return MinimalSource(
            file_path=self.file_path,
            first_character_index=self.start,
            last_character_index=self.end
        )


class UnansweredQuestion(BaseModel):
    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str


class AnsweredQuestion(UnansweredQuestion):
    sources: List[MinimalSource]
    answer: str


class RagDataset(BaseModel):
    rag_questions: List[AnsweredQuestion | UnansweredQuestion]


class MinimalSearchResults(BaseModel):
    question_id: str
    question: str
    retrieved_sources: List[MinimalSource]


class MinimalAnswer(MinimalSearchResults):
    answer: str


class StudentSearchResults(BaseModel):
    search_results: List[MinimalSearchResults]
    k: int


class StudentSearchResultsAndAnswer(BaseModel):
    search_results: List[MinimalAnswer]
    k: int
