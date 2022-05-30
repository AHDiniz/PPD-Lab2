class SeedStatus:
    def __init__(self, status: int, seed: int, challenge: int):
        self.status = status
        self.seed = seed
        self.challenge = challenge
        self.__dict__ = {
            'status': self.status,
            'seed': self.seed,
            'challenge': self.challenge
        }

    # override the str method
    def __str__(self) -> str:
        return "Status: " + str(self.status) + " Seed: " + str(self.seed) + " Challenge: " + str(self.challenge)

