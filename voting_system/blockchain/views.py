from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .blockchain import Blockchain
import json

# Initialize blockchain
blockchain = Blockchain()

@require_http_methods(["GET"])
def mine(request):
    last_proof = blockchain.last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    previous_hash = blockchain.hash(blockchain.last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': 'New block forged',
        'index': block['index'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'votes': block['votes'],
    }
    return JsonResponse(response)

@csrf_exempt
@require_http_methods(["POST"])
def vote(request):
    values = json.loads(request.body)
    required = ['voter_id', 'candidate']
    if not all(key in values for key in required):
        return JsonResponse({'message': 'Missing values'}, status=400)

    index = blockchain.new_vote(values['voter_id'], values['candidate'])
    response = {
        'message': f'Vote will be added to Block {index}'
    }
    return JsonResponse(response)

@require_http_methods(["GET"])
def full_chain(request):
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return JsonResponse(response)

@require_http_methods(["GET"])
def votes(request):
    votes = []
    for block in blockchain.chain:
        votes.extend(block['votes'])
    return JsonResponse(votes, safe=False)

