import SocketServer
import threading
import socket
import sys

class DLCommandServer(threading.Thread):

    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.HOST = host
        self.PORT = port

    def run(self):
        server = SocketServer.TCPServer((self.HOST, self.PORT), CommandHandler)
        server.serve_forever()


class CommandHandler(SocketServer.BaseRequestHandler):
    def handle(self):

        self.data = self.request.recv(1024).strip()

        print "{} wrote:".format(self.client_address[0])
        print self.data

        # just send back the same data, but upper-cased

        #self.request.sendall(self.data.upper())


class DLServer(threading.Thread):

    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.ADDR = (host, port)
        self.Status = ''
        self.DL_Result = 'aa'


    def setResult(self, res):
        self.DL_Result = res

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(self.ADDR)
        sock.listen(2)

        while True:
            print 'Waiting Client'

            cl_sock, addr = sock.accept()
            print addr, ' connected!'

            while True:

                try:
                    cmd_str = '[%s] %s' % ('CLS', self.DL_Result)
                    cl_sock.sendall( cmd_str )

                except socket.error, (errorCode, message):
                    if errorCode != 10035:
                        #print 'socket.error - (' + str(errorCode) + ') ' + message
                        break

            cl_sock.close()
            print addr,  ' close client socket'

        sock.close()
        print 'close server socket'
