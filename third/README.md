## 三、增加了部分查询功能

运行可以选择端口：

```cmd
python blockchain.py -p 8080
```

**查看全部区块**

```python
@app.route('/blocks/all', methods=['GET'])
def get_all_block():
    return jsonify(blockchain)
```

浏览器访问：

[http://localhost:8080/blocks/all](http://localhost:8080/blocks/all)

在浏览器里就可以看到区块链的json结果

输出：

```json
[
  {
    "data": "Genesis Block", 
    "hash": "dd37ac3028e6811960329225342bac25eef76d19956941d873130017854bfa68", 
    "index": 0, 
    "previous_hash": 0, 
    "timestamp": 1674472839720
  }, 
  {
    "data": "hello", 
    "hash": "e166dd24946e6e803e9bf95d7353875792aac97c4dd0c9dd1e9fbaf5a0db3598", 
    "index": 1, 
    "previous_hash": "dd37ac3028e6811960329225342bac25eef76d19956941d873130017854bfa68", 
    "timestamp": 1674472839720
  }, 
  {
    "data": "hi~", 
    "hash": "b4556d5672811d0ea2719c1e4009665a2c9b67d253cf0d021e534819c166547d", 
    "index": 2, 
    "previous_hash": "e166dd24946e6e803e9bf95d7353875792aac97c4dd0c9dd1e9fbaf5a0db3598", 
    "timestamp": 1674472839720
  }
]
```

**查看最新的区块**

```python
@app.route('/blocks/last',methods=['GET'])
def get_last_block():
    last_block = blockchain[len(blockchain)-1]
    return jsonify(last_block)
```

浏览器访问：

[http://localhost:8080/blocks/last](http://localhost:8080/blocks/last)

在浏览器里就可以看到区块链的json结果

```python
{
  "data": "hi~", 
  "hash": "b4556d5672811d0ea2719c1e4009665a2c9b67d253cf0d021e534819c166547d", 
  "index": 2, 
  "previous_hash": "e166dd24946e6e803e9bf95d7353875792aac97c4dd0c9dd1e9fbaf5a0db3598", 
  "timestamp": 1674472839720
}
```





















**查看全部区块**

```python
@app.route('/blocks/all', methods=['GET'])
def get_all_block():
    return jsonify(blockchain)
```

浏览器访问：

[http://localhost:8080](http://localhost:8080/)

你在浏览器里就可以看到区块链的json结果**查看全部区块**

```python
@app.route('/blocks/all', methods=['GET'])
def get_all_block():
    return jsonify(blockchain)
```

浏览器访问：

[http://localhost:8080](http://localhost:8080/)

你在浏览器里就可以看到区块链的json结果**查看全部区块**

```python
@app.route('/blocks/all', methods=['GET'])
def get_all_block():
    return jsonify(blockchain)
```

浏览器访问：

[http://localhost:8080](http://localhost:8080/)

你在浏览器里就可以看到区块链的json结果

输出：

```json
{'index': 0, 'timestamp': 1674471806772, 'data': 'Genesis Block', 'previous_hash': 0, 'hash': 'f93a0d2e18dc0b4ee39b70fe4f8199cc4cceb1d7a3a9dbe1305995f231e2b9f1'}

{'index': 1, 'timestamp': 1674471806772, 'data': 'hello', 'previous_hash': 'f93a0d2e18dc0b4ee39b70fe4f8199cc4cceb1d7a3a9dbe1305995f231e2b9f1', 'hash': 'c0716897f8c837c153d5348ff7af7d25417bac94c4a31b057785d2fe6134d46a'}

{'index': 2, 'timestamp': 1674471806772, 'data': 'hi~', 'previous_hash': 'c0716897f8c837c153d5348ff7af7d25417bac94c4a31b057785d2fe6134d46a', 'hash': '02cf3e7ccc483e2ee7cd1822ec59513bd2b123ceacd845d509b05c557ab2c1a1'}

{'index': 3, 'timestamp': 1674471806772, 'data': '~', 'previous_hash': '02cf3e7ccc483e2ee7cd1822ec59513bd2b123ceacd845d509b05c557ab2c1a1', 'hash': 'a0784c9491c2a5fe939506a1f24b3b2b8d5ed6ed95018d468f36aeccbea88ab6'}
```

