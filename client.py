
import sys
import socket
host = '127.0.0.1'
port = 5004 
SIZE = 2048




def EnvoyerPrix(s):
    ref=input("donner reference:")
    s.sendto(str(ref).encode(),(host,port))
    prix=int(input("Proposeer un prix:"))
    s.sendto(str(prix).encode(),(host,port))
    (response,res)=s.recvfrom(SIZE)
    print(str(response.decode()))
    return

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
(response,res)=s.recvfrom(SIZE)
print(str(response.decode()))
while(1):
    EnvoyerPrix(s)


sys.exit()
