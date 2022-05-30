from xmlrpc.server import SimpleXMLRPCServer

from transaction_bo import TransactionBO

transaction_bo = TransactionBO()

# A simple server with simple arithmetic functions
server = SimpleXMLRPCServer(("0.0.0.0", 8000), allow_none=True)
print("Listening on port 8000...")
#server.register_multicall_functions()
server.register_function(transaction_bo.get_transaction_id, 'getTransactionID')
server.register_function(transaction_bo.get_challenge, 'getChallenge')
server.register_function(transaction_bo.get_transaction_status, 'getTransactionStatus')
server.register_function(transaction_bo.submit_challenge, 'submitChallenge')
server.register_function(transaction_bo.get_winner, 'getWinner')
server.register_function(transaction_bo.get_seed, 'getSeed')
transaction_bo.start_server()
server.serve_forever()
