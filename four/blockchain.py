# 同步区块

import hashlib as hasher
from time import time
from flask import Flask, jsonify, render_template
from argparse import ArgumentParser
import requests


blockchain = []
nodes = []

def add_node(node):
    nodes.append(node)

#返回自身区块链高度
def get_height():
    last_block = blockchain[len(blockchain)-1]
    last_block_index = last_block["index"]
    return last_block_index

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


#验证区块链
def validate(blocks):
    bool = True
    # 上一个区块
    previous_index = 0
    previous_hash = 0
    for block in blocks:
        # 当前的块
        index = block["index"]
        hash = block["hash"]
        if (index > 0):
            # 如果index是衔接的, 如果上一个区块的当前hash和当前区块的上一个hash值能对上
            if (previous_index == index-1 and previous_hash == block["previous_hash"]):
                # 把当前的变为上一个
                previous_index = index
                previous_hash = hash
            else:
                bool = False
        elif (index == 0):
            previous_index = index
            previous_hash = hash
            pass
    return bool


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/addblock/<string:msg>',methods=['GET'])
def add_blockchain(msg):
    add_a_block(msg)
    return jsonify(blockchain)


@app.route('/blocks/last',methods=['GET'])
def get_last_block():
    last_block = blockchain[len(blockchain)-1]
    return jsonify(last_block)


@app.route('/blocks/<int:index>',methods=['GET'])
def get_block(index):
    if(len(blockchain)>=index):
        block = blockchain[index]
        return jsonify(block)
    else:
        return jsonify({"error":"noindex"})


@app.route('/blocks/<int:from_index>/<int:to_index>',methods=['GET'])
def get_block_from_to(from_index, to_index):
    blocks=[]
    if(len(blockchain)>from_index and len(blockchain)>to_index and to_index>=from_index):
        for i in range(from_index,to_index+1):
            block=blockchain[i]
            blocks.append(block)
        return jsonify(blocks)
    else:
        return jsonify({"error":"noindex"})

@app.route('/blocks/all',methods=['GET'])
def get_all_block():
    return jsonify(blockchain)

#查看区块链高度
@app.route('/blocks/height',methods=['GET'])
def get_block_height():
    last_block = blockchain[len(blockchain)-1]
    print(last_block)
    return jsonify(last_block["index"])

#查看节点
@app.route('/nodes',methods=['GET'])
def get_get_nodes():
    print(nodes)
    return jsonify(nodes)

#添加节点
@app.route('/nodes/add/<string:ip>/<int:port>',methods=['GET'])
def add_nodes(ip, port):
    node = {"ip": ip, "port": port}
    # 确保不重复添加
    if node not in nodes:
        nodes.append(node)
    print(node)
    return jsonify(nodes)

#同步区块
@app.route('/blocks/sync',methods=['GET'])
def blocks_sync():
    syn = False
    for node in nodes:
        ip = node["ip"]
        port = node["port"]
        url_height = f"http://{ip}:{port}/blocks/height"
        url_all = f"http://{ip}:{port}/blocks/all"
        # 尝试去同步
        try:
            # 尝试获得对方高度
            print(url_height)
            print(url_all)
            r_height = requests.get(url_height)
            height = int(r_height.json())
            print(height)
            self_index = get_height()
            print(self_index)
            # 如果对方的比自己的大
            if height > self_index:
                # 请求所有的blockchain信息
                r_blocks_all = requests.get(url_all)
                blocks = r_blocks_all.json()
                # 把对方的blockchain赋值自己的blokchain
                # 这里有个问题，即区块链没有进行验证，以后会补上。
                is_validate = validate(blocks)
                # 把对方的blockchain赋值自己的blokchain
                if (is_validate):
                    blockchain.clear()
                    for block in blocks:
                        blockchain.append(block)
                # blockchain.clear()
                # for block in blocks:
                #     blockchain.append(block)
                syn = True
        except:
            return jsonify("error")
    return jsonify(f"syn: {syn}")


if __name__ == '__main__':
    make_a_genesis_block()
    add_a_block("hello")
    add_a_block("hi~")
    add_a_block("~")

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8080, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    # app.run(debug=True, host='0.0.0.0', port=port)
    app.run(host='0.0.0.0', port=port)
