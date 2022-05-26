from transaction_status import TransactionStatus


class SeedStatus:
    def __init__(self, status: TransactionStatus, seed: int, challenge: int):
        self.status = status
        self.seed = seed
        self.challenge = challenge
        
    # override the str method
    def __str__(self) -> str:
        return "Status: " + str(self.status) + " Seed: " + str(self.seed) + " Challenge: " + str(self.challenge)