import re
from abc import ABC, abstractmethod

class Wallet(ABC):
	def __init__(self, wallet_address):
		if self.is_valid_eth_address(wallet_address):
			self.address = wallet_address
		else:
			raise Exception("wallet_address has an invalid format!")
		self.transaction_hashes = []
		self.transaction_details = {}
		self.balance = 0
		self.last_update_on_block = 0
		self.query_limit = 0
		self.input_addresses = {} # Dict of dicts with {"0x...":{"count":(number of appearances), "sum":(sum of all transactions in sats)}}
		self.output_addresses = {} # List of touples with {"address":"0x...", "count":(number of appearances), "sum":(sum of all transactions in sats)}

	@abstractmethod
	def is_updated(self):
		# Todo: check if the objects information is up to date
		return False

	@abstractmethod
	def query_all(self):
		# Todo: update wallets information
		return True


	def set_query_limit(self, limit):
		self.query_limit = limit

	def get_wallet_address(self):
		return self.address

	def get_all_transaction_hashes(self):
		return self.transaction_hashes

	def get_transaction_count(self):
		return len(self.transaction_hashes)

	def get_transaction_details(self, tx_hash):
		return self.transaction_details.get(tx_hash)

	def get_input_addresses(self):
		return self.input_addresses

	def get_output_addresses(self):
		return self.output_addresses


	@staticmethod
	def is_valid_eth_address(address):
		# Check if the address matches the pattern
		pattern = r"^0x[a-fA-F0-9]{40}$"
		match = re.match(pattern, address)

		# Return True if the address is valid, False otherwise
		return bool(match)



class MyClass:
    # Class-level attributes
    class_attribute = "Hello, I am a class attribute"

    # Constructor (initializer) method
    def __init__(self, parameter1, parameter2):
        # Instance-level attributes
        self.parameter1 = parameter1
        self.parameter2 = parameter2

    # Instance method
    def instance_method(self):
        print("I am an instance method")
        print("Instance attribute value:", self.parameter1)

    # Class method
    @classmethod
    def class_method(cls):
        print("I am a class method")
        print("Class attribute value:", cls.class_attribute)

    # Static method
    @staticmethod
    def static_method():
        print("I am a static method")