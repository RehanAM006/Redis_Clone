import socket
import threading
import time


HOST = '127.0.0.1'
PORT = 6379

data_store = {}
expiry_store = {}  # key -> timestamp


# Server configuration
HOST = '0.0.0.0'
PORT = 6379

# Hardcoded password for AUTH
PASSWORD = "rehan1"

# In-memory key-value store
data_store = {}
expiry_store = {}  # Stores expiration time: key -> timestamp
channel_subscribers = {} #channel -> list connections

# === Load from RDB (if exists) ===

try:
    with open('dump.rdb', 'r') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) >= 2:
                key = parts[0]
                value = parts[1]

                expiry_time = float(part[2])  if len(parts) == 3 and parts[2] != 'None' else None
 

                expiry_time = float(parts[2]) if len(parts) == 3 and parts[2] != 'None' else None


                data_store[key] = value
                if expiry_time:
                    expiry_store[key] = expiry_time

    print("Loaded database from dump.rdb")

except FileNotFoundError:
    print("No previous database found, starting fresh")


def parse_resp(data: str):


# === RESP Protocol Parser ===
def parse_resp(data: str):
    """Parse RESP protocol from redis-cli"""

    lines = data.split('\r\n')
    if not lines or not lines[0].startswith('*'):
        return []

    num_items = int(lines[0][1:])
    items = []

    i = 1
    while i < len(lines) - 1 and len(items) < num_items:
        if lines[i].startswith('$'):
            item = lines[i + 1]
            items.append(item)
            i += 2
        else:
            i += 1
    return items


def auto_save():


# === Auto Save Thread ===
def auto_save():
    """Saves key-value store to dump.rdb every 60 seconds"""

    while True:
        time.sleep(60)
        try:
            with open('dump.rdb', 'w') as f:
                for key, value in data_store.items():
                    expiry_time = expiry_store.get(key)
                    line = f"{key}|{value}|{expiry_time}\n"
                    f.write(line)
            print("[AutoSave] Database saved to dump.rdb")
        except Exception as e:

            print("f[AutoSave] Error saving database: {e}")


def is_expired(key):
    """Check and delete key if expired. Returns True if key is expired."""

            print(f"[AutoSave] Error saving database: {e}")


# === Expiry Check ===
def is_expired(key):
    """Remove key if expired. Return True if it was expired."""

    if key in expiry_store:
        if time.time() >= expiry_store[key]:
            data_store.pop(key, None)
            expiry_store.pop(key, None)
            return True
    return False



def handle_client(conn, addr):
    print(f"Connected by {addr}")

