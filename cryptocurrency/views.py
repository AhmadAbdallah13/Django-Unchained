import json
from uuid import uuid4
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from blockchain.views import blockchain


# Creating an address for the node running our server
node_address = str(uuid4()).replace('-', '')
root_node = 'e36f0158f0aed45b3bc755dc52ed4560d'


# Adding a new transaction to the Blockchain
# @csrf_exempt
class AddTransaction(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        received_json = json.loads(request.body)
        transaction_keys = ['sender', 'receiver', 'amount']
        if not all(key in received_json for key in transaction_keys):
            return 'Some elements of the transaction are missing', HttpResponse(status=400)
        index = blockchain.add_transaction(
            received_json['sender'],
            received_json['receiver'],
            received_json['amount']
        )
        response = {'message': f'This transaction will be added to Block {index}'}
        return JsonResponse(response)


# Connecting new nodes
# @csrf_exempt
class ConnectNode(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        received_json = json.loads(request.body)
        nodes = received_json.get('nodes')
        if nodes is None:
            return "No node", HttpResponse(status=400)
        for node in nodes:
            blockchain.add_node(node)
        response = {
            'message': 'All the nodes are now connected. The Sudocoin Blockchain now contains the following nodes:',
            'total_nodes': list(blockchain.nodes)
        }
        return JsonResponse(response)


# Replacing the chain by the longest chain if needed
# @csrf_exempt
class ReplaceChain(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        is_chain_replaced = blockchain.replace_chain()
        if is_chain_replaced:
            response = {
                'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                'new_chain': blockchain.chain
            }
        else:
            response = {
                'message': 'All good. The chain is the largest one.',
                'actual_chain': blockchain.chain
            }
        return JsonResponse(response)
