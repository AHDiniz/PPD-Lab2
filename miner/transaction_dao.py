from typing import List
from transaction import Transaction

import random

transactions: List[Transaction] = []


class TransactionDAO:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # add a transaction to the list of transactions
    def create_transaction(self) -> None:
        transaction = Transaction(
            self.get_last_transaction().transaction_id + 1, random.randint(1, 128), None, -1)
        transactions.append(transaction)

    # get a transaction by id
    def get_transaction(self, transaction_id: int) -> Transaction:
        for transaction in transactions:
            if transaction.transaction_id == transaction_id:
                return transaction

    # update a transaction by id
    def update_transaction(self, transaction_id: int, challenge: int, seed: str, winner: int) -> Transaction:
        for transaction in transactions:
            if transaction.transaction_id == transaction_id:
                transaction.challenge = challenge
                transaction.seed = seed
                transaction.winner = winner
                return transaction

    # get last transaction
    def get_last_transaction(self) -> Transaction:
        if len(transactions) == 0:
            return Transaction(-1, 0, None, -1)  # default transaction

        return transactions[-1]
