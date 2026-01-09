from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes


def generate_issuer_keys():
    private_key = ec.generate_private_key(ec.SECP256K1())
    public_key = private_key.public_key()
    return private_key, public_key

def sign_data(private_key, data: str):
    signature = private_key.sign(
        data.encode(),
        ec.ECDSA(hashes.SHA256())
    )
    return signature.hex()

def verify_signature(public_key, data: str, signature_hex: str):
    try:
        public_key.verify(
            bytes.fromhex(signature_hex),
            data.encode(),
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except:
        return False
