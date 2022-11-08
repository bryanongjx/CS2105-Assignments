import sys
from socket import *
from sqlite3 import connect

def WebServer():

    def parse(connectionSocket):
        prevByte = b""
        currByte = connectionSocket.recv(1, MSG_WAITALL)
        result = ""
        while ((currByte == b' ') and (prevByte == b' ')) == False:
            result += currByte.decode()
            prevByte = currByte
            currByte = connectionSocket.recv(1, MSG_WAITALL)
        return result

    def process(data, connectionSocket):
        method = ""
        storePath = ""
        keyPath = ""
        contentLen = 0
        res = ""
        dataList = data.split()

        for i, string in enumerate(dataList):
            if string.upper() in ("DELETE", "POST", "GET"):
                method = string.upper()
            elif "/" in string:
                dir = string.split('/')
                dir = dir[1:]
                storePath = dir[0].lower()
                if len(dir) == 2:
                    keyPath = dir[1]
                else:
                    keyPath = "/".join(dir[1:])
            elif "content-length" in string.lower():
                try: 
                    contentLen = int(dataList[i + 1])
                except ValueError:
                    continue
        print(method + ' ' + storePath + ' ' + keyPath)
        
        # POST
        if method == 'POST':
            if storePath == 'key':
                if keyPath in counterStore:
                    connectionSocket.recv(contentLen, MSG_WAITALL)
                    res = "405 MethodNotAllowed  ".encode()
                else:
                    keyValueStore.update({keyPath: connectionSocket.recv(contentLen, MSG_WAITALL)})
                    res = "200 OK  ".encode()

            elif storePath == 'counter':
                if keyPath not in keyValueStore:
                    connectionSocket.recv(contentLen, MSG_WAITALL)
                    res = ("405 MethodNotAllowed  ").encode()
                elif (keyPath not in counterStore) and (keyPath in keyValueStore):
                    temp = int((connectionSocket.recv(contentLen, MSG_WAITALL).decode()))
                    counterStore.update({keyPath: temp})
                    res = "200 OK  ".encode()
                elif keyPath in counterStore:
                    counterValue = counterStore[keyPath]
                    increment = int((connectionSocket.recv(contentLen, MSG_WAITALL).decode()))
                    counterValue += increment
                    counterStore.update({keyPath: counterValue})
                    res = "200 OK  ".encode()

        # GET
        if method == 'GET':
            if storePath == 'key':
                if keyPath in keyValueStore:
                    if keyPath in counterStore:
                        counterStore[keyPath] = counterStore[keyPath] - 1
                        if counterStore[keyPath] == 0:
                            counterStore.pop(keyPath)
                            keyValueStore.pop(keyPath)
                    value = keyValueStore[keyPath]
                    res = ('200 OK Content-Length ' + str(len(value)) + '  ' + str(value)).encode()
                else:
                    res = ('404 NotFound  ').encode()
            elif storePath == 'counter':
                if keyPath not in keyValueStore:
                    res = ('404 NotFound  ').encode()
                else:
                    if keyPath in counterStore:
                        value = counterStore[keyPath]
                        res = ('200 OK Content-Length ' + str(len(str(value))) + '  ' + str(value)).encode()
                    else:
                        res = ('200 OK Content-Length 8  Infinity').encode()
            else:
                res = ('405 MethodNotAllowed  ').encode()

        # DELETE
        if method == 'DELETE':
            if storePath == 'key':
                if keyPath not in keyValueStore:
                    res = ('404 NotFound  ').encode()
                else:
                    if keyPath in counterStore:
                        res = ('405 MethodNotAllowed  ').encode()
                    else:
                        value = keyValueStore[keyPath]
                        keyValueStore.pop(keyPath)
                        res = ('200 OK Content-Length ' + str(len(value)) + '  ' + str(value)).encode()
            elif storePath == 'counter':
                if keyPath not in keyValueStore:
                    res = ('404 NotFound  ').encode()
                else:
                    counterValue = counterStore[keyPath]
                    counterStore.pop(keyPath)
                    res = ("200 OK Content-Length " + str(len(str(counterValue))) + "  " + str(counterValue)).encode()
        print(res)
        return res
    keyValueStore = {}
    counterStore = {}
    serverPort = int(sys.argv[1])
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))

    while True:
        serverSocket.listen()
        connectionSocket, clientAddress = serverSocket.accept()
        print("Connection Successful")
        while (connectionSocket.recv(1024, MSG_PEEK)):
            data = parse(connectionSocket)
            response = process(data, connectionSocket)
            connectionSocket.send(response)
        connectionSocket.close()
        print('connection closed')

if __name__ == "__main__":
    WebServer()

