from enum import Enum

class TransactionStatus(Enum):
    resolvido = 0
    pendente = 1
    invalid_id = -1
    
    # override the str method
    def __str__(self) -> str:
        return "Transaction Status: " + str(self.value)