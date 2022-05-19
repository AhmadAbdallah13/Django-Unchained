from django.http import JsonResponse
from rest_framework.views import APIView

from blockchain.blockchain import Blockchain


# Creating our Blockchain
blockchain = Blockchain()


# Mining a new block
class MineBlock(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
        previous_block = blockchain.get_previous_block()
        previous_nonce = previous_block['nonce']
        nonce = blockchain.proof_of_work(previous_nonce)
        previous_hash = blockchain.hash(previous_block)
        block = blockchain.create_block(nonce, previous_hash)
        response = {
            'message': 'Congratulations, you just mined a block!',
            'index': block['index'],
            'timestamp': block['timestamp'],
            'nonce': block['nonce'],
            'previous_hash': block['previous_hash']
        }
        return JsonResponse(response)


# Getting the full Blockchain
class GetChain(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
        response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain)
        }
        return JsonResponse(response)


# Checking if the Blockchain is valid
class CheckBlockchain(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
        is_valid = blockchain.is_chain_valid(blockchain.chain)
        if is_valid:
            response = {'message': 'All good. The Blockchain is valid.'}
        else:
            response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
        return JsonResponse(response)
