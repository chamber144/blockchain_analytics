'''

'''

import requests, json, asyncio, aiohttp

url_base_blockbook = "https://blockbook.ambrosus.io/api/v2/"
apollo_onboarding_address = "0xA80e0B8595a3739266e0Ba7d1Bf8a5AcB9F9d433"
apollo_deposit_address = "0x8687424E13b437834b6D6203e9A0f1EE084F9c25"
apollo_onboarding_address_hera_hool = "0x5d82Fb586886c49D80170F6440039b7f5FA302DE"

'''
async def query_api(url):
	"""
	Input:	URL (String)
	Output:	JSON-Object with the answer from the API
	"""
	response = await requests.get(url)

	if response.status_code == 200:
		return response.json()
	else:
		# API call failed
		print("Error:", response.status_code)

	return
'''

async def query_api(url):
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as response:
			await asyncio.sleep(0.1)
			return await response.json()

async def get_transactions_by_page(address, page, page_size):
	answer = []

	my_URL = url_base_blockbook + "address/" + address + "?page=" + str(page) + "&pageSize=" + str(page_size)

	my_query = await query_api(my_URL)
	my_transactions = my_query.get("txids")
	for tx in my_transactions:
		answer.append(tx)

	return answer

async def get_transactions_number_of_pages(address, page_size):
	answer = 0
	my_URL = url_base_blockbook + "address/" + address + "?page=1&pageSize=" + str(page_size)
	query_answer = await query_api(my_URL)
	answer = query_answer.get("totalPages")
	return answer

async def get_transactions(address):
	"""
	Input: eth compatible wallet address as string

	Output: A list with all transactions of an address.
	"""
	result = []
	page_size = 1000
	page_count = await get_transactions_number_of_pages(address, page_size)

	tasks = []
	for i in range(page_count):
		tasks.append(asyncio.create_task(get_transactions_by_page(address, i + 1, page_size)))
		#transactions = get_transactions_by_page(address, i + 1, page_size)
		#for tx in transactions:
		#	result.append(tx)
	for task in asyncio.as_completed(tasks):
		transactions = await task
		for tx in transactions:
			result.append(tx)

	return result

async def get_transaction_details(transaction):
	"""
	Input:  A transaction hash as string
	Output: A nested dictionary with the transaction details. Example:
			{txid:	"0xd164c19ea685b0188376992d2f42437cd1178838ed84104bd9018aed26d05e1e"
			vin: 
				0:
					n: 0
					addresses:
						0: "0x3bD825b7Eb270b191d1C3886E2463159623C9EF5"
					isAddress: true
			vout:
				0:
					value: "1325787000000000000000000"
					n: 0
					addresses:
						0: "0xcD092a88C2e6CC2F9Ea30F714bD9dFdeA074796e"
					isAddress: true
			blockHash: 		"0x0cc7043c432755e9a981d347a97d4fb1b19055fb8f920b08ee4f9a742ff9f05a"
			blockHeight: 	24618726
			confirmations: 	167925
			blockTime: 		1684497210
			value: 			"1325787000000000000000000"
			fees: 			"210000000000000"
			ethereumSpecific:	
				status: 	1
				nonce: 		11281
				gasLimit: 	21000
				gasUsed: 	21000
				gasPrice: 	"10000000000"
				data: 		"0x"
	"""
	my_URL = url_base_blockbook + "tx/" + transaction
	answer = await query_api(my_URL)
	return answer

def get_transaction_sender_from_json(transaction_json):
	return transaction_json.get("vin")[0].get("addresses")[0]

def get_transaction_receiver_from_json(transaction_json):
	return transaction_json.get("vout")[0].get("addresses")[0]

def get_apollos(onboarding_address):
	"""
	An early intent to get a list with all apollo addresses.
	But there's something missing with the onboarding addresses:
	    The apollo_onboarding_address contains regular apollo nodes
	    The apollo_onboarding_address_hera_pool contains apollo nodes that are made by the staking pool (hera)
	    The sum of apollos which used those two onboarding addresses seems to be smaller than the total amount of apollo nodes.
	    There needs to be a third onboarding address, or a subset of apollos was onboarded differently.

	This function sirves as reference for later investigations.
	"""
	my_apollos = []
	my_page = 1
	my_URL = url_base_blockbook + "address/" + onboarding_address + "?page=" + str(my_page) + "&pageSize=500"
	print(my_URL)

	response = requests.get(my_URL)
	if response.status_code == 200:
		print()
		my_transactions = response.json().get("txids")
		for tx in my_transactions:
			tx_URL = url_base_blockbook + "tx/" + tx
			tx_response = requests.get(tx_URL)
			sender = tx_response.json().get("vin")[0].get("addresses")[0]
			if len(tx_response.json().get("vout")[0].get("addresses")) == 1:
				receiver = tx_response.json().get("vout")[0].get("addresses")[0]
			else:
				raise Exception("More than one receiver in transaction "+ tx +"! What we gonna do?")

			#print("From: " + sender + ", to: " + receiver)
			if sender != apollo_deposit_address and receiver != apollo_deposit_address:
				if receiver == apollo_onboarding_address:
					if sender not in my_apollos:
						my_apollos.append(sender)

		# make magic

	else:
		# API call failed
		print("Error:", response.status_code)


	return my_apollos

