from socket import *
import threading
import time

#########################

#"chatRoomName":[ list of (ips, usernames, socket) ]
rooms = {}

#########################

def getIPAddress():
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def getMessage(sock):
    data = sock.recv(1024)
    return data.decode('ascii')

def isMember(room, ip):
    found = false
    for user in rooms[room]:
        found = ip == pair[0]
    return found

def findRoom(ip):
    print(f"DEBUG: finding {ip}")
    foundRoom = "NONE"
    for room in rooms.keys():
        print(f"DEBUG: checking {room}")
        for user in rooms[room]:
            print(f"DEBUG: {user}")
            if ip[0] == user[0][0]:
                foundRoom = room
    return foundRoom

def findUsername(room, ip):
    for user in rooms[room]:
        if ip[0] == user[0][0]:
            return user[1]
    return "Username not found"

def findSocket(room, ip):
    for user in rooms[room]:
        if ip[0] == user[0][0]:
            return user[2]
    return "Socket not found"

def sendMessage(sock, msg):
    #try:
    sock.send(msg.encode('ascii'))
    #except:
    #    print("Message failed to send")

def publishMessage(room, message):
    print("DEBUG: Entered publishMessage")
    for user in rooms[room]:
        try:
            sendMessage(user[2], message)
        except:
            print(f"DEBUG: Removing {user[1]}")
            EXIT(user[0], null, null)
    print("DEBUG: Exiting publishMessage")

#########################

def JOIN(ip, room_user, s):
    print("DEBUG: Entered JOIN")
    room, user = room_user.split(" ",1)
    response = ""
    if(not room in rooms.keys()):
        rooms[room] = []
        response += f"OK \t {room} created\n"
    if(user in rooms[room]):
        response += f"Denied \t {user} not unique\n"
    else:
        response += f"OK \t joined {room}\n"
        rooms[room].append((ip, user, s))
    print("DEBUG: Exiting JOIN")
    return response

def EXIT(ip, none1, none2):
    print("DEBUG: Entered EXIT")
    room = findRoom(ip)
    username = findUsername(room, ip)
    s = findSocket(room, ip)
    publishMessage(room, f"LEFT \t{username}")
    rooms[room].remove((ip, username, s))
    if len(rooms[room]) == 0:
        del rooms[room]
    print("DEBUG: Exiting EXIT")
    return ""


def SEND(ip, message, none):
    print("DEBUG: Entered SEND")
    if(not message.isascii() or len(message) > 250):
        print("DEBUG: Exiting SEND with error")
        raise ValueError("Message not supported")
    else:
        room = findRoom(ip)
        if room == "NONE":
            print("DEBUG: Exiting SEND with no username")
            return "REJECTED: No registered chatroom"
        publishMessage(room,f"SENT\t{findUsername(room, ip)}\t{message}")
        print("DEBUG: Exiting SEND")
        return ""


def WHO(ip, none1, none2):
    print("DEBUG: Entered WHO")
    room = findRoom(ip)
    if room == "NONE":
        print("DEBUG: Exiting WHO with error")
        return "REJECTED: No registered chatroom"
    response = "MEMBERS\t"
    for user in rooms[room]:
        response += user[1]+","
    print("DEBUG: Exiting WHO")
    return response[:-1]


def LIST(none1, none2, none3):
    print("DEBUG: Entered LIST")
    response = "ROOMS\t"
    for room in rooms.keys():
        response += room+","
    print("DEBUG: Exiting LIST")
    return response[:-1]

#########################

options = { "JOIN": JOIN,
            "EXIT": EXIT,
            "SEND": SEND,
            "WHO" : WHO ,
            "LIST": LIST }

#########################

def processRequest(s, addr):
    request = getMessage(s)
    data = ""
    #print(f"DEBUG: {request}")
    try:
        request, data = request.split(" ",1)
    except:
        print("ERROR WITH ARGUMENTS")
    #print(f"DEBUG: {request}, {data}")
    response = options[request](addr, data, s)
    sendMessage(s, response)
    if request != "JOIN":
        s.close()


#LWSPP 1.1
def LWSPP():
    serversocket = socket()

    host = getIPAddress()
    print(f"Listening on {host}:2028")
    serversocket.bind((host, 2028))

    serversocket.listen()

    while True:
        print("Waiting for connection...")
        clientsocket, addr = serversocket.accept()
        print("Connnection from", addr)

        threading.Thread(target=processRequest, args=(clientsocket, addr)).start()

    serversocket.close()

#########################

if __name__ == "__main__":
    LWSPP()
