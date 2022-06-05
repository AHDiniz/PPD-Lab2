#include "rpcMiner_dao.h"

struct transaction_struct
{
    int transactionId;
    int challenge;
    int seed;
    int winner;
};
const MAX_TRANSACTIONS = 1000;
Transaction trasactions[MAX_TRANSACTIONS];
int nextTransactionId = 1;


// implement functions from rpcMiner_dao.h
int get_current_transaction_id()
{
    return nextTransactionId - 1;
}

Transaction *get_transaction_by_id(int transactionId);

void create_transaction() {
    Transaction *transaction = &trasactions[nextTransactionId];
    transaction->transactionId = get_current_transaction_id();
    transaction->challenge = rand() % 20;
    transaction->seed = -1;
    transaction->winner = -1;
    nextTransactionId++;
}

int get_transaction_id_item(Transaction *transaction)
{
    if (transaction == NULL)
    {
        return -1; // transaction not found
    }
    return transaction->transactionId;
}

int get_challenge_item(Transaction *transaction)
{
    if (transaction == NULL)
    {
        return -1; // transaction not found
    }
    return transaction->challenge;
}
int get_seed_item(Transaction *transaction)
{
    if (transaction == NULL)
    {
        return -1; // transaction not found
    }
    return transaction->seed;
}
int get_winner_item(Transaction *transaction)
{
    if (transaction == NULL)
    {
        return -1; // transaction not found
    }
    return transaction->winner;
}

int set_seed_item(Transaction *transaction, int seed)
{
    if (transaction == NULL)
    {
        return -1; // transaction not found
    }
    transaction->seed = seed;
    return 0;
}
int set_winner_item(Transaction *transaction, int winner)
{
    if (transaction == NULL)
    {
        return -1; // transaction not found
    }
    transaction->winner = winner;
    return 0;
}