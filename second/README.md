## 二、使用了flask构建web界面的区块链

加入了flask做一个web站点

运行方法：

```cmd
python blockchain.py
```

**查看块**

```python
@app.route('/',methods=['GET'])
def get_blockchain():
    # 转化为json输出
    return jsonify(blockchain)
```

浏览器访问：

[http://localhost:8080](http://localhost:8080/)

你在浏览器里就可以看到区块链的json结果

输出：

```json
[
  {
    "data": "Genesis Block", 
    "hash": "134664223835198291c3a3b29a4154b00c5e3faa71ae645b6936d45822ba414c", 
    "index": 0, 
    "previous_hash": 0, 
    "timestamp": 1674472194689
  }, 
  {
    "data": "hello", 
    "hash": "c6b41ffc9b52e006caf3ec6de65722d6f575046270b2984f150f4af8b30d16ca", 
    "index": 1, 
    "previous_hash": "134664223835198291c3a3b29a4154b00c5e3faa71ae645b6936d45822ba414c", 
    "timestamp": 1674472194689
  }, 
  {
    "data": "hi~", 
    "hash": "78b9eb5134956a2d0df48924483ba0f0ba37921827931fd52a03436b431ab5dc", 
    "index": 2, 
    "previous_hash": "c6b41ffc9b52e006caf3ec6de65722d6f575046270b2984f150f4af8b30d16ca", 
    "timestamp": 1674472194689
  }
]
```

**添加块**

```python
@app.route('/addblock/<string:msg>',methods=['GET'])
def add_blockchain(msg):
    add_a_block(msg)
    return jsonify(blockchain)
```

浏览器访问：

http://localhost:8080/addblock/hhhhhh

输出：

```json
[
  {
    "data": "Genesis Block", 
    "hash": "134664223835198291c3a3b29a4154b00c5e3faa71ae645b6936d45822ba414c", 
    "index": 0, 
    "previous_hash": 0, 
    "timestamp": 1674472194689
  }, 
  {
    "data": "hello", 
    "hash": "c6b41ffc9b52e006caf3ec6de65722d6f575046270b2984f150f4af8b30d16ca", 
    "index": 1, 
    "previous_hash": "134664223835198291c3a3b29a4154b00c5e3faa71ae645b6936d45822ba414c", 
    "timestamp": 1674472194689
  }, 
  {
    "data": "hi~", 
    "hash": "78b9eb5134956a2d0df48924483ba0f0ba37921827931fd52a03436b431ab5dc", 
    "index": 2, 
    "previous_hash": "c6b41ffc9b52e006caf3ec6de65722d6f575046270b2984f150f4af8b30d16ca", 
    "timestamp": 1674472194689
  }, 
  {
    "data": "hhhhhh", 
    "hash": "a978a9a1c174f4e04b49306a064a75e08615092ac36049aa6e05a7fb7b7c76d1", 
    "index": 3, 
    "previous_hash": "78b9eb5134956a2d0df48924483ba0f0ba37921827931fd52a03436b431ab5dc", 
    "timestamp": 1674472322215
  }
]
```

