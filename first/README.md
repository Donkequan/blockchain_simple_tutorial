## 一、最简单的区块链

最简单的区块链仅仅有块结构：

1. index 块索引
2. previous_hash上一个块的hash
3. hash 本块的hash
4. timestamp时间戳
5. data 内此处可以放内容

运行方法：

```cmd
python blockchain.py
```

运行：

1. 生成一个初始块

   ```python
   def make_a_genesis_block():
       index = 0
       timestamp = int(round(time() * 1000))
       data = "Genesis Block"
       previous_hash = 0
       block = make_a_block(index, timestamp, data, previous_hash)
       blockchain.append(block)
   ```

2. 添加新块

   ```python
   def add_a_block(data):
       last_block = blockchain[len(blockchain)-1]
       index = last_block["index"]+1
       timestamp = int(round(time() * 1000))
       previous_hash = last_block["hash"]
       blockchain.append(make_a_block(index, timestamp, data, previous_hash))
   ```

3. 展示块内容

输出：

```json
{'index': 0, 'timestamp': 1674471806772, 'data': 'Genesis Block', 'previous_hash': 0, 'hash': 'f93a0d2e18dc0b4ee39b70fe4f8199cc4cceb1d7a3a9dbe1305995f231e2b9f1'}

{'index': 1, 'timestamp': 1674471806772, 'data': 'hello', 'previous_hash': 'f93a0d2e18dc0b4ee39b70fe4f8199cc4cceb1d7a3a9dbe1305995f231e2b9f1', 'hash': 'c0716897f8c837c153d5348ff7af7d25417bac94c4a31b057785d2fe6134d46a'}

{'index': 2, 'timestamp': 1674471806772, 'data': 'hi~', 'previous_hash': 'c0716897f8c837c153d5348ff7af7d25417bac94c4a31b057785d2fe6134d46a', 'hash': '02cf3e7ccc483e2ee7cd1822ec59513bd2b123ceacd845d509b05c557ab2c1a1'}

{'index': 3, 'timestamp': 1674471806772, 'data': '~', 'previous_hash': '02cf3e7ccc483e2ee7cd1822ec59513bd2b123ceacd845d509b05c557ab2c1a1', 'hash': 'a0784c9491c2a5fe939506a1f24b3b2b8d5ed6ed95018d468f36aeccbea88ab6'}
```

