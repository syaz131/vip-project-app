from tkinter import filedialog
from tkinter import *
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
from PIL import ImageTk, Image, ImageChops

import os
import numpy as np
import pandas as pd

import cv2

images = []
stitchedImage = [0]

gui = Tk()
gui.geometry("1300x650")
style = ThemedStyle(gui)

style.set_theme("arc")
style.configure('my.TButton', foreground="white")
gui.title("Panorama and Paint by Number")


def myClick():
    mylabel = ttk.Label(gui, text="myclick clicked")
    mylabel.pack()


# -------- input field ---------
input1 = Entry(gui, width=60)
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


# def readFolder():
#     images.clear()
#     # folder_path = 'C:/Users/Asus/Pictures/scott folder'
#     myList = os.listdir(folder_path)
#     print(f'Total no of images detected : {len(myList)}')
#     print(len(images))
#     for imgN in myList:
#         curImg = cv2.imread(f'{folder_path}/{imgN}')
#         curImg = cv2.cvtColor(curImg, cv2.COLOR_BGR2RGB)
#         # curImg = cv2.resize(curImg, (0, 0), None, 0.2, 0.2)
#         images.append(curImg)


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
    print('s')
    try:
        (status, result) = stitcher.stitch(images)
        if status == cv2.STITCHER_OK:
            print('succ')
            Label(gui, text='Stitching success').pack()
            # stitchedImage = result
            stitchedImage.append(result)
            print(images[0].shape)
            print(stitchedImage.shape)
            print(result.shape)

            # ttk.Button(gui, text="Show Images Page", command=image_page(stitchedImage[0])).pack()

            # print(stitchedImage)
            # image_page(stitchedImage)

        else:
            Label(master=gui, textvariable='Images cannot be stitched').pack()
    except:
        Label(master=gui, textvariable='Images cannot be stitched').pack()




def main_page():
    label_panorama = ttk.Label(gui, text="Panorama Section")
    label_panorama.pack()

    btn_input1 = ttk.Button(gui, text="Input 1", command=myInput)
    btn_input1.pack()

    btn_run_stitch = ttk.Button(gui, text="Ex Button Click", command=myClick)
    btn_run_stitch.pack()

    slider = Scale(gui, from_=1, to=10, orient=HORIZONTAL)
    slider.pack()

    folder_path = str()
    label_fpath = Label(master=gui, textvariable=folder_path)
    label_fpath.pack()

    btn_fpath = ttk.Button(text="Browse", command=browse_button)
    btn_fpath.pack()

    # btn_images = ttk.Button(gui, text="Read Folder", command=readFolder)
    # btn_images.pack()

    btn_img_page = ttk.Button(gui, text="Show Images Page", command=image_page)
    btn_img_page.pack()

    btn_stitch = ttk.Button(gui, text="Run Stitching", command=stitchingImage)
    btn_stitch.pack()

    btn_img_page = ttk.Button(gui, text="Show Stitched Images", command=image_page_stitched)
    btn_img_page.pack()

    gui.mainloop()


main_page()
