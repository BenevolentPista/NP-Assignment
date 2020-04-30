import socket
import tqdm
import os
import ffmpeg

# device's IP address
SERVER_HOST = "192.169.1.104"
SERVER_PORT = 5001

# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

filename = "/home/pranav/Documents/PranavSista_2017A7PS1225H.mp4"
filesize = os.path.getsize(filename)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER_HOST,SERVER_PORT))
print('Client has been assigned socket name', s.getsockname())


data_sent = f"{filename}{SEPARATOR}{filesize}".encode()
s.send(data_sent)

progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    for _ in progress:

        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break

        s.sendall(bytes_read)
        progress.update(len(bytes_read))

s.close()