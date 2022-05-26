from enum import Enum


class SubmitStatus(Enum):
    valido = 1
    invalido = 0
    ja_solucionado = 2
    invalid_id = -1

    # override the str method
    def __str__(self) -> str:
        return "Submit Status: " + str(self.value)
    
    def __dict__(self):
        return self.value