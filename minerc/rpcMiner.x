struct SubmitChallengeRequest {
       int transactionId;
       int seed;
       int clientId;
};

struct SeedResponse {
    int status;
    int seed;
    int challenge;
};

program PROG { 
       version VERSAO { 
            int get_transaction_id(void) = 1;
            int get_challenge(int) = 2;
            int get_transaction_status(int) = 3;
            int submit_challenge(SubmitChallengeRequest) = 4;
            int get_winner(int) = 5;
            SeedResponse get_seed(int) = 6;
       } = 100;
} = 55555555;

