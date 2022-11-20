import tkinter
import threading
import cv2
import socket
import pickle
import struct
import imutils

# UI Code
top = tkinter.Tk()
top.geometry("500x350")

video_frame = tkinter.LabelFrame(top, text="Video", width=430, height=240)
video_frame.pack()
control_frame = tkinter.LabelFrame(top, text="Controls", width=430, height=100)
control_frame.pack()


# Capture Function
def video_cap():
    # Define a video capture object
    vid = cv2.VideoCapture(0)
    
    # Connect to Target machine	
    out_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)		
    port = 6667	

    # Socket Bind
    out_sock.bind(('', port))

    print('SERVER IS LIVE')

    # Socket Listen
    out_sock.listen(5)

    # Socket Accept
    while True:
        client_socket, addr = out_sock.accept()
        print('GOT CONNECTION FROM:', addr)
        if client_socket:
            vid = cv2.VideoCapture(0)
            
            while(vid.isOpened()):
                img, frame = vid.read()
                frame = imutils.resize(frame, width=320)
                a = pickle.dumps(frame)
                message = struct.pack("Q",len(a)) + a
                client_socket.sendall(message)
                
                cv2.imshow('Live Link',frame)
                if cv2.waitKey(1) == '13':
                    client_socket.close()
	

#Start Capture Thread
cap_thread = None

def start_cap():
    cap_thread = threading.Thread(target = video_cap)
    cap_thread.start()

def stop_cap():
    pass



btnconnect = tkinter.Button(control_frame, width = 15, height = 2, text = "Start Stream", command = start_cap).place(x = 10, y = 19)
btndisconnect = tkinter.Button(control_frame, width = 15, height = 2, text = "Stop Stream", command = stop_cap).place(x = 297, y = 19)

top.mainloop()