from enum import StrEnum, auto


class Stage(StrEnum):
    INTRO = auto()
    EDA = auto()
    MODELS = auto()


STAGES = Stage.__members__
