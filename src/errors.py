class RagError(Exception):
    """Error esperado: se muestra al usuario sin traceback"""


class IndexLoadError(RagError):
    """Error en el indexado."""


class EmptyQuestionError(RagError):
    """Error: pregunta vacía."""


class InvalidKError(RagError):
    """Error: k inválido"""
