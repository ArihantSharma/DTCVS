import sys
import uvicorn
from Network.server import app, start_node

node_id = sys.argv[1]
port = int(sys.argv[2])
peers = sys.argv[3:]

start_node(node_id, peers)

uvicorn.run(app, host="0.0.0.0", port=port)
