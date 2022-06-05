from enum import Enum
import hashlib
import random
import sys
import xmlrpc.client
import threading as thrd
from multiprocessing import cpu_count
from time import perf_counter
from submit_request import SubmitRequest
from seed_status import SeedStatus

# Calcula total de argumentos
n = len(sys.argv)
 
# Verificação do uso correto/argumentos
if (n!=3):
    print("\nUso correto: rpc_miner_client server_address port_number.\n")
    exit(-1)


rpcServerAddr = "http://" + sys.argv[1] + ":" + sys.argv[2] + "/"
proxy = xmlrpc.client.ServerProxy(rpcServerAddr, allow_none=True)

class SeedCalculator(thrd.Thread):
    def __init__(self, challenge):
        thrd.Thread.__init__(self)
        self.__challenge = challenge
        self.__seed = 0
        self.__time_to_finish = 0
    
    @property
    def seed(self):
        return self.__seed
    
    @property
    def time_to_finish(self):
        return self.__time_to_finish

    def run(self):
        start = perf_counter()

        while True:
            self.__seed = random.randint(0, 2000000000)
            hashed_seed = hashlib.sha1(self.__seed.to_bytes(8, byteorder='big')).hexdigest()
            prefix = hashed_seed[0:self.__challenge]

                # iterate over prefix characters to check if it is a valid seed
            for i in range(0, self.__challenge):
                if prefix[i] != "0":
                    break
            else:
                break

        end = perf_counter()

        self.__time_to_finish = end - start

class Menu(Enum):
    TRANSACTION = 1
    CHALLENGE = 2
    STATUS = 3
    WINNER = 4
    RESULT = 5
    MINER = 6
    EXIT = 99

class MinerClient:
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

    def get_transaction_status(self, transaction_id: int = None) -> int:
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

    def __submit_challenge(self, transaction_id: int, seed: int, client_id: int) -> int:
        print("Submitting challenge...")
        return proxy.submitChallenge(SubmitRequest(transaction_id, seed, client_id))

    def mine(self) -> None:
        
        while (True):
            print("Procurando transação...")
            transaction_id = self.get_transaction_id()
            challenge = self.get_challenge(transaction_id)

            count = 0
            # TODO: implementar o código para paralelizar o cálculo do seed
            start = perf_counter()
            seed = 0
            # generate a random seed until it is valid
            while (count < 5000000):
                count = count + 1
                seed = random.randint(0, 2000000000)
                hashed_seed = hashlib.sha1(
                    seed.to_bytes(8, byteorder='big')).hexdigest()
                prefix = hashed_seed[0:challenge]

                # iterate over prefix characters to check if it is a valid seed
                for i in range(0, challenge):
                    if prefix[i] != "0":
                        break
                else:
                    break
            else:                
                print("Não foi possível gerar um seed válido em 500000 tentativas")
                continue

            end = perf_counter()
            t = end-start

            result = self.__submit_challenge(
                transaction_id, seed, client_id)

            print("Time to finish: {0:.4f}s, result: {1}, seed: {2}".format(t, result, self.get_seed(transaction_id)))

client_id = randint(0, 100)
miner = MinerClient()
miner.run()