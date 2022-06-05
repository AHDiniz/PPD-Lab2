class SubmitRequest:
    def __init__(self, transaction_id: int, seed: int, client_id: int) -> None:
        self.transaction_id = transaction_id
        self.seed = seed
        self.client_id = client_id
        self.__dict__ = {
            "transaction_id": self.transaction_id,
            "seed": self.seed,
            "client_id": self.client_id
        }