# === Handle Each Client ===
def handle_client(conn, addr):
    print(f"Connected by {addr}")
    clnt_authd = False  # Track if this client has authenticated


    with conn:
        buffer = b""
        while True:
            try:
                chunk = conn.recv(1024)
                if not chunk:
                    break
                buffer += chunk

                # Decode chunk

                try:
                    data = buffer.decode()
                except UnicodeDecodeError:
                    continue

                commands = parse_resp(data)
                buffer = b""  # Clear after decoding

                if not commands:
                    conn.sendall(b'-Error: invalid or empty RESP\r\n')
                    continue

                command = commands[0].upper()


                # Enforce authentication for all commands except AUTH
                if not clnt_authd and command != 'AUTH':
                    conn.sendall(b"-NOAUTH Authentication required\r\n")
                    continue

                # === Core Redis-like Commands ===


                if command == 'PING':
                    conn.sendall(b'+PONG\r\n')

                elif command == 'SET' and len(commands) == 3:
                    key, value = commands[1], commands[2]
                    data_store[key] = value
                    expiry_store.pop(key, None)
                    conn.sendall(b'+OK\r\n')

                elif command == 'GET' and len(commands) == 2:
                    key = commands[1]

                    if is_expired(key) or key not in data_store:
                        conn.sendall(b"$-1\r\n")
                    else:
                        value = data_store[key]
                        response = f"${len(value)}\r\n{value}\r\n"
                        conn.sendall(response.encode())

                elif command == 'EXPIRE' and len(commands) == 3:
                    key, seconds = commands[1], int(commands[2])
                    if key in data_store and not is_expired(key):
                        expiry_store[key] = time.time() + seconds
                        conn.sendall(b":1\r\n")
                    else:
                        conn.sendall(b":0\r\n")

                elif command == 'TTL' and len(commands) == 2:
                    key = commands[1]

                    if is_expired(key) or key not in data_store:
                        conn.sendall(b":-2\r\n")
                    elif key not in expiry_store:
                        conn.sendall(b":-1\r\n")
                    else:
                        remaining = int(expiry_store[key] - time.time())

                        if remaining < 0:
                            conn.sendall(b":-2\r\n")
                        else:
                            conn.sendall(f":{remaining}\r\n".encode())

                        conn.sendall(f":{max(remaining, 0)}\r\n".encode())


                elif command == 'DEL' and len(commands) == 2:
                    key = commands[1]
                    deleted = 0


                    if is_expired(key):
                        pass


                    if is_expired(key):
                        pass

                    elif key in data_store:
                        data_store.pop(key, None)
                        expiry_store.pop(key, None)
                        deleted = 1



                    conn.sendall(f":{deleted}\r\n".encode())

                elif command == 'INCR' and len(commands) == 2:
                    key = commands[1]


                    if is_expired(key):
                        data_store.pop(key, None)
                        expiry_store.pop(key, None)

                    if key not in data_store:
                        data_store[key] = "1"
                        conn.sendall(b":1\r\n")

                    else:
                        current_value = data_store[key]


                    if is_expired(key):
                        data_store.pop(key, None)
                        expiry_store.pop(key, None)
                    if key not in data_store:
                        data_store[key] = "1"
                        conn.sendall(b":1\r\n")
                    else:
                        current_value = data_store[key]

                        try:
                            num = int(current_value)
                            num += 1
                            data_store[key] = str(num)
                            conn.sendall(f":{num}\r\n".encode())

                        except (ValueError, TypeError):
                            conn.sendall(b"-ERROR: value is not an integer\r\n")

                elif command == 'SAVE':
                    try:
                        with open('dump.rdb', 'w') as f:
                            for key, value in data_store.items():
                                expire_time = expiry_store.get(key)

                                line = f"{key}|{value}|{expire_time}\n"
                                f.write(line)
                            conn.sendall(b"+OK: Data saved to dump.rdb\r\n")
                    except Exception as e:
                        error_msg = f"-ERROR saving data: {str(e)}\r\n"
                        conn.sendall(error_msg.encode())
            

                                f.write(f"{key}|{value}|{expire_time}\n")
                        conn.sendall(b"+OK: Data saved to dump.rdb\r\n")
                    except Exception as e:
                        conn.sendall(f"-ERROR saving data: {e}\r\n".encode())

                elif command == 'FLUSHALL':
                    data_store.clear()
                    expiry_store.clear()
                    conn.sendall(b"+OK\r\n")

                elif command == 'KEYS':
                    keys = []
                    for k in list(data_store.keys()):
                        if is_expired(k):
                            data_store.pop(k, None)
                            expiry_store.pop(k, None)
                        else:
                            keys.append(k)
                    response = f"*{len(keys)}\r\n"
                    for key in keys:
                        response += f"${len(key)}\r\n{key}\r\n"
                    conn.sendall(response.encode())

                # === AUTH Support ===
                elif command == 'AUTH':
                    if len(commands) == 2:
                        password = commands[1]
                    elif len(commands) == 3:
                        password = commands[2]
                    else:
                        conn.sendall(b"-ERR wrong number of arguments for AUTH\r\n")
                        continue

                    if password == PASSWORD:
                        clnt_authd = True
                        conn.sendall(b"+OK\r\n")
                    else:
                        conn.sendall(b"-ERR invalid password\r\n")

                # === Custom Help Command ===
                elif command == 'MYHELP':
                    help_lines = [
                        "GET key",
                        "SET key value",
                        "DEL key",
                        "EXPIRE key seconds",
                        "TTL key",
                        "INCR key",
                        "FLUSHALL",
                        "KEYS",
                        "AUTH [password] or AUTH [username] [password]",
                        "PING",
                        "SAVE",
                        "MYHELP",
                    ]
                    response = f"*{len(help_lines)}\r\n"
                    for line in help_lines:
                        response += f"${len(line)}\r\n{line}\r\n"
                    conn.sendall(response.encode())

                elif command == 'SUBSCRIBE' and len(commands) >= 2:
                    for channel in commands[1:]:
                        # Initialize channel list
                        if channel not in channel_subscribers:
                            channel_subscribers[channel] = []

                        # Add this connection if not already subscribed
                        if conn not in channel_subscribers[channel]:
                            channel_subscribers[channel].append(conn)

                        # RESP response format:
                        # *3\r\n$9\r\nsubscribe\r\n$<len(channel)>\r\n<channel>\r\n:<subscription_count>\r\n
                        response = f"*3\r\n$9\r\nsubscribe\r\n${len(channel)}\r\n{channel}\r\n:{len(channel_subscribers[channel])}\r\n"
                        conn.sendall(response.encode())


                elif command == 'PUBLISH' and len(commands) == 3:
                        channel = commands[1]
                        message = commands[2]

                        subscribers = channel_subscribers.get(channel, [])
                        sent_count = 0

                        for subscriber_conn in subscribers:
                            try:
                                # RESP message format for pub/sub:
                                # *3\r\n$7\r\nmessage\r\n$<len(channel)>\r\n<channel>\r\n$<len(message)>\r\n<message>\r\n
                                response = (
                                    f"*3\r\n"
                                    f"$7\r\nmessage\r\n"
                                    f"${len(channel)}\r\n{channel}\r\n"
                                    f"${len(message)}\r\n{message}\r\n"
                                )
                                subscriber_conn.sendall(response.encode())
                                sent_count += 1
                            except Exception as e:
                                print(f"[PUBLISH] Failed to send to subscriber: {e}")

                        # Respond to publisher with count of delivered messages
                        conn.sendall(f":{sent_count}\r\n".encode())




                else:
                    conn.sendall(b'-Error: unknown or invalid command\r\n')


            except Exception as e:
                print(f"Error with {addr}: {e}")
                break



# === Start Server ===

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")


        threading.Thread(target=auto_save, daemon=True).start()


        # Start background auto-save thread
        threading.Thread(target=auto_save, daemon=True).start()

        # Accept connections

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"Started thread for {addr}")


# Entry point

if __name__ == "__main__":
    start_server()

