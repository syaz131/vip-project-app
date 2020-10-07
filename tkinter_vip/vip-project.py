from tkinter import filedialog
from tkinter import *
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
from PIL import ImageTk, Image, ImageChops

import os
import numpy as np
import pandas as pd
# from matplotlib import pyplot as plt

import cv2

images = []

gui = Tk()
gui.geometry("1300x650")
style = ThemedStyle(gui)

# gui = ttk.Frame(gui)
style.set_theme("arc")
# style.set_theme("equilux")
style.configure('my.TButton', foreground="white")
gui.title("Panorama and Paint by Number")


def myClick():
    mylabel = ttk.Label(gui, text="myclick clicked")
    mylabel.pack()


# -------- input field ---------
input1 = Entry(gui, width=60)
# input1.insert(0, "Enter Name : ") # default value
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

    # delete

    filename = filedialog.askdirectory()
    folder_path = filename
    lbl_path = ttk.Label(gui, text=folder_path)
    lbl_path.pack()
    print(filename)


def readFolder():
    images.clear()
    folder_path = 'C:/Users/Asus/Pictures/scott folder'
    myList = os.listdir(folder_path)
    print(f'Total no of images detected : {len(myList)}')
    # lbl_path = Label(gui, text=folder_path)
    # lbl_path.pack()
    print(len(images))
    for imgN in myList:
        curImg = cv2.imread(f'{folder_path}/{imgN}')
        curImg = cv2.cvtColor(curImg, cv2.COLOR_BGR2RGB)
        # curImg = cv2.resize(curImg, (0, 0), None, 0.2, 0.2)
        images.append(curImg)

    # for i in range(len(images)):
    #     btn_img = Button(gui, text="Show Image " + str(i))
    #     btn_img.pack()

# def foo(image):
#     image.img = ImageTk.PhotoImage(Image.open("ball.png"))
#     image.canvas.create_image(20,20, anchor=NW, image=self.img)
#     image.canvas.image = self.img

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


def image_page():
    #
    # def forward(img_num):
    #     global label_img
    #     global btn_forward
    #     global btn_back
    #     global myImg
    #
    #     label_img.grid_forget()
    #     imgPil = Image.fromarray(images[img_num - 1].astype('uint8'), 'RGB')
    #     myImg = ImageTk.PhotoImage(imgPil)
    #     label_img = Label(image=imgPil)
    #
    #     # label_img = Label(top, image=myImg).grid(row=0, column=0, columnspan=3)
    #     btn_forward = Button(top, text=">>", command=lambda: forward(img_num + 1))
    #     btn_back = Button(top, text="<<", command=lambda: back(img_num + 1))
    #
    #     label_img.grid(row=0, column=0, columnspan=3)
    #     btn_back.grid(row=1, column=0)
    #     btn_forward.grid(row=1, column=2)
    #
    # def back(img_num):
    #     global label_img
    #     global btn_forward
    #     global btn_back
    #     global myImg
    #
    #     # label_img.grid_forget()
    #
    #     label_img.grid_forget()
    #     imgPil = Image.fromarray(images[img_num - 1].astype('uint8'), 'RGB')
    #     myImg = ImageTk.PhotoImage(imgPil)
    #     label_img = Label(image=imgPil)
    #
    #     btn_forward = Button(top, text=">>", command=lambda: forward(img_num - 1))
    #     btn_back = Button(top, text="<<", command=lambda: back(img_num - 1))
    #
    #     label_img.grid(row=0, column=0, columnspan=3)
    #     btn_back.grid(row=1, column=0)
    #     btn_forward.grid(row=1, column=2)

    # self.toplevel.bind("<Configure>", resize)
    # plt.figure(figsize=(2, 5))

    # for i in range(len(images)):
    # plt.subplot(1, 5, 1), plt.imshow(images[1]), plt.title('Image '+str(1))
    # plt.xticks([]), plt.yticks([])
    # plt.subplot(1, 5, 2), plt.imshow(images[1]), plt.title('Image '+str(2))
    # plt.xticks([]), plt.yticks([])
    # plt.subplot(1, 5, 3), plt.imshow(images[1]), plt.title('Image '+str(3))
    # plt.xticks([]), plt.yticks([])
    # plt.show()

    global myImg

    # for i in range(len(images)):

    # global label_img

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

    # btn_exit = Button(top, text="Exit gallery", command=top.quit)
    # btn_back = Button(top, text="<<", command=back, state=DISABLED)
    # btn_forward = Button(top, text=">>", command=lambda: forward(2))

    # btn_back.grid(row=1, column=0)
    # btn_exit.grid(row=1, column=1)
    # btn_forward.grid(row=1, column=2)



def main_page():
    label_panorama = ttk.Label(gui, text="Panorama Section")
    label_panorama.pack()

    btn_input1 = ttk.Button(gui, text="Input 1", command=myInput)
    # btn_input1 = ttk.Button(gui, text="Input 1", command=myInput, style="my.TButton")
    btn_input1.pack()

    btn_run_stitch = ttk.Button(gui, text="Run Stitching", command=myClick)
    btn_run_stitch.pack()

    slider = Scale(gui, from_=1, to=10, orient=HORIZONTAL)
    slider.pack()

    folder_path = str()
    label_fpath = Label(master=gui, textvariable=folder_path)
    label_fpath.pack()
    # label_fpath.grid(row=0, column=1)
    btn_fpath = ttk.Button(text="Browse", command=browse_button)
    btn_fpath.pack()
    # btn_fpath.grid(row=0, column=3)

    # cv2.imread(folder_path)

    btn_images = ttk.Button(gui, text="Read Folder", command=readFolder)
    btn_images.pack()
    # images = readFolder()

    # btn_show_images = ttk.Button(gui, text="Show Images", command=showImages)
    # btn_show_images.pack()

    btn_img_page = ttk.Button(gui, text="Show Images Page", command=image_page)
    btn_img_page.pack()

    # btn_sec_wind = ttk.Button(gui, text="Open Second Window", command=se)
    # btn_sec_wind.pack()


    gui.mainloop()


main_page()
