# Redis Clone (Python)

> 🚀 A minimal Redis clone built from scratch using **Python sockets and threading**, supporting basic Redis functionality and data persistence.

---

## ✨ Features

- 📝 **SET** — Store key-value pairs
- 🔍 **GET** — Retrieve values
- 💑 **DEL** — Delete keys
- ⏳ **EXPIRE** — Set key expirations
- ⏱️ **TTL** — Check time left before expiration
- ➕ **INCR** — Auto-increment integer values
- 🏓 **PING** — Health check
- 💾 **SAVE** — Manual database save
- 🔥 **Auto-Save** — Automatic periodic database save every 60 seconds
- 💃 **Persistence** — Loads previous data from file on server startup
- 🔌 **Multi-client support** — Handles multiple clients concurrently using threads

---

## 🛠️ How It Works

- Built using **low-level socket programming** (TCP server)
- **Multi-threaded**: Each client is handled in a separate thread
- **Simple RESP-like Protocol** for commands
- Stores key-value data in memory
- Automatically persists data to `dump.rdb` file

---

## 💻 Installation

1. **Clone the repository**

```bash
git clone https://github.com/RehanAM006/Redis_Clone.git
cd redis-clone-python
```

2. **Run the server**

```bash
python server.py
```

---

## 📱 How to Connect

You can use **`redis-cli`** or **telnet**:

```bash
telnet localhost 6379
```

Then start sending commands!

---

## 📋 Supported Commands

| Command             | Description                                    | Example                             |
|:--------------------|:-----------------------------------------------|:------------------------------------|
| `SET key value`      | Set a string value to a key                   | `SET name Alice`                    |
| `GET key`            | Get the value of a key                        | `GET name`                          |
| `DEL key`            | Delete a key and its value                    | `DEL name`                          |
| `EXPIRE key seconds` | Set a timeout on a key (in seconds)            | `EXPIRE name 10`                    |
| `TTL key`            | Get remaining time to live of a key (in secs)  | `TTL name`                          |
| `INCR key`           | Increment integer value of a key by 1         | `INCR counter`                      |
| `PING`               | Check if server is alive                      | `PING`                              |
| `SAVE`               | Manually save database to `dump.rdb`           | `SAVE`                              |

---

## 📂 Project Structure

| File        | Purpose                         |
|:------------|:---------------------------------|
| `server.py` | Main server code                 |
| `dump.rdb`  | Auto-saved database backup file  |

---

## 🧪 Example Session

```bash
127.0.0.1:6379> PING
+PONG

127.0.0.1:6379> SET greeting Hello
+OK

127.0.0.1:6379> GET greeting
$5
Hello

127.0.0.1:6379> INCR counter
:1

127.0.0.1:6379> EXPIRE greeting 10
:1

127.0.0.1:6379> TTL greeting
:8

127.0.0.1:6379> SAVE
+OK
```

---

## 🚀 Future Improvements (Optional)

- Implement Redis data types like **LISTS**, **HASHES**, **SETS**
- Add **Pub/Sub** messaging system
- **Authentication** support (e.g., `AUTH password`)
- More efficient **binary-safe protocol parsing**
- Background saving with less blocking (like Redis BGSAVE)

---

## 👨‍💻 Author

Built with ❤️ by **Rehan Ahmad Mirza**

---



---

