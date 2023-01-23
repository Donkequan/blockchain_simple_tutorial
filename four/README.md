## 四、增加了节点同步的区块链

增加一个list，保存节点。

```
nodes=[]
```

为了方便同步数据，我们要增加一个获知区块链高度的接口

```python
@app.route('/blocks/height',methods=['GET'])
def get_block_height():
    last_block = blockchain[len(blockchain)-1]
    print(last_block)
    return jsonify(last_block["index"])
```

访问：http://localhost:8080/blocks/height

这样，即可得到区块链的高度。当目标节点的区块链高度大于本地区块链高度时，才去同步。

**查看节点**

```python
@app.route('/nodes',methods=['GET'])
def get_get_nodes():
    print(nodes)
    return jsonify(nodes)
```

访问：http://localhost:8080/nodes



**添加节点**

```python
@app.route('/nodes/add/<string:ip>/<int:port>',methods=['GET'])
def add_nodes(ip, port):
    node = {"ip": ip, "port": port}
    # 确保不重复添加
    if node not in nodes:
        nodes.append(node)
    print(node)
    return jsonify(nodes)
```

访问：http://localhost:8080/nodes/add/localhost/9000

浏览器输出：

```json
[
  {
    "ip": "localhost",
    "port": 9000
  }
]
```



测试：

1. 启动三个节点

   ```cmd
   python blockchain.py -p 8080
   python blockchain.py -p 8081
   python blockchain.py -p 8083
   ```

2. 在8080的节点中添加个节点8081和8082

   ```url
   浏览器访问
   http://localhost:8080/nodes/add/localhost/8081
   http://localhost:8080/nodes/add/localhost/8083
   ```

3. 查看8080同步的节点

   ```
   http://localhost:8080/nodes
   ```

   输出：

   ```json
   [{"ip":"localhost","port":8081},{"ip":"localhost","port":8083}]
   ```

4. 在8081的区块链中加一个块

   ```
   http://localhost:8081/addblock/hhhhhhhh
   ```

5. 在8080节点中同步

   ```
   http://localhost:8080/blocks/sync
   ```

 6. 查看块更新

    ```
    http://localhost:8080/blocks/all
    ```

    输出：

    ```json
    [{"data":"Genesis Block","hash":"fc37b534d1f5ce36b791d7d93febac19fd5486974542cd87813e7f52c372b751","index":0,"previous_hash":0,"timestamp":1674473970879},{"data":"hello","hash":"cdba97b0da9f1029124f95514fb56047761de3c477706985b822c57efbdbc0b3","index":1,"previous_hash":"fc37b534d1f5ce36b791d7d93febac19fd5486974542cd87813e7f52c372b751","timestamp":1674473970879},{"data":"hi~","hash":"447986c9af1cc0cff36d4a44865b3df8d2fc4e5c850bd3ffb235cc293cafb53a","index":2,"previous_hash":"cdba97b0da9f1029124f95514fb56047761de3c477706985b822c57efbdbc0b3","timestamp":1674473970879},{"data":"~","hash":"9e4c84e663c97c9d21ca67c435030f8badd109fe1e49c4db8001e537cb009c44","index":3,"previous_hash":"447986c9af1cc0cff36d4a44865b3df8d2fc4e5c850bd3ffb235cc293cafb53a","timestamp":1674473970879},{"data":"hhhhhhhh","hash":"2007ab84bf528bc3d798873ec2f28f231ee78b3ed2dfae8d54ee33b5b363f5d1","index":4,"previous_hash":"9e4c84e663c97c9d21ca67c435030f8badd109fe1e49c4db8001e537cb009c44","timestamp":1674474092981}]
    ```

    
