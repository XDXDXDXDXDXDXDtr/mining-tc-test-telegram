import threading
import hashlib
import socket
import time

wallet = "RahzUJEigB7JBxdAQFMyn51JbZvNf7l9lKlkJKWACW" # УКАЖИ ЭТО ПЖ
addr = "95.183.13.145"
port = 1488
diff = 6
timeout = 0.2
prev_hash = ""

def gen_hash(nonce) -> str:
    value = f"{prev_hash}.{str(nonce)}"
    return value, hashlib.sha256(value.encode()).hexdigest()


def mine(diff):
    try:
        nonce, target = 0, "0" * diff
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((addr, port))
        while True:
            VALUE, HASH = gen_hash(nonce)
            if HASH.startswith(target):
                total = f"check:{VALUE}:{HASH}:{wallet}"
                sock.send(total.encode())
                result = sock.recv(1024).decode()
                print(HASH, result)
                return
            nonce += 1
    except Exception as e: print(e)


def main():
    while True:
        mine(diff)

thread1 = threading.Thread(target=main)
thread1.start()

while True:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((addr, port))
        sock.send("get_last_hash".encode())
        l = sock.recv(1024).decode()
        prev_hash = l
        time.sleep(timeout)
    except: print ("OTVAL")
