import socket

class webApp:

    def __init__(self, hostname, port):
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind((hostname, port))
        mySocket.listen(5)
        while True:
            print('Waiting for connections')
            (recvSocket, address) = mySocket.accept()
            print('HTTP request received (going to parse and process):')
            request = recvSocket.recv(4096).decode('ASCII')
            print(request)
            (returnCode, htmlAnswer) = self.process(request)
            print('Answering back...')
            recvSocket.send(bytes('HTTP/1.1 ' + returnCode + ' \r\n\r\n' + htmlAnswer + '\r\n', 'utf-8'))
            recvSocket.close()

if __name__ == '__main__':
    testWebApp = webApp("localhost", 1234)
