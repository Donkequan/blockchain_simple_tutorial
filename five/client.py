from time import time
import requests
import base64
import ecdsa

import click
import json
import os

# 上传块
# python .\client.py -action -s -froma Vb0IaNd8tVffF3V6PzPrUT+OznDYLfc/6sJ167KfdBJu6IsX/Oxq2qfiIOeQHEzhovqSJNqg/f3/P/EKCaJDkQ== -toa 4JaS/gUOII5soTL92K+dGSZ+bnHFxXDspSJg4n8+xn3Nn0CIrYj5RQBaOUgc0j4wgOFSWPQbmG2C+wN0tYIvlA== -private b327ad7c845f13c808157ac28ec9ac39a7f779aecdd47ba330d3598e7d38f251 -msg "hhh"

@click.command()
@click.option('-action', help='action: n/s')
@click.option('-msg', help='msg')
@click.option('-froma', help='from address')
@click.option('-toa', help='to address')
@click.option('-private', help='private_key')


def client(action, msg, froma, toa, private):
    if action == "g":
        public_key, private_key = generate_ECDSA_keys()
        # 使用 click.echo 进行输出是为了获得更好的兼容性
        click.echo("")
        click.echo("address:{0}\n".format(public_key))
        click.echo("private_key:{0}\n".format(private_key))
    if action == "s":
        if (msg and froma and toa and private):
            print(send_transaction(froma, toa, msg, private))


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


def send_transaction(from_address, to_address, msg, private_key):
    if len(private_key) == 64:
        # message就是时间戳
        signature, message = sign_ECDSA_msg(private_key)
        url = "http://localhost:8080/post"
        d = {"from_address": from_address, "to_address": to_address, "msg": msg, "signature":signature, "message":message}
        r = requests.post(url, data=d)
        return r.text
    else:
        return ("Wrong address or key length! Verify and try again.")


if __name__ == '__main__':
    client()

    # from
    # address: Vb0IaNd8tVffF3V6PzPrUT+OznDYLfc/6sJ167KfdBJu6IsX/Oxq2qfiIOeQHEzhovqSJNqg/f3/P/EKCaJDkQ==
    # private_key: b327ad7c845f13c808157ac28ec9ac39a7f779aecdd47ba330d3598e7d38f251

    # to
    # address: 4JaS/gUOII5soTL92K+dGSZ+bnHFxXDspSJg4n8+xn3Nn0CIrYj5RQBaOUgc0j4wgOFSWPQbmG2C+wN0tYIvlA==
    # private_key: bb70c04d2d8020992cec13c4d14b945ae2d12255abc96042dfc512feeeac0909
