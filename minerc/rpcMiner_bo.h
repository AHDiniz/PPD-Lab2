#include "rpcMiner.h"
#ifndef _RPCMINER_BO_H
#define _RPCMINER_BO_H
int get_transaction_id_bo();
int get_challenge_bo(int transactionId);
int get_transaction_status_bo(int transactionId);
int submit_challenge_bo(SubmitChallengeRequest* submitRequest);
int get_winner_bo(int transactionId);
SeedResponse get_seed_bo(int transactionId);
#endif