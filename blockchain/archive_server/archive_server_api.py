'''

'''

import requests
import json
from web3 import Web3

url = "https://network-archive.ambrosus.io"  # Replace with the URL of your Geth node

# Create a web3.py object
web3 = Web3(Web3.HTTPProvider(url))

# Get the address that you want to find transactions for
address = "0x08B1f6724BF069150Aa382e1454C5CB6208bC3Fc"
block_number = web3.eth.get_block('latest').number
block_number = 24776208
print("block_number: ", block_number, ", type: ", type(block_number))

balance = web3.eth.get_balance(address)
print("balance: ", balance)

my_block = web3.eth.get_block(block_number)
print(my_block)

my_transaction_count = web3.eth.get_transaction_count(address)
print("transaction count: ", my_transaction_count)

# Query the node for all transactions that have been sent to the address
#transactions = web3.eth.getTransactions(address)
#transactions = web3.eth.get_transaction(transaction_hash)



# For each transaction, get the sender address
sender_addresses = []
for transaction in transactions:
    sender_address = transaction.from_address
    sender_addresses.append(sender_address)

# Print the list of sender addresses
print(sender_addresses)



# Create the JSON-RPC request payload
payload = {
    "jsonrpc": "2.0",
    "method": "eth_call",
    "params": [
        {
            "to": "0xContractAddress",  # Replace with the contract address
            "data": "0xFunctionSignature"  # Replace with the function signature
        },
        "latest"
    ],
    "id": 1
}

# Send the JSON-RPC request
response = requests.post(url, json=payload)

# Check the response status code
if response.status_code == 200:
    # Parse the response JSON
    result = response.json()
    # Process the result
    print(result)
else:
    # Print an error message if the request was not successful
    print("Request failed with status code:", response.status_code)

