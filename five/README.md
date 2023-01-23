## 五、增加了签名

客户端可以生成地址，然后使用私钥签名，签名的内容经过服务端检查，可以上链。

生成两个地址和私钥，一个发送者一个接收者

```
python client.py -action g
python client.py -action g
```

运行服务器：

```cmd
python blockchain.py
```

发送交易

```cmd
python client.py -action s -froma Vb0IaNd8tVffF3V6PzPrUT+OznDYLfc/6sJ167KfdBJu6IsX/Oxq2qfiIOeQHEzhovqSJNqg/f3/P/EKCaJDkQ== -toa 4JaS/gUOII5soTL92K+dGSZ+bnHFxXDspSJg4n8+xn3Nn0CIrYj5RQBaOUgc0j4wgOFSWPQbmG2C+wN0tYIvlA== -private b327ad7c845f13c808157ac28ec9ac39a7f779aecdd47ba330d3598e7d38f251 -msg "hhh"
```

返回

```json
[
  {
    "data": "Genesis Block",
    "hash": "ef24e6c56de9f2a71eb45a34e6a95bc856229c599c7fb87a64b05ad7668e2507",
    "index": 0,
    "previous_hash": 0,
    "timestamp": 1674475073062
  },
  {
    "data": {
      "from": "Vb0IaNd8tVffF3V6PzPrUT+OznDYLfc/6sJ167KfdBJu6IsX/Oxq2qfiIOeQHEzhovqSJNqg/f3/P/EKCaJDkQ==",
      "msg": "hhh",
      "to": "4JaS/gUOII5soTL92K+dGSZ+bnHFxXDspSJg4n8+xn3Nn0CIrYj5RQBaOUgc0j4wgOFSWPQbmG2C+wN0tYIvlA=="
    },
    "hash": "fce192f5a26d29f5e936fcfd33112e8ad56113727a6c12017399d543993b6520",
    "index": 1,
    "previous_hash": "ef24e6c56de9f2a71eb45a34e6a95bc856229c599c7fb87a64b05ad7668e2507",
    "timestamp": 1674475140222
  }
]
```

