import os
import glob
import time
import RPi.GPIO as GPIO
from bluetooth import *

email='x'
option='picture'
numb=2
attachm=1

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "SpyCam",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
while True:          
    print ("Waiting for connection on RFCOMM channel ", port)
    client_sock, client_info = server_sock.accept()
    print ("Accepted connection ")
    try:
        data = client_sock.recv(1024)
        if len(data) == 0: break
        print ("received "+ data)
        email,option,numb,attachm = data.split(" ")
        file = open("options.txt", "w+")
        file.write(email+'\n')
        file.write(option+'\n')
        file.write(numb+'\n')
        file.write(attachm+'\n')
        file.close()

	    #client_sock.send(data)
 
    except IOError:
        pass

    except KeyboardInterrupt:

        print ("disconnected")

        client_sock.close()
        server_sock.close()
        print ("all done")

        break
