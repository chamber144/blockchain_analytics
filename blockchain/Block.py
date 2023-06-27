class Block:
	def __init__(self, block_number = none, block_hash = none):
		if block_number is none and block_hash is none:
			raise Exception("You need to specify block_number or block_hash to create a Block-Object!")

		if block_number is not None:
			self.block_number = block_number
		if block_hash is not None:
			self.block_hash = block_hash

