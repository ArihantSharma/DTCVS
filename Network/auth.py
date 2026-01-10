from fastapi import Request, HTTPException

TRUSTED_NODES = {
    "node-A": "secretA",
    "node-B": "secretB"
}

async def node_auth(request: Request):
    node_id = request.headers.get("X-Node-ID")
    token = request.headers.get("X-Node-Token")

    if not node_id or not token:
        raise HTTPException(status_code=401, detail="Missing node auth")

    if TRUSTED_NODES.get(node_id) != token:
        raise HTTPException(status_code=403, detail="Invalid node credentials")
