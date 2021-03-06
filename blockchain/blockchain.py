import datetime
import hashlib
import json
import requests
from urllib.parse import urlparse


class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(nonce=1, previous_hash='0')
        self.nodes = set()

    def create_block(self, nonce, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'nonce': nonce,
            'previous_hash': previous_hash,
            'transactions': self.transactions
        }
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    @staticmethod
    def proof_of_work(previous_nonce):
        new_nonce = 1
        check_nonce = False
        while check_nonce is False:
            """
            - the code inside the str() is the algo, make it as hard as you want.
            
            - the hash_operation algorithm we pass in must be non-symmetrical
            such that if the order of operation were to be reversed it would’t result in the same value.
            For instance, a+b is equal to b+a, but a-b is not equal to b-a.

            - we can take advantage of the timestamp to make the algo harder. Read here:
            https://www.section.io/engineering-education/an-introduction-to-blockchain-architecture/#mining-and-proof-of-work
            """
            hash_operation = hashlib.sha256(str(new_nonce ** 2 - previous_nonce ** 2).encode()).hexdigest()
            # the more leading zeros we require the more difficult it will be to mine a block.
            if hash_operation[:4] == '0000':
                check_nonce = True
            else:
                new_nonce += 1
        return new_nonce

    # generate a hash of an entire block
    @staticmethod
    def hash(block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            current_block = chain[block_index]
            if current_block['previous_hash'] != self.hash(previous_block):
                return False
            previous_nonce = previous_block['nonce']
            current_nonce = current_block['nonce']
            hash_operation = hashlib.sha256(str(current_nonce ** 2 - previous_nonce ** 2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = current_block
            block_index += 1
        return True

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append(
            {
                'sender': sender,
                'receiver': receiver,
                'amount': amount,
                'time': str(datetime.datetime.now())
             }
        )
        # todo: check this get_last_block.
        previous_block = self.get_last_block()
        return previous_block['index'] + 1

    def get_last_block(self):
        return self.chain[-1]

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/blockchain/get_chain/')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
