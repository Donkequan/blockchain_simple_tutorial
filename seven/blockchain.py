# 解耦

from flask import Flask, jsonify, render_template,request
from argparse import ArgumentParser
import requests

from block import *

block_tool = BlockchainTool()

app = Flask(__name__)


@app.route('/',methods=['POST','GET'])
def home():
    # 查找
    if request.method == 'POST':
        address=request.form.get('address')
        out_logs = []
        in_logs = []
        for i in range(1, len(block_tool.blockchain)):
            block = block_tool.blockchain[i]
            if address == block.consignor:
                out_logs.append(block)
            if address == block.consignee:
                in_logs.append(block)
        return render_template('index.html', out_logs=out_logs, in_logs=in_logs)
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/say/<string:msg>',methods=['GET'])
def add_blockchain(msg):
    block_tool.add_a_block(msg)
    return jsonify(block_tool.json(block_tool.blockchain))


@app.route('/blocks/last',methods=['GET'])
def get_last_block():
    last_block = block_tool.blockchain[len(block_tool.blockchain)-1]
    return jsonify(last_block.to_dic())


@app.route('/blocks/<int:index>',methods=['GET'])
def get_block(index):
    if(len(block_tool.blockchain)>=index):
        block = block_tool.blockchain[index]
        return jsonify(block.to_dic())
    else:
        return jsonify({"error":"noindex"})


@app.route('/blocks/<int:from_index>/<int:to_index>',methods=['GET'])
def get_block_from_to(from_index, to_index):
    blocks=[]
    if(len(block_tool.blockchain)>from_index and len(block_tool.blockchain)>to_index and to_index>=from_index):
        for i in range(from_index,to_index+1):
            block=block_tool.blockchain[i]
            blocks.append(block)
        return jsonify(blocks)
    else:
        return jsonify({"error":"noindex"})

@app.route('/blocks/all',methods=['GET'])
def get_all_block():
    return jsonify(block_tool.json(block_tool.blockchain))

#查看区块链高度
@app.route('/blocks/height',methods=['GET'])
def get_block_height():
    last_block = block_tool.blockchain[len(block_tool.blockchain)-1]
    print(last_block)
    return jsonify(last_block["index"])

#查看节点
@app.route('/nodes',methods=['GET'])
def get_get_nodes():
    print(block_tool.nodes)
    return jsonify(block_tool.json(block_tool.nodes))

#添加节点
@app.route('/nodes/add/<string:ip>/<int:port>',methods=['GET'])
def add_nodes(ip, port):
    node = {"ip": ip, "port": port}
    # 确保不重复添加
    if node not in block_tool.nodes:
        block_tool.nodes.append(node)
    print(node)
    return jsonify(block_tool.json(block_tool.nodes))

#同步区块
@app.route('/blocks/sync',methods=['GET'])
def blocks_sync():
    syn = False
    for node in block_tool.nodes:
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
            self_index = block_tool.get_height()
            print(self_index)
            if height > self_index:
                r_blocks_all = requests.get(url_all)
                blocks = r_blocks_all.json()
                is_validate = block_tool.validate(blocks)
                if (is_validate):
                    block_tool.blockchain.clear()
                    for block in blocks:
                        block_tool.blockchain.append(block)
                syn = True
        except:
            return jsonify("error")
    return jsonify(f"syn: {syn}")

#验证
@app.route('/validate',methods=['GET'])
def blocks_validate():
    return jsonify(block_tool.validate(block_tool.blockchain))


#信息上链
@app.route('/post', methods=['POST'])
def post():
    if request.method == 'POST':
        consignor = request.form.get('froma')
        consignee = request.form.get('toa')
        msg=request.form.get('msg')
        signature = request.form.get('signature')
        message = request.form.get('message')
        if block_tool.validate_signature(consignor, signature, message):
            block_tool.add_a_block(consignor, consignee, msg)
            return jsonify(block_tool.json(block_tool.blockchain))
        else:
            return jsonify("error")


if __name__ == '__main__':
    block_tool.make_a_genesis_block()

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8080, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    # app.run(debug=True, host='0.0.0.0', port=port)
    app.run(host='0.0.0.0', port=port)
