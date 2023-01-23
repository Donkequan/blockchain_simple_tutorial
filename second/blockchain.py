# 加了flask

import hashlib as hasher
from time import time
from flask import Flask, jsonify

blockchain = []

# 输入block header生成hash
def hash(index, data, timestamp, previous_hash):
    sha = hasher.sha256()
    sha.update("{0}{1}{2}{3}".format(index, data, timestamp, previous_hash).encode("utf8"))
    return sha.hexdigest()

# 生成一个block字典
def make_a_block(index, timestamp, data, previous_hash):
    block = {}
    block["index"] = index
    block["timestamp"] = timestamp
    block["data"] = data
    block["previous_hash"] = previous_hash
    block["hash"] = hash(index, data, timestamp, previous_hash)
    return block


def add_a_block(data):
    last_block = blockchain[len(blockchain)-1]
    index = last_block["index"]+1
    timestamp = int(round(time() * 1000))
    previous_hash = last_block["hash"]
    blockchain.append(make_a_block(index, timestamp, data, previous_hash))


def make_a_genesis_block():
    index = 0
    timestamp = int(round(time() * 1000))
    data = "Genesis Block"
    previous_hash = 0
    # 生成一个block字典
    block = make_a_block(index, timestamp, data, previous_hash)
    blockchain.append(block)


app = Flask(__name__)

@app.route('/',methods=['GET'])
def get_blockchain():
    # 转化为json输出
    return jsonify(blockchain)

@app.route('/addblock/<string:msg>',methods=['GET'])
def add_blockchain(msg):
    add_a_block(msg)
    return jsonify(blockchain)


if __name__ == '__main__':
    make_a_genesis_block()
    add_a_block("hello")
    add_a_block("hi~")
    app.run(debug=True, host='0.0.0.0', port=8080)
