from tkinter import filedialog
from tkinter import *
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
from PIL import ImageTk, Image, ImageChops
import imutils

import os
import numpy as np
import pandas as pd

import cv2

images = []
stitchedImage = [0]

gui = Tk()
gui.geometry("1300x650")
style = ThemedStyle(gui)

style.set_theme("clearlooks")
style.configure('my.TButton', foreground="white")
gui.title("Panorama and Paint by Number")

main_frame = Frame(gui)
main_frame.pack(side=LEFT, fill=BOTH, expand=1)

canvas = Canvas(main_frame)
canvas.pack(side=LEFT, fill=BOTH, expand=1)

scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

second_frame = Frame(canvas)
canvas.create_window((0, 0), window=second_frame, anchor='nw')


def myClick():
    mylabel = ttk.Label(second_frame, text="myclick clicked")
    mylabel.pack()

# -------- input field ---------
input1 = Entry(second_frame, width=60)
input1.pack()

def myInput():
    input01 = "Hello " + input1.get()
    mylabel = ttk.Label(gui, text=input01)
    mylabel.pack()


def mySlider(slider):
    input01 = "Hello " + str(int(slider))
    mylabel = ttk.Label(gui, text=input01)
    mylabel.pack()


def browse_button():
    global folder_path

    filename = filedialog.askdirectory()
    folder_path = filename
    lbl_path = ttk.Label(gui, text=folder_path)
    lbl_path.pack()
    print(filename)

    images.clear()
    # folder_path = 'C:/Users/Asus/Pictures/scott folder'
    myList = os.listdir(folder_path)
    print(f'Total no of images detected : {len(myList)}')
    print(len(images))
    for imgN in myList:
        curImg = cv2.imread(f'{folder_path}/{imgN}')
        curImg = cv2.cvtColor(curImg, cv2.COLOR_BGR2RGB)
        # curImg = cv2.resize(curImg, (0, 0), None, 0.2, 0.2)
        images.append(curImg)


def showImages():
    top = Toplevel()
    top.title("Image Insert")

    for i in range(len(images)):
        canvas = Canvas(gui)
        canvas.pack()
        # if len(images) > 0:
        imgPil = Image.fromarray(images[i].astype('uint8'), 'RGB')
        myImg = ImageTk.PhotoImage(imgPil)
        img = Label(top, image=myImg)
        img.image = myImg
        img.place(x=0, y=0)


def image_page_stitched():
    global myImg

    top = Toplevel()
    top.title("Image Insert")
    imgPil = Image.fromarray(stitchedImage[0].astype('uint8'), 'RGB')

    size = (1000, 800)
    imgPil.thumbnail(size, Image.ANTIALIAS)
    image_size = imgPil.size

    thumb = imgPil.crop((0, 0, size[0], size[1]))

    offset_x = int(max((size[0] - image_size[0]) / 2, 0))
    offset_y = int(max((size[1] - image_size[1]) / 2, 0))

    thumb = ImageChops.offset(thumb, offset_x, offset_y)

    myImg = ImageTk.PhotoImage(thumb)
    label_img = Label(top, image=myImg).pack()


def image_page():
    global myImg

    top = Toplevel()
    top.title("Image Insert")
    imgPil = Image.fromarray(images[0].astype('uint8'), 'RGB')

    size = (1000, 800)
    imgPil.thumbnail(size, Image.ANTIALIAS)
    image_size = imgPil.size

    thumb = imgPil.crop((0, 0, size[0], size[1]))

    offset_x = int(max((size[0] - image_size[0]) / 2, 0))
    offset_y = int(max((size[1] - image_size[1]) / 2, 0))

    thumb = ImageChops.offset(thumb, offset_x, offset_y)

    myImg = ImageTk.PhotoImage(thumb)
    label_img = Label(top, image=myImg).pack()


def stitchingImage():
    # result = np.ndarray(shape=(2, 2))
    # images = resizeImage(images)
    stitcher = cv2.Stitcher.create()
    stitchedImage.clear()
    print('stitching')
    try:
        (status, result) = stitcher.stitch(images)
        if status == cv2.STITCHER_OK:
            print('success')
            Label(gui, text='Stitching success').pack()

            print("cropping...")
            stitched = cv2.copyMakeBorder(result, 10, 10, 10, 10,
                                          cv2.BORDER_CONSTANT, (0, 0, 0))

            gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            c = max(cnts, key=cv2.contourArea)

            mask = np.zeros(thresh.shape, dtype="uint8")
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

            minRect = mask.copy()
            sub = mask.copy()
            print("cropping1...")
            while cv2.countNonZero(sub) > 0:
                minRect = cv2.erode(minRect, None)
                sub = cv2.subtract(minRect, thresh)

            cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
            print("cropping2...")
            cnts = imutils.grab_contours(cnts)
            c = max(cnts, key=cv2.contourArea)
            (x, y, w, h) = cv2.boundingRect(c)

            stitched = stitched[y:y + h, x:x + w]

            stitched = cv2.cvtColor(stitched, cv2.COLOR_BGR2RGB)
            stitchedImage.append(stitched)
            cv2.imwrite("output.png", stitched)
            print("done crop...")

            # result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            # cv2.imwrite("output not crop.png", result)

        else:
            if status == 1:
                errMsg = "Not Enough Keypoints. \nNeed More Images"

            if status == 2:
                errMsg = "Homography Estimation Fail. \nNot Enough Unique Texture or Object to be Matched"

            if status == 3:
                errMsg = "Camera Parameters Adjust Fail"

            Label(gui, text='Stitching Unsucessful.\n' + errMsg).pack()
    except:
        Label(master=gui, textvariable='Images cannot be stitched').pack()


def main_page():
    label_panorama = ttk.Label(second_frame, text="Panorama Section")
    label_panorama.pack()

    btn_input1 = ttk.Button(second_frame, text="Input 1", command=myInput)
    btn_input1.pack()

    btn_run_stitch = ttk.Button(second_frame, text="Ex Button Click", command=myClick)
    btn_run_stitch.pack()

    slider = Scale(second_frame, from_=1, to=10, orient=HORIZONTAL)
    slider.pack()

    folder_path = str()
    label_fpath = Label(master=second_frame, textvariable=folder_path)
    label_fpath.pack()

    btn_fpath = ttk.Button(second_frame, text="Browse", command=browse_button)
    btn_fpath.pack()

    btn_img_page = ttk.Button(second_frame, text="Show Images Page", command=image_page)
    btn_img_page.pack()

    btn_stitch = ttk.Button(second_frame, text="Run Stitching", command=stitchingImage)
    btn_stitch.pack()

    btn_img_page = ttk.Button(second_frame, text="Show Stitched Images", command=image_page_stitched)
    btn_img_page.pack()


    gui.mainloop()


main_page()

# to run
# python.exe vip-project.py

# to compile
# pyinstaller.exe --onefile --icon=vip-icon.ico vip-project.py
