import tkinter 
import cv2 # pip install opencv-python
import PIL.Image, PIL.ImageTk # pip install pillow
from functools import partial
import threading
import time
import imutils # pip install imutils

stream = cv2.VideoCapture("clip.mp4") # it will capture my video
flag = True
def play(speed):
    global flag
    print(f"You clicked on play. Speed is {speed}")

    # Play the video in reverse mode
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)#its is denote the frame number. whuch  reads a frame number
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)#suppose frame number is 100 and speed is -5 then frame nuber shows a 100-5=95;

    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))# I would bring tkinter compatible photo image
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    if flag:
        canvas.create_text(134, 26, fill="black", font="Times 26 bold", text="Decision Pending")# blink a background color of frame 
    flag = not flag
    

def pending(decision):
    # 1. Display decision pending image
    frame = cv2.cvtColor(cv2.imread("pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)# it can use in tkinter GUI
    # 2. Wait for 1 second
    time.sleep(1.5)

    # 3. Display sponsor image
    frame = cv2.cvtColor(cv2.imread("sponsor.png"), cv2.COLOR_BGR2RGB)# it has changed the rgb color
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)# changed resize of image
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))# my frame have to changed to photo image object
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)

    # 4. Wait for 1.5 second
    time.sleep(2.5)
    # 5. Display out/notout image
    if decision == 'out':
        decisionImg = "out.png"
    else:
        decisionImg = "not_out.png"
    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)


def out():
    thread = threading.Thread(target=pending, args=("out",))#why use it. because program will not block and it will move to down side
    thread.daemon = 1# as I want make a daemon program
    thread.start()
    #it will run the pending fuction
    print("Player is out")


def not_out():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()
    print("Player is not out")

# Width and height of our main screen
SET_WIDTH = 650 # it is visible in the screen
SET_HEIGHT = 368

# Tkinter gui starts here
window = tkinter.Tk()#it is syntax;
window.title("Third Umpire Decision Review Kit")# tittle  
cv_img = cv2.cvtColor(cv2.imread("welcome.png"), cv2.COLOR_BGR2RGB) # open_cv is  a huge open source library for compuer vision and image processing
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)# background of image is present in the canvas
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img)) 
# whatever image I put in tkinter convas
image_on_canvas = canvas.create_image(0, 0, ancho=tkinter.NW, image=photo)
#it is desgin.
canvas.pack()


# Buttons to control playback
btn = tkinter.Button(window, text="<< Previous (fast)", width=50, command=partial(play, -25))
# I have made bottons
btn.pack()# we have to pack button 
# we can move on any speed in command fuction

btn = tkinter.Button(window, text="<< Previous (slow)", width=50, command=partial(play, -2)) #command fuction - use for play button
btn.pack()#packs all the widgets one after the other in a window

btn = tkinter.Button(window, text="Next (slow) >>", width=50, command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text="Next (fast) >>", width=50, command=partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text="Give Out", width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text="Give Not Out", width=50, command=not_out)
btn.pack()
window.mainloop() #ready to run applicaton and it is infinite loop used to run the application