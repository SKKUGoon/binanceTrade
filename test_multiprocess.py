from socket_client import clientb00
from socket_client import clientb01
from socket_client import clientb02
from socket_client import clientm00
from socket_client import clientm01
from socket_client import clientm02spld
from socket_client import clientm03
from socket_client import clientf00
from socket_client import clientf01s
from socket_client import clientf01l


from multiprocessing import Process, Pool
import broadcast
import os


if __name__ == "__main__":
    print(f"main process {os.getpid()}")
    p1 = Process(broadcast.broadcast())
    p2 = Process(clientb00.back00())
    p3 = Process(clientm00.middle00())

    for p in (p1, p2, p3):
        print('running start')
        p.start()

