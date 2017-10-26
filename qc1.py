import select
import socket
import sys
import queue
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
# Bind the socket to the port
server_address = ('0.0.0.0', 10000)
print('starting up on {} port {}'.format(*server_address),
              file=sys.stderr)
server.bind(server_address)
# Listen for incoming connections
server.listen(5)

# Sockets from which we expect to read
inputs = [server]

# Sockets to which we expect to write
outputs = []
# Outgoing message queues (socket:Queue)
mq = queue.Queue()


while inputs:
    print('waiting for the next event', file=sys.stderr)
    readable, writable, exceptional = select.select(inputs,outputs,inputs)
    for s in readable:
        if s is server:
            connection,client_address=s.accept()
            print('  connection from', client_address,file=sys.stderr)
            connection.setblocking(0)
            inputs.append(connection)
        else:
            data=s.recv(1024)
            if data:
                print('  received {!r} from {}'.format(data, s.getpeername()), file=sys.stderr,)
                if s not in outputs:
                    outputs.append(s)
            else:
                print('  closing', client_address,
                        file=sys.stderr)
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
    for s in writable:
        msg="HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html>123</html>\n"
        print('  sending {!r} to {}'.format(msg,s.getpeername()),file=sys.stderr)
        s.sendall(msg.encode())
        #if s in outputs:
        outputs.remove(s)
        inputs.remove(s)
        s.close()
    for s in exceptional:
        print('exception condition on', s.getpeername(),file=sys.stderr)
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
