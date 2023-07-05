import enum


class Operations(enum.Enum):
    GetFiles = 0
    UploadFile = 1
    GetFile = 2
    GoInDirectory = 3
    GoOutDirectory = 4
