#include <stdio.h>
#include <stdlib.h>
#include "rpcMiner_bo.h"
#include "rpcMiner_dao.h"
#include <openssl/sha.h>

// implement functions from rpcMiner_bo.h

int calculate_seed(int challenge, int seed);

int get_transaction_id_bo()
{
    return get_current_transaction_id();
}

int get_challenge_bo(int transactionId)
{
    Transaction *transaction = get_transaction_by_id(transactionId);

    if (transaction == NULL)
    {
        return -1; // transaction not found
    }
    return get_challenge_item(transaction); // challenge for the transaction
}

int get_transaction_status_bo(int transactionId)
{
    Transaction *transaction = get_transaction_by_id(transactionId);

    if (transaction == NULL)
    {
        return -1; // transaction not found
    }

    if (get_seed_item(transaction) == -1)
    {
        return 1; // transaction pending
    }

    return 0; // transaction finished
}

int submit_challenge_bo(SubmitChallengeRequest *submitRequest)
{
    if (submitRequest == NULL)
    {
        return -1; // invalid request
    }

    int transactionId = submitRequest->transactionId;
    int seed = submitRequest->seed;
    int clientId = submitRequest->clientId;

    Transaction *transaction = get_transaction_by_id(transactionId);

    if (transaction == NULL)
    {
        return -1; // transaction not found
    }

    if (get_seed_item(transaction) != -1)
    {
        return 2; // transaction already finished
    }
    int challenge = get_challenge_item(transaction);
    int result = calculate_seed(challenge, seed);
    if (result == -1)
    {
        return -1; // invalid seed
    }
    set_seed_item(transaction, seed);
    set_winner_item(transaction, clientId);
    create_transaction();

    return 0; // valid challenge submitted
}

int calculate_seed(int challenge, int seed)
{
    char data[2000000000];
    sprintf(data, "%d", seed);
    size_t length = strlen(data);
    unsigned char hash[SHA_DIGEST_LENGTH];
    SHA1(data, length, hash);
    // hash now contains the 20-byte SHA-1 hash
    for (int i = 0; i < challenge; i++)
    {
        if (hash[i] != '0')
        {
            return 0; // invalid seed
        }
    }
    return 1; // valid seed
}

int get_winner_bo(int transactionId)
{
    Transaction *transaction = get_transaction_by_id(transactionId);

    if (transaction == NULL)
    {
        return -1; // transaction not found
    }

    if (get_seed_item(transaction) == -1)
    {
        return 0; // transaction pending
    }

    return get_winner_item(transaction); // winner for the transaction
}

SeedResponse get_seed_bo(int transactionId)
{
    SeedResponse seedResponse;
    Transaction *transaction = get_transaction_by_id(transactionId);

    if (transaction == NULL)
    {
        seedResponse.status = -1; // transaction not found
        return seedResponse;
    }

    seedResponse.seed = get_seed_item(transaction);
    seedResponse.status = get_transaction_status_bo(transactionId);
    seedResponse.challenge = get_challenge_item(transaction);
    return seedResponse;
}