from socket import *
import sys

ip = "172.16.211.70"
data = "JOIN room cam"

def LWSPPClient(addr, message):
    s = socket()
    s.connect((addr,2028))
    #print(message)
    s.send(message.encode('ascii'))
    persist = True
    while persist:
        print(s.recv(1024).decode('ascii'))
        persist = message.split(' ')[0] == "JOIN"
    s.close()
    #if(message.split(' ')[0] != "JOIN"):
        #print("HERE")
    #    s.close()
    #else:
    #    while(True):
    #        received = s.recv(1024)
    #        print(received.decode('ascii'))

if(len(sys.argv[1].split(".")) == 4):
    ip = sys.argv[1]
    data = ""
    for i in range(2,len(sys.argv)):
        data += sys.argv[i] + " "
    LWSPPClient(ip, data.strip())
else:
    print("DEFAULT")
    LWSPPClient(ip, data)

#if __name__ == '__main__':
#    LWSPPClient(ip, data)
