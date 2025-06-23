# 🔁 Redis Clone (Python)

> 🚀 A beginner-friendly Redis clone built from scratch using **Python sockets and threading**, supporting core Redis features like key-value storage, expiration, persistence, and Pub/Sub — perfect for learning systems programming and building your portfolio.

---

## ✨ Features

- 📝 `SET`, `GET`, `DEL` — Basic key-value operations  
- ⏳ `EXPIRE`, `TTL` — Key expiration with countdown  
- ➕ `INCR` — Increment integer keys  
- 🛑 `FLUSHALL` — Clear all keys  
- 🔐 `AUTH` — Password authentication  
- 📋 `KEYS` — List all keys  
- 🔔 `PUB/SUB` — Publish/Subscribe support  
- 💾 `SAVE` — Manual DB save to file  
- 💾 **Auto-Save** every 60s to `dump.rdb`  
- 🔌 Multi-client via threading  
- 🧠 RESP-like protocol parsing  

---

## 📦 Project Structure

redis_server/
├── server.py # Redis server implementation
├── test_server.py # Unit tests
├── Dockerfile # Container build file
├── redis_data/ # Persistent RDB storage
├── LICENSE # MIT license
├── .gitignore
└── README.md


---

## 🚀 Quick Start

### 🐍 Run with Python


python3 server.py

###🐳 Run with Docker

docker build -t redis-clone .
docker run -p 6379:6379 \
  -v $(pwd)/redis_data/dump.rdb:/app/dump.rdb \
  redis-clone

###📡 How to Connect

Use redis-cli, telnet, or a Python client:

redis-cli -p 6379
AUTH rehan1
SET name "Rehan"
GET name
EXPIRE name 10
TTL name

###📋 Supported Commands
| Feature         | Description                              |
|----------------|------------------------------------------|
| `SET`, `GET`    | Store and retrieve string values         |
| `EXPIRE`, `TTL` | Set expiration and view remaining time   |
| `DEL`           | Delete keys manually                     |
| `INCR`          | Auto-increment numeric values            |
| `AUTH`          | Simple password protection               |
| `SAVE`          | Manual save to `dump.rdb` file           |
| `FLUSHALL`      | Clear the entire DB                      |
| `KEYS`          | List all keys                            |
| `MYHELP`        | Built-in help command                    |
| `SUBSCRIBE`     | Subscribe to a connection                |
| `PUBLISH`       | Send Messages to a connection            |
###🧪 Example CLI Session

127.0.0.1:6379> AUTH rehan1
+OK

127.0.0.1:6379> SET greeting Hello
+OK

127.0.0.1:6379> GET greeting
$5
Hello

127.0.0.1:6379> EXPIRE greeting 10
:1

127.0.0.1:6379> TTL greeting
:9

127.0.0.1:6379> PING
+PONG

127.0.0.1:6379> SAVE
+OK

###🔮 Future Features

    Add Redis LIST, SET, HASH support

    Background save (BGSAVE) and replication

    Advanced logging and analytics

    Client library in Python

    Cluster support for horizontal scaling

###📜 License

This project is licensed under the MIT License.
👨‍💻 Author

Built with ❤️ by Rehan Ahmad Mirza