def print_nested_json(data, leading_space=""):
    if isinstance(data, dict):
        for key, value in data.items():
            print(leading_space + key, end=': ')
            print_nested_json(value, leading_space + "  ")
    elif isinstance(data, list):
        for item in data:
            print_nested_json(item, leading_space + "  ")
    else:
    	print(data)
		#print(f"Value: {data}")

if __name__ == "__main__":
	print("starting blockbook_api test function...")
	
	#transactions = get_transactions("0xcd092a88c2e6cc2f9ea30f714bd9dfdea074796e")
	#print("total transactions: ",str(len(transactions)))

	#transaction_details = get_transaction_details("0xd164c19ea685b0188376992d2f42437cd1178838ed84104bd9018aed26d05e1e")
	#print(transaction_details.get("vin")[0].get("addresses")[0])
	#print("Sender:   ", get_transaction_sender_from_json(transaction_details))
	#print("Receiver: ", get_transaction_receiver_from_json(transaction_details))
	#print("transaction_details", type(transaction_details))
	#for detail in transaction_details:
	#	print(detail, transaction_details.get(detail))

	'''
	print(transaction_details)
	print()
	print(transaction_details.get("vin"))
	print(transaction_details.get("vout"))
	print(transaction_details.get("ethereumSpecific"))
	print(transaction_details.get("humbug"))
	'''
	#print_nested_json(transaction_details)

	'''
	transactions_page = get_transactions_by_page("0x38daC0383F62Ce821C2b4618D655012789B15541", 1, 10)
	for tx in transactions_page:
		print(str(tx))
	'''

	#my_address = "0x38daC0383F62Ce821C2b4618D655012789B15541" # 6 transactions, 2 with ERC20 tokens
	my_address = "0x3D0F148FE58d592B9CCF5ab492C971D4954B5e7a"

	page_count = asyncio.run(get_transactions_number_of_pages(my_address, 10))
	print("page count: ", str(page_count))



	all_transactions = asyncio.run(get_transactions(my_address))
	input_addresses = []
	output_addresses = []
	print("Iterating through all transactions...")

	async def magic():
		counter = 0
		'''	
		for i in range(page_count):
			tasks.append(asyncio.create_task(get_transactions_by_page(address, i + 1, page_size)))
			#transactions = get_transactions_by_page(address, i + 1, page_size)
			#for tx in transactions:
			#	result.append(tx)
		for task in asyncio.as_completed(tasks):
			transactions = await task
			for tx in transactions:
				result.append(tx)
		'''
		tasks = []
		for tx in all_transactions:
			tasks.append(asyncio.create_task(get_transaction_details(tx)))

		for task in asyncio.as_completed(tasks):
			counter += 1
			print("fetching transaction "+str(counter)+" of "+str(len(all_transactions)))
			my_json = await task	
			print("transaction "+str(counter)+" fetched")		
			my_sender = get_transaction_sender_from_json(my_json)
			my_receiver = get_transaction_receiver_from_json(my_json)

			#print_nested_json(my_json)
			#print("sender: ", my_sender, ", receiver: ", my_receiver)

			if my_sender not in input_addresses:
				#print("adding "+my_sender+" as sender...")
				input_addresses.append(my_sender)

			if my_receiver not in output_addresses:
				#print("adding "+my_receiver+" as receiver...")
				output_addresses.append(my_receiver)

	asyncio.run(magic())

	print("Address: "+my_address)

	new_text = "Input addresses: \n\n"
	for my_addr in input_addresses:
	    new_text = new_text + my_addr + "\n"
	print(new_text)

	new_text = "Output addresses: \n\n"
	for my_addr in output_addresses:
	    new_text = new_text + my_addr + "\n"
	print(new_text)

	print("Input addresses: ", len(input_addresses))
	print("Output addresses: ", len(output_addresses))

	#print_nested_json()