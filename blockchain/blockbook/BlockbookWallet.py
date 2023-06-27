from ..Wallet import Wallet
import blockchain.blockbook.blockbook_api as bb
import asyncio

class BlockbookWallet(Wallet):
	BASE_URL = "https://blockbook.ambrosus.io/api/v2/"
	SOURCE = "blockbook"

	def is_updated(self):
		# Todo: check if the objects information is up to date
		return False

	def query_transaction_hashes(self):
		print("query transaction hashes...")
		self.transaction_hashes = asyncio.run(bb.get_transactions(self.address))
		print("got a total of",len(self.transaction_hashes),"transactions...\n")

	async def query_transactions_details_async(self, my_transaction_hashes):
		answer = {}
		tasks = []
		for tx in my_transaction_hashes:
			tasks.append(asyncio.create_task(bb.get_transaction_details(tx)))

		for get_transaction_details_task in asyncio.as_completed(tasks):
			my_transaction_details = await get_transaction_details_task
			tx = my_transaction_details.get("txid")
			#print("adding to answer[",tx,"]",my_transaction_details)
			answer[tx] = my_transaction_details
		return answer


	async def query_all_transaction_details_async(self):
		semaphore = asyncio.Semaphore(1)
		tasks = []
		for tx in self.transaction_hashes:
			async with semaphore:
				tasks.append(asyncio.create_task(bb.get_transaction_details(tx)))


			#await semaphore.acquire()
			#tasks.append(asyncio.create_task(bb.get_transaction_details(tx)))
			#semaphore.release()

		for get_transaction_details_task in asyncio.as_completed(tasks):
			async with semaphore:
				#await semaphore.acquire()
				my_transaction_details = await get_transaction_details_task
				#semaphore.release()
				tx = my_transaction_details.get("txid")
				self.transaction_details[tx] = my_transaction_details

	def query_all_transaction_details(self):
		print("query all transaction details...")
		#asyncio.run(self.query_transactions_async(self.transaction_hashes))
		counter = 0
		counter_total = 0
		max_connections = 50
		my_transaction_hashes = []
		#print("\ntype(my_transaction_hashes)",type(my_transaction_hashes))
		for tx in self.transaction_hashes:
			#print("counter:", counter, ", counter_total:", counter_total)
			counter += 1
			counter_total += 1
			my_transaction_hashes.append(tx)
			if counter == max_connections or counter_total == len(self.transaction_hashes):
				my_transaction_details = asyncio.run(self.query_transactions_details_async(my_transaction_hashes))
				#print("len(my_transaction_hashes)",len(my_transaction_hashes))
				#print("len(my_transaction_details)",len(my_transaction_details))
				for tx in my_transaction_details:
					#transaction_hash = transaction_details.get("txid")
					#print("tx: ",tx,", type(tx):",type(tx))
					self.transaction_details[tx] = my_transaction_details.get(tx)
				print("queried",counter,"additional transactions, totaling",counter_total,"transaction details for now...")
				my_transaction_hashes = []
				counter = 0
				#print("--------------------------------------------")
		#print("counter_total:",counter_total)
		#print("len(self.transaction_details)",len(self.transaction_details))



		#asyncio.run(self.query_all_transaction_details_async())
		#for tx in self.transaction_hashes:
		#	self.transaction_details[tx] = bb.get_transaction_details(tx)

	def extract_all_addresses(self):
		print("extract all addresses...")
		for tx in self.transaction_hashes:
			my_json = self.transaction_details.get(tx)
			my_sender = my_json.get("vin")[0].get("addresses")[0]
			my_receiver = my_json.get("vout")[0].get("addresses")[0]
			value = int(my_json.get("value"))

			def add_address_to_dictionary(address, dictionary):
				if address.upper() not in self.address.upper():
					if address in dictionary:
						dictionary[address] = {
							"count": dictionary.get(address).get("count") + 1,
							"sum": dictionary.get(address).get("sum") + value
						}
					else:
						dictionary[address] = {"count": 1, "sum": value}

			add_address_to_dictionary(my_sender, self.input_addresses)
			add_address_to_dictionary(my_receiver, self.output_addresses)
			'''
			if my_sender not in self.address:
				if my_sender in self.input_addresses:
					self.input_addresses[my_sender] = {
						"count": self.input_addresses.get(my_sender).get("count") + 1,
						"sum": self.input_addresses.get(my_sender).get("sum") + value
					}
				else:
					self.input_addresses[my_sender] = {"count": 1, "sum": value}

			if my_receiver not in self.address:
				if my_receiver in self.output_addresses:
					self.output_addresses[my_receiver] = {
						"count": self.output_addresses.get(my_receiver).get("count") + 1,
						"sum": self.output_addresses.get(my_receiver).get("sum") + value
					}
				else:
					self.output_addresses[my_receiver] = {"count": 1, "sum": value}
			'''


	def query_all(self):
		# Todo: update wallets information
		self.query_transaction_hashes()
		self.query_all_transaction_details()
		self.extract_all_addresses()
		return True

