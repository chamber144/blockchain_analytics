#!/usr/bin/env python3

import argparse, sys, asyncio
from blockchain.Wallet import Wallet

parser = argparse.ArgumentParser()

parser.add_argument("wallet", type=str,
					help="AMB Wallet address")
parser.add_argument("-t", "--transactions", help="Gets all transaction IDs of the specified address", action="store_true")
parser.add_argument("-i", "--input_addresses", help="Gets all addresses that sent to the specified address.", action="store_true")
parser.add_argument("-o", "--output_addresses", help="Gets all addresses the specified address was sending to.", action="store_true")

parser.add_argument("-n", "--native_explorer_api", help="Parse the native explorer api (explorer-api.airdao.io)", action="store_true")
parser.add_argument("-b", "--blockbook_api", help="Parse the blockbook api (blockbook.airdao.io)", action="store_true")
parser.add_argument("-a", "--archive_server_api", help="Parse the archive server api (network-archive.ambrosus.io)", action="store_true")

parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2],
                    help="increase output verbosity")
#args = parser.parse_args()

def start(argument_parser):

	try:
		#sys.stderr = open(os.devnull, 'w')
		args = argument_parser.parse_args()
		sys.stderr = sys.__stderr__
	except:
		print()
		argument_parser.print_help()
		exit(1)

	if Wallet.is_valid_eth_address(args.wallet):
		#my_wallet = Wallet(args.wallet)
		print("Great, you provided a valid AMB address: ", args.wallet, "\n")
		if not args.input_addresses and not args.output_addresses and not args.transactions:
			print("But what you want me to do with it?\n")
	else:
		print("this is NOT a valid wallet address!!! God dammit!!!")
		exit()

	wallets = []

	if args.native_explorer_api:
		import blockchain.amb_explorer
		explorer_wallet = import_wallet_from_api(args.wallet, blockchain.amb_explorer)

	if args.blockbook_api:
		from blockchain.blockbook.BlockbookWallet import BlockbookWallet
		blockbook_wallet = BlockbookWallet(args.wallet)
		blockbook_wallet = import_wallet_from_api(blockbook_wallet)
		wallets.append(blockbook_wallet)

	if args.archive_server_api:
		import blockchain.archive_server
		archive_wallet = import_wallet_from_api(args.wallet, blockchain.archive_server)

	def format_amb_amount(amount):
		amb_amount = amount/1000000000000000000
		if amb_amount >= 1000000:
			return str(int(amb_amount/1000000))+"M"
		if amb_amount >= 1000:
			return str(int(amb_amount/1000))+"k"
		return str(int(amb_amount))

	for my_wallet in wallets:

		total_transactions_input = 0
		total_transactions_output = 0
		total_value_input = 0
		total_value_output = 0

		if args.transactions:
			print("Total transactions: ",len(my_wallet.get_all_transaction_hashes()))

		if args.input_addresses:
			print("\nInput addresses:")
			for my_address in my_wallet.get_input_addresses():
				details = my_wallet.get_input_addresses().get(my_address)
				print(my_address, ": count:", details.get("count"), "total AMB:", format_amb_amount(details.get("sum")))
				total_value_input += details.get("sum")
				total_transactions_input += details.get("count")

		if args.output_addresses:
			print("\nOutput addresses:")
			for my_address in my_wallet.get_output_addresses():
				details = my_wallet.get_output_addresses().get(my_address)
				print(my_address, ": count:", details.get("count"), "total AMB:", format_amb_amount(details.get("sum")))
				total_value_output += details.get("sum")
				total_transactions_output += details.get("count")

		print("\n\nSource address:",my_wallet.get_wallet_address(),"\n")

		print("Total input addresses:", len(my_wallet.get_input_addresses()))
		print("Total input transacions:",total_transactions_input)
		print("Total input value:",format_amb_amount(total_value_input),"\n")

		print("Total output addresses:", len(my_wallet.get_output_addresses()))
		print("Total output transacions:",total_transactions_output)
		print("Total output value:",format_amb_amount(total_value_output))
		


def import_wallet_from_api(wallet_object):
	my_wallet = wallet_object
	my_wallet.query_all()
	#print("\nwallet:", my_wallet.get_wallet_address())
	#print("transaction hashes:", my_wallet.get_all_transaction_hashes())

	#print("\ntransaction count:", my_wallet.get_transaction_count())

	#for tx in my_wallet.get_all_transaction_hashes():
		#print("-----------------------------------")
		#print("type: ", type(my_wallet.get_transaction_details(tx)))
		#print("my_wallet.get_transaction_details(tx):\n", my_wallet.get_transaction_details(tx))
		#for detail in my_wallet.get_transaction_details(tx):
		#	print(detail, ": ", my_wallet.get_transaction_details(tx).get(detail))
		#print()
	return my_wallet

start(parser)