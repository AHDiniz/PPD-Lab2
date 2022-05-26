import hashlib
import random
import sys
from time import perf_counter
from submit_status import SubmitStatus
from transaction_bo import TransactionBO

transaction_bo = TransactionBO()

transaction_bo.start_server()

while (True):
    transaction_id = transaction_bo.get_transaction_id()
    challenge = transaction_bo.get_challenge(transaction_id)
    print("Challenge: {0}".format(challenge))
    print("Transaction ID: {0}".format(transaction_id))

    seed = 0
    start = perf_counter()
    # generate a random seed until it is valid
    while (True):
        seed = random.randint(0, sys.maxsize)
        hashed_seed = hashlib.sha1(
            seed.to_bytes(8, byteorder='big')).hexdigest()
        prefix = hashed_seed[0:challenge]

        # iterate over prefix characters to check if it is a valid seed
        for i in range(0, challenge):
            if prefix[i] != "0":
                break
        else:
            break

    end = perf_counter()
    t = end-start

    result = transaction_bo.submit_challenge(
        transaction_id, seed, 1)

    print("Time to finish: {0:.4f}s, seed: {1}".format(t, seed))
