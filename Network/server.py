from fastapi import FastAPI, Depends
import requests

from Models import Blockchain
from .node import Node
from .serialisation import serialize_chain, deserialize_chain
from .auth import node_auth

app = FastAPI()

node: Node = None



def start_node(node_id: str, peers: list[str]):
    global node

    blockchain = Blockchain(difficulty=4, block_size=5)
    node = Node(node_id, blockchain)

    for p in peers:
        node.add_peer(p)

@app.post("/credential")
def add_credential(credential: dict):
    node.receive_credential(credential)
    broadcast_chain()
    return {"status": "credential added"}

@app.post("/chain", dependencies=[Depends(node_auth)])
def receive_chain(payload: dict):
    incoming_chain = deserialize_chain(payload["chain"])

    if node.should_accept_chain(incoming_chain):
        node.replace_chain(incoming_chain)
        return {"status": "chain replaced"}

    return {"status": "chain rejected"}

@app.get("/chain")
def get_chain():
    return {
        "length": len(node.blockchain.chain),
        "chain": serialize_chain(node.blockchain.chain)
    }

def broadcast_chain():
    data = {"chain": serialize_chain(node.blockchain.chain)}

    for peer in node.peers:
        try:
            requests.post(
                f"{peer}/chain",
                json=data,
                headers={
                    "X-Node-ID": node.node_id,
                    "X-Node-Token": "secretA"  # injected per node
                },
                timeout=2
            )
        except:
            pass

