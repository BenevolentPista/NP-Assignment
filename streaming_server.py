import socket
import tqdm
import os
import ffmpeg

# device's IP address
SERVER_HOST = "192.169.1.104"
SERVER_PORT = 5001

width = 10
height = 10

# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((SERVER_HOST, SERVER_PORT))
sock.listen(1)
print('Listening at', sock.getsockname())

while True:
    sc, sockname = sock.accept()
    print('We have accepted a connection from', sockname)
    print('  Socket name:', sc.getsockname())
    print('  Socket peer:', sc.getpeername())

    # receive the file infos
    # receive using client socket, not server socket
    received = sc.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)

    # remove absolute path if there is
    filename = os.path.basename(filename)

    # convert to integer
    filesize = int(filesize)

    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for _ in progress:
            bytes = sc.recv(BUFFER_SIZE)
            if not bytes:
                break

            f.write(bytes)

            '''
            process = ffmpeg.input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))
            process = ffmpeg.output('output.mp4', pix_fmt='yuv420p')
            process = ffmpeg.overwrite_output()
            process = ffmpeg.run_async(pipe_stdin=True)

            process.communicate(input=bytes)
            '''

            # update the progress bar
            progress.update(len(bytes))

    print("File successfully delivered")
    print(os.path.dirname(os.path.realpath(__file__)))

    sc.close()