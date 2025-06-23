# 🔁 Redis Clone (Python)

A beginner-friendly Redis clone built in Python — supporting core Redis commands, expiration, persistence, and authentication. Perfect for learning systems programming and contributing to open source.

---

## ⚙️ Features

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

---

## 🚀 Quick Start

### 🐍 Run directly with Python
```bash
python3 server.py

### 🐳 Run with Docker

docker build -t redis-clone .
docker run -p 6379:6379 \
  -v $(pwd)/redis_data/dump.rdb:/app/dump.rdb \
  redis-clone

### 🧪 Test it

redis-cli -p 6379
> AUTH rehan1
> SET name "Rehan"
> GET name
> EXPIRE name 30
> TTL name

### 🧠 Tech Stack
Python 3.10

Sockets (TCP)

RESP protocol

Docker

### 📂 Project Structure
redis_server/
├── server.py           # main Redis clone
├── test_server.py      # unit tests
├── redis_data/         # persistent dump.rdb file
├── Dockerfile
├── README.md
└── LICENSE

### 📜 License
Licensed under the MIT License.

### 🤝 Contributions

---

You can now paste this into your `README.md`. Let me know when it’s done — we can continue with another GitHub file or feature.


>>>>>>> 5c02de4 (Add PUB/SUB, Docker,README, and tests)
