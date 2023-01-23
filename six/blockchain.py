# 区块链浏览器

import hashlib as hasher
from time import time
import json
from flask import Flask, jsonify, render_template,request
from argparse import ArgumentParser
import requests
import ecdsa
import base64


blockchain = []
nodes=[]

def add_node(node):
    nodes.append(node)

#返回自身区块链高度
def get_height():
    last_block = blockchain[len(blockchain)-1]
    last_block_index = last_block["index"]
    return last_block_index

# 输入block header生成hash
# def hash(index, data, timestamp, previous_hash):
#     sha = hasher.sha256()
#     sha.update("{0}{1}{2}{3}".format(index, data, timestamp, previous_hash).encode("utf8"))
#     return sha.hexdigest()

def hash(index,consignor,consignee,memo,timestamp,previous_hash):
    sha = hasher.sha256()
    sha.update("{0}{1}{2}{3}{4}{5}".format(index,consignor,consignee,memo,timestamp,previous_hash).encode("utf8"))
    return sha.hexdigest()

# 生成一个block字典
# def make_a_block(index, timestamp, data, previous_hash):
#     block = {}
#     block["index"] = index
#     block["timestamp"] = timestamp
#     block["data"] = data
#     block["previous_hash"] = previous_hash
#     block["hash"] = hash(index, data, timestamp, previous_hash)
#     return block

# 新建一个区块
# consignor:寄件人
# consignee：收件人
# msg:备注信息
def make_a_block(index,timestamp,consignor,consignee,msg,previous_hash):
    block={}
    block["index"]=index
    block["timestamp"]=timestamp
    block["consignor"]=consignor
    block["consignee"]=consignee
    block["msg"]=msg
    block["previous_hash"]=previous_hash
    block["hash"]=hash(index,consignor,consignee,msg,timestamp,previous_hash)
    return block


# def add_a_block(data):
#     last_block = blockchain[len(blockchain)-1]
#     index = last_block["index"]+1
#     timestamp = int(round(time() * 1000))
#     previous_hash = last_block["hash"]
#     blockchain.append(make_a_block(index, timestamp, data, previous_hash))

def add_a_block(consignor, consignee, msg):
    last_block = blockchain[len(blockchain)-1]
    index = last_block["index"]+1
    timestamp = int(round(time() * 1000))
    previous_hash = last_block["hash"]
    blockchain.append(make_a_block(index, timestamp, consignor, consignee, msg, previous_hash))


# def make_a_genesis_block():
#     index = 0
#     timestamp = int(round(time() * 1000))
#     data = "Genesis Block"
#     previous_hash = 0
#     # 生成一个block字典
#     block = make_a_block(index, timestamp, data, previous_hash)
#     blockchain.append(block)

def make_a_genesis_block():
    index=0
    timestamp=int(round(time() * 1000))
    consignor = 0
    consignee = 0
    msg="Genesis Block"
    previous_hash=0
    blockchain.append(make_a_block(index,timestamp,consignor,consignee,msg,previous_hash))


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


def validate_signature(public_key, signature, message):
    public_key = (base64.b64decode(public_key)).hex()
    signature = base64.b64decode(signature)
    vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key), curve=ecdsa.SECP256k1)
    try:
        return vk.verify(signature, message.encode())
    except:
        return False


app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('index.html')

@app.route('/',methods=['POST','GET'])
def home():
    # 查找
    if request.method == 'POST':
        address=request.form.get('address')
        out_logs=[]
        in_logs=[]
        for i in range(1,len(blockchain)):
            block=blockchain[i]
            if address == block["consignor"]:
                out_logs.append(block)
            if address == block["consignee"]:
                in_logs.append(block)
        return render_template('index.html',out_logs=out_logs,in_logs=in_logs)
    if request.method == 'GET':
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
        try:
            print(url_height)
            print(url_all)
            r_height = requests.get(url_height)
            height = int(r_height.json())
            print(height)
            self_index = get_height()
            print(self_index)
            if height > self_index:
                r_blocks_all = requests.get(url_all)
                blocks = r_blocks_all.json()
                is_validate = validate(blocks)
                if (is_validate):
                    blockchain.clear()
                    for block in blocks:
                        blockchain.append(block)
                syn = True
        except:
            return jsonify("error")
    return jsonify(f"syn: {syn}")


#验证
@app.route('/validate',methods=['GET'])
def blocks_validate():
    return jsonify(validate(blockchain))


#信息上链
# @app.route('/post',methods=['POST'])
# def add_block():
#     if request.method == 'POST':
#         from_address = request.form.get('from_address')
#         to_address = request.form.get('to_address')
#         msg = request.form.get('msg')
#         signature = request.form.get('signature')
#         message = request.form.get('message')
#         if validate_signature(from_address, signature, message):
#             data = {
#                 "from": from_address,
#                 "to": to_address,
#                 "msg": msg
#             }
#             add_a_block(data)
#             return jsonify(blockchain)
@app.route('/post',methods=['POST'])
def post():
    if request.method == 'POST':
        consignor = request.form.get('froma')
        consignee = request.form.get('toa')
        msg=request.form.get('msg')
        signature = request.form.get('signature')
        message = request.form.get('message')
        if validate_signature(consignor, signature, message):
            add_a_block(consignor,consignee,msg)
            return jsonify(blockchain)
        else:
            return jsonify("error")


if __name__ == '__main__':
    make_a_genesis_block()

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8080, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(debug=True, host='0.0.0.0', port=port)
