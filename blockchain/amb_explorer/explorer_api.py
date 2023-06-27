''' 

Probably best to use blockbook as much as possible. 
Use explorer-api only if blockbook doesn't provide the information (i.E. types, roles, retire, onboarding, ...)
Careful: blockbook does not show the transactions for apollo_onboarding_address_hera_pool! 

Example URLs for BlockBook:
https://blockbook.ambrosus.io/api/v2/address/0xA80e0B8595a3739266e0Ba7d1Bf8a5AcB9F9d433?page=1&pageSize=50


Example URLs for explorer-api:
https://explorer-api.ambrosus.io/search/0xc155A7B612772ce4F4B7d7Dc0037b6133d4cD551 -> gives back information about the address, if it's a node, contract or whatever.



The explorer API can be used with the following categories and sorting methods: (but not sure )
	categories: apollos, atlases, accounts. 
	Sorting: totalBundles, balance, address, totalTx, 

	Categories: blocks
	Sorting:

	Categories: transactions
	Sorting: transactions, transfers, contracts, fees, validator_proxies, block_rewards, kycs, challenges, payouts
'''

import requests

url_base_explorer_api = "https://explorer-api.ambrosus.io/"
apollo_onboarding_address = "0xA80e0B8595a3739266e0Ba7d1Bf8a5AcB9F9d433"
apollo_deposit_address = "0x8687424E13b437834b6D6203e9A0f1EE084F9c25"
apollo_onboarding_address_hera_pool = "0x5d82Fb586886c49D80170F6440039b7f5FA302DE"

def get_from_explorer_api(category):
	answer = {}
	has_next = True
	next_hash = ""
	max_loops = 20 # explorer-api has a hard limit of 50 entries. 50 entries * 20 loops equals a maximum of 1000 entries.
	loops = 0
	while has_next:
		loops += 1
		my_URL = url_base_explorer_api + category + "?sort=totalBundles&next=" + next_hash + "&limit=50"
		response = requests.get(my_URL)
		if response.status_code == 200:
			content = list(response.json().values())
			data = content[0]		#contains data about the nodes
			next_field = content[2]  #contains information about if there's a next page 
		else:
			# API call failed
			print("Error:", response.status_code)
			raise Exception("Could not get " + my_URL)
		
		for node in data:
			my_node = node.get("address")
			my_stake = node.get("stake").get("ether")
			#myStatus = node.get("status")
			#if my_node not in answer and myStatus.lower() == "online":
			if my_node not in answer:
				answer[my_node] = my_stake
			else:
				#raise Exception("Node was already added! Aborting to avoid double entries.")
				print("Node was already added! Not adding it a second time!")


		if next_field.get("hasNext"):
			next_hash = next_field.get("next")
		else:
			has_next = False

		if loops >= max_loops and has_next:
			raise Exception("max_loops reached! Aborting in order to avoid spamming the API.")

	return answer
	


if __name__ == "__main__":

	# get a list with all apollo node addresses

	#apollos = getApollos(apollo_onboarding_address)
	#apollosHeraPool = getApollos(apollo_onboarding_address_hera_pool)
	apollos = getFromExplorerApi("apollos")

	for apollo in apollos:
		print(apollo + ": " + str(apollos.get(apollo)))

	#print("Apollos from Hera Staking found: ", len(apollosHeraPool))

	atlases = getFromExplorerApi("atlases")

	for atlas in atlases:
		print(atlas + ": " + str(atlases.get(atlas)))

	print("Apollos found: ", len(apollos))
	print("Atlases found: ", len(atlases))


	# get all(?) movements on the "apollo transfer through"-address (ATT): 0xA80e0B8595a3739266e0Ba7d1Bf8a5AcB9F9d433
	apollo_deposits = []

	# get a list with all atlas node addresses

	# with every apollo node address do:
		# If it is NOT an apollo from the staking program:
			# check ATT movements and calculate how much is still on there
