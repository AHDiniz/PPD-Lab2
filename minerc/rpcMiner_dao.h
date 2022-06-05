#include "rpcMiner.h"

#ifndef _RPCMINER_DAO_H_
#define _RPCMINER_DAO_H_

typedef struct transaction_struct Transaction;


int get_current_transaction_id();

Transaction* get_transaction_by_id(int transactionId);

void create_transaction();

int get_transaction_id_item(Transaction* transaction);
int get_challenge_item(Transaction* transaction);
int get_seed_item(Transaction* transaction);
int get_winner_item(Transaction* transaction);

int set_seed_item(Transaction* transaction, int seed);
int set_winner_item(Transaction* transaction, int winner);

#endif
