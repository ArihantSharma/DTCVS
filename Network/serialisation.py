from Models.block import Block

def serialize_chain(chain: list[Block]):
    return [
        {
            "index": b.index,
            "timestamp": b.timestamp,
            "credentials": b.credentials,
            "prev_hash": b.prev_hash,
            "nonce": b.nonce,
            "hash": b.hash
        }
        for b in chain
    ]

def deserialize_chain(data):
    chain = []

    for b in data:
        block = Block(
            index=b["index"],
            timestamp=b["timestamp"],
            credentials=b["credentials"],
            prev_hash=b["prev_hash"]
        )
        block.nonce = b["nonce"]
        block.hash = b["hash"]
        chain.append(block)

    return chain
