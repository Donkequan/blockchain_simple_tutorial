import base64
import ecdsa


def generate_ECDSA_keys():
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) #this is your sign (private key)
    private_key = sk.to_string().hex() #convert your private key to hex
    vk = sk.get_verifying_key() #this is your verification key (public key)
    public_key = vk.to_string().hex()
    public_key = base64.b64encode(bytes.fromhex(public_key))
    return public_key.decode(), private_key


if __name__ == '__main__':
    public_key, private_key = generate_ECDSA_keys()
    print(f"address:{public_key}")
    print(f"private_key:{private_key}")
