import hashlib as hasher
from time import time

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
    block = make_a_block(index, timestamp, data, previous_hash)
    blockchain.append(block)


if __name__ == '__main__':
    # 生成一个初始块
    make_a_genesis_block()
    # 添加新的块
    add_a_block("hello")
    add_a_block("hi~")
    add_a_block("~")
    # 展示块
    for block in blockchain:
        print(block)
