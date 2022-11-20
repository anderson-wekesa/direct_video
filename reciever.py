import tkinter
import threading
import cv2
import socket
import numpy
import pickle
import struct

# UI Code
top = tkinter.Tk()
top.geometry("500x350")

video_frame = tkinter.LabelFrame(top, text="Video", width=430, height=240)
video_frame.pack()
control_frame = tkinter.LabelFrame(top, text="Controls", width=430, height=100)
control_frame.pack()


# Capture Function
def video_playback():	

    # next create a socket object
    sock = socket.socket()		
    print ("Socket successfully created")

    # reserve a port on your computer in our case it is 12345 but it can be anything
    host_ip = '192.168.0.13'
    port = 6667			

    sock.connect((host_ip, port)) # a tuple
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = sock.recv(4*1024) # 4K
            if not packet: break
            data+=packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
        
        while len(data) < msg_size:
            data += sock.recv(4*1024)
        frame_data = data[:msg_size]
        data  = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("Live Link",frame)
        if cv2.waitKey(1) == '13':
            break
    #sock.close()

    

#Start Capture Thread
cap_thread = None

def start_recv():
    cap_thread = threading.Thread(target = video_playback)
    cap_thread.start()

def stop_recv():
    pass



btnconnect = tkinter.Button(control_frame, width = 15, height = 2, text = "Start Stream", command = start_recv).place(x = 10, y = 19)
btndisconnect = tkinter.Button(control_frame, width = 15, height = 2, text = "Stop Stream", command = stop_recv).place(x = 297, y = 19)

top.mainloop()