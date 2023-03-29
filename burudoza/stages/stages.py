from enum import StrEnum, auto


class Stage(StrEnum):
    INTRO = auto()
    EDA = auto()
    MODELS = auto()


STAGES = Stage._member_names_
