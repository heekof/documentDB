from enum import Enum, auto

class DocumentStatus(Enum):
    ACTIVE = auto()
    HOT = auto()
    COLD = auto()
    ARCHIVE = auto()
    SOFT_DELETE = auto()


class Status(Enum):
    PENDING = auto()      # 1
    RUNNING = auto()      # 2
    COMPLETED = auto()    # 3