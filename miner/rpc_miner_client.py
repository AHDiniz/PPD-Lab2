from enum import Enum
import hashlib
import random
import sys
from time import perf_counter
from seed_status import SeedStatus
from submit_status import SubmitStatus
from transaction_status import TransactionStatus
import xmlrpc.client


# Calcula total de argumentos
n = len(sys.argv)
 
# Verificação do uso correto/argumentos
if (n!=3):
    print("\nUso correto: rpc_miner_client server_address port_number.\n")
    exit(-1)


rpcServerAddr = "http://" + sys.argv[1] + ":" + sys.argv[2] + "/"
proxy = xmlrpc.client.ServerProxy(rpcServerAddr)

class Menu(Enum):
    TRANSACTION = 1
    CHALLENGE = 2
    STATUS = 3
    WINNER = 4
    RESULT = 5
    MINER = 6
    EXIT = 99

class MinerClient:
    def __init__(self):
        pass

    def run(self):
        while True:
            self.__show_menu()
            option = int(input('Escolha uma opção: '))
            if option == Menu.TRANSACTION.value:
                self.get_transaction_id()
            elif option == Menu.CHALLENGE.value:
                self.get_challenge()
            elif option == Menu.STATUS.value:
                self.get_transaction_status()
            elif option == Menu.WINNER.value:
                self.get_winner()
            elif option == Menu.RESULT.value:
                self.get_seed()
            elif option == Menu.MINER.value:
                self.mine()
            elif option == Menu.EXIT.value:
                print("Saindo...")
                break
            else:
                print('Opção inválida')

    def __show_menu(self):
        print('''
MENU:
[1] - Transação atual
[2] - Desafio
[3] - Status
[4] - Vencedor
[5] - Resultado
[6] - Minerar
[99] - Sair
            ''')


    def __input_transaction_id(self):
        return int(input("Enter Transaction ID: "))

    def get_transaction_id(self) -> int:
        transaction_id = proxy.getTransactionID()
        print("Transaction ID: {0}".format(transaction_id))
        return transaction_id

    def get_challenge(self, transaction_id: int = None) -> int:
        if (transaction_id is None):
            transaction_id = self.__input_transaction_id()
            challenge = proxy.getChallenge(transaction_id)
            print("Challenge: {0}".format(challenge))
            return challenge
        else:
            return proxy.getChallenge(transaction_id)

    def get_transaction_status(self, transaction_id: int = None) -> TransactionStatus:
        if (transaction_id is None):
            transaction_id = self.__input_transaction_id()
            status = proxy.getTransactionStatus(transaction_id)
            print("Status: {0}".format(status))
            return status
        else:
            return proxy.getTransactionStatus(transaction_id)

    def get_winner(self, transaction_id: int = None) -> int:
        if (transaction_id is None):
            transaction_id = self.__input_transaction_id()
            winner = proxy.getWinner(transaction_id)
            print("Winner: {0}".format(winner))
            return winner
        else:
            return proxy.getWinner(transaction_id)

    def get_seed(self, transaction_id: int = None) -> SeedStatus:
        if (transaction_id is None):
            transaction_id = self.__input_transaction_id()
            seed = proxy.getSeed(transaction_id)
            print("Seed: {0}".format(seed))
            return seed
        else:
            return proxy.getSeed(transaction_id)

    def __submit_challenge(self, transaction_id: int, seed: int, client_id: int) -> SubmitStatus:
        print("Submitting challenge...")
        return proxy.submitChallenge(transaction_id, seed, client_id)

    def mine(self) -> None:
        transaction_id = self.get_transaction_id()
        challenge = self.get_challenge(transaction_id)


        # TODO: implementar o código para paralelizar o cálculo do seed
        start = perf_counter()
        seed = 0
        # generate a random seed until it is valid
        while (True):
            seed = random.randint(0, 2000000000)
            hashed_seed = hashlib.sha1(
                seed.to_bytes(4, byteorder='big')).hexdigest()
            prefix = hashed_seed[0:challenge]

            # iterate over prefix characters to check if it is a valid seed
            for i in range(0, challenge):
                if prefix[i] != "0":
                    break
            else:
                break

        end = perf_counter()
        t = end-start

        result = self.__submit_challenge(
            transaction_id, seed, 1)

        print("Time to finish: {0:.4f}s, result: {1}, seed: ".format(t, result, self.get_seed(transaction_id)))


miner = MinerClient()
miner.run()