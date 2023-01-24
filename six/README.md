## 六、区块链浏览器

可以在浏览器中查看某个地址的全部信息

**得到一个发送者的keys**

```cmd
python generateKey.py
```

输出

```cmd
address:fxbAv/OpUAuT+m8aXPYBfT9h34UXFYa6lPi6pQcPsDmudwZ9wAm2m0kG933AsNq7uDFCfT+z5bZGooWIeh9C6g==
private_key:f5bcd97516d8c38a3a7819a4653b2482fb816e7c8ea5becd7c189037d5ea598d
```

**得到一个接收者的keys**

```cmd
python generateKey.py
```

输出

```cmd
address:1voYAu7nVehpyAnuImBRXCYXFSfCnarjJCFv+YvSl6fXhV5rhQ/Gx3gy1twe7OGKMFEcuiby8R4Nps7StK3Aaw==
private_key:1d1357b83c44cbeb3511d6f48ef99bfaf2b5dfafaec16463fde3da86d976d7c5
```

client是发送者

运行flask server

```cmd
python blockchain.py
```

**发送交易**

```cmd
python client.py -host localhost -port 8080 -toa 1voYAu7nVehpyAnuImBRXCYXFSfCnarjJCFv+YvSl6fXhV5rhQ/Gx3gy1twe7OGKMFEcuiby8R4Nps7StK3Aaw== -froma fxbAv/OpUAuT+m8aXPYBfT9h34UXFYa6lPi6pQcPsDmudwZ9wAm2m0kG933AsNq7uDFCfT+z5bZGooWIeh9C6g== -msg hello -private f5bcd97516d8c38a3a7819a4653b2482fb816e7c8ea5becd7c189037d5ea598d
```

