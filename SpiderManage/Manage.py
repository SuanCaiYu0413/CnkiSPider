# -*- coding:utf-8 -*-
from MyCnki.CnkiSpider import Spider
import socket

def main():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost',8001))
    sock.listen(5)

    while True:
        connection, address = sock.accept()
        print connection
        buf = connection.recv(1024)
        print buf
        connection.close()

if __name__ == '__main__':
    main()