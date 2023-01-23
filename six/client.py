from time import time
import requests
import base64
import ecdsa

import click

@click.command()
# @click.option('--count', default=1, help='Number of greetings.')
# @click.option('--name', prompt='Your name', help='The person to greet.')
@click.option('-host', help='host')
@click.option('-port', help='port')
@click.option('-msg', help='msg')
@click.option('-froma', help='from address')
@click.option('-toa', help='to address')
@click.option('-private', help='private_key')


def client(host, port, froma, toa, msg, private):
    if (host and port and froma and toa and msg and private):
        if len(private) == 64:
            signature, message = sign_ECDSA_msg(private)
            url = f"http://{host}:{port}/post"
            d = {"froma": froma, "toa": toa, "msg": msg, "signature": signature, "message": message}
            r = requests.post(url, data=d)
            print(r.text)
        else:
            print("Wrong address or key length! Verify and try again.")


def generate_ECDSA_keys():
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    private_key = sk.to_string().hex()
    vk = sk.get_verifying_key()
    public_key = vk.to_string().hex()
    public_key = base64.b64encode(bytes.fromhex(public_key))
    return public_key.decode(), private_key


def sign_ECDSA_msg(private_key):
    message = str(round(time()))
    bmessage = message.encode()
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
    signature = base64.b64encode(sk.sign(bmessage))
    return signature, message


if __name__ == '__main__':
    client()