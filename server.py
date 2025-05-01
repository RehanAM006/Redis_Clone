import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 6379

data_store = {}
expiry_store = {}  # key -> timestamp

try:
    with open('dump.rdb', 'r') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) >= 2:
                key = parts[0]
                value = parts[1]
                expiry_time = float(part[2])  if len(parts) == 3 and parts[2] != 'None' else None
 
                data_store[key] = value
                if expiry_time:
                    expiry_store[key] = expiry_time

    print("Loaded database from dump.rdb")

except FileNotFoundError:
    print("No previous database found, starting fresh")

def parse_resp(data: str):
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
    if key in expiry_store:
        if time.time() >= expiry_store[key]:
            data_store.pop(key, None)
            expiry_store.pop(key, None)
            return True
    return False


def handle_client(conn, addr):
    print(f"Connected by {addr}")
    with conn:
        buffer = b""
        while True:
            try:
                chunk = conn.recv(1024)
                if not chunk:
                    break
                buffer += chunk

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

                elif command == 'DEL' and len(commands) == 2:
                    key = commands[1]
                    deleted = 0

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
            

                else:
                    conn.sendall(b'-Error: unknown or invalid command\r\n')

            except Exception as e:
                print(f"Error with {addr}: {e}")
                break


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")

        threading.Thread(target=auto_save, daemon=True).start()

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"Started thread for {addr}")


if __name__ == "__main__":
    start_server()

