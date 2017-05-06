import socket
import massey
import argparse

BUFF = 4096
CHUNK_SIZE = 4

def server(port):
    print("... Server Started ...")

    server_address = None
    server_port = port
    sock = None

    print("Server port: " + str(server_port))

    for res in socket.getaddrinfo(server_address, server_port, socket.AF_INET6, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res

        try:
            sock = socket.socket(af, socktype, proto)
        except socket.error:
            sock = None
            continue

        try:
            sock.bind(sa)
            sock.listen(4)
        except socket.error:
            sock.close()
            sock = None
            continue
        break



    if sock is None:
        print('Open socket error...')
    else:
        while True:
            print("Waiting for a connection ...")
            connection, client_address = sock.accept()
            print("Connection established with: ", client_address)

            # receives a message and send it back encrypted with 'e'
            data = connection.recv(BUFF)
            vect = []
            res = massey.chunkstring(data, CHUNK_SIZE)
            dkey = []
            for elem in res:
                e,d = massey.generate_keys()
                dkey.append(d)
                vect.append(massey.crypt_chunk(elem, e))
            connection.send("".join(vect))


            # receives a message and decrypt it with 'd',
            # this is the original clear text
            res = []
            data = connection.recv(BUFF)
            i=0
            for elem in massey.chunkstring(data, CHUNK_SIZE):
                d=dkey[i]
                res.append(massey.crypt_chunk(elem, d))
                i += 1
            print("The decrypted message is: " + "".join(res))

            connection.close()

def client(s_ip, s_port):
    print("... Client Started ...")
    print("Server address: " + s_ip)
    print("Server port: " + str(s_port))

    print("Menu:")
    print("1) Connect to server")
    print("2) Send a message with Massey-Omura protocol")
    print("0) Close connection")

    s = None
    while True:
        print("#########################################")
        choice = raw_input("Choice #: ")
        if choice == '1':
            s=socket.socket()
            s.connect((s_ip, s_port))
            print("Connected with the server")
        if choice == '2':
            if s is not None:
                msg = raw_input("Message: ")
                msg = msg + "0"*((CHUNK_SIZE - (len(msg)%CHUNK_SIZE))%CHUNK_SIZE)
                i = 0
                vect = []
                dkey = []
                while i<len(msg)/CHUNK_SIZE:
                    e,d = massey.generate_keys()
                    dkey.append(d)
                    vect.append(massey.crypt_chunk(msg[(i*CHUNK_SIZE):(i*CHUNK_SIZE)+CHUNK_SIZE], e))
                    i += 1
                # send the message encrypted with 'e'
                s.send("".join(vect))
                print "The message was sent"

                # receives a message, decrypt it with 'd', and send it back
                res = []
                data = s.recv(BUFF)
                vect = massey.chunkstring(data, CHUNK_SIZE)
                i=0
                for elem in vect:
                    d=dkey[i]
                    res.append(massey.crypt_chunk(elem, d))
                    i += 1

                s.send("".join(res))
            else:
                print("No active socket")
        if choice == '0':
            if s is not None:
                s.send("CLOSE")
                s.close()
                s = None
                print("Connection interrupted")
                break
            else:
                print("No active socket")

def main(p_args, other_args):
    if p_args.l:
        server(p_args.p)
    else:
        client(p_args.a, p_args.p)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-l', help='Activate Server',action='store_true')
  parser.add_argument('-p', type=int, default=3000, help='Server Port')
  parser.add_argument('-a', type=str, default='127.0.0.1', help='Server Address')
  args, unparsed = parser.parse_known_args()
  main(args, unparsed)
