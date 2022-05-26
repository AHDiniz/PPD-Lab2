import hashlib
from seed_status import SeedStatus
from submit_status import SubmitStatus
from transaction_dao import TransactionDAO
from transaction_status import TransactionStatus
from transaction import Transaction


class TransactionBO:
    invalid_id = -1

    def __init__(self):
        self.transaction_dao = TransactionDAO()

    # start server transactions
    def start_server(self) -> Transaction:
        transaction = self.transaction_dao.create_transaction()
        return transaction

    # return the id of the transaction open for challenge
    def get_transaction_id(self) -> int:
        return self.transaction_dao.get_last_transaction().transaction_id

    # return the challenge of the transaction given by id or -1 if not found
    def get_challenge(self, transaction_id: int) -> int:
        transaction: Transaction = self.transaction_dao.get_transaction(
            transaction_id)
        if transaction is None:
            return self.invalid_id
        return transaction.challenge

    # return status of the transaction given by id or -1 if not found
    def get_transaction_status(self, transaction_id: int) -> TransactionStatus:
        transaction = self.transaction_dao.get_transaction(transaction_id)
        if transaction is None:
            return TransactionStatus.invalid_id

        if transaction.seed is None:
            return TransactionStatus.pendente

        return TransactionStatus.resolvido

    # submit a seed for the transaction given by id and return if it is valid or not, -1 if not found
    def submit_challenge(self, transaction_id: int, seed: int, client_id: int) -> SubmitStatus:
        transaction = self.transaction_dao.get_transaction(transaction_id)
        if transaction is None:
            return SubmitStatus.invalid_id

        if transaction.seed is not None:
            return SubmitStatus.ja_solucionado

        hashed_seed = hashlib.sha1(
            seed.to_bytes(8, byteorder='big')).hexdigest()
        prefix = hashed_seed[0:transaction.challenge]

        # iterate over prefix characters to check if it is a valid seed
        for i in range(0, transaction.challenge):
            if prefix[i] != "0":
                return SubmitStatus.invalido

        # mark the transaction as solved and the winner, return valid
        transaction.seed = seed
        transaction.winner = client_id
        self.transaction_dao.create_transaction()
        return SubmitStatus.valido

    # get the winner of the transaction given by id, 0 if no winner or -1 if not found

    def get_winner(self, transaction_id: int) -> int:
        transaction = self.transaction_dao.get_transaction(transaction_id)
        if transaction is None:
            return self.invalid_id

        if (transaction.seed is None):
            return 0

        return transaction.winner

    # get the seed of the transaction given by id, None if not found
    def get_seed(self, transaction_id: int) -> SeedStatus:
        transaction = self.transaction_dao.get_transaction(transaction_id)
        if transaction is not None:
            return SeedStatus(self.get_transaction_status(transaction_id), transaction.seed, transaction.challenge)
