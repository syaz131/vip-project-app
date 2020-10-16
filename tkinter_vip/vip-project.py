from tkinter import filedialog
from tkinter import *
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
from PIL import ImageTk, Image, ImageChops
import imutils

import os
import numpy as np
import cv2

images = []
stitchedImage = [0]
inputNumber = 0

gui = Tk()
gui.geometry("1300x800")
style = ThemedStyle(gui)

style.set_theme("clearlooks")
gui.title("Panorama and Paint by Number")

main_frame = Frame(gui)
main_frame.pack(side=LEFT, fill=BOTH, expand=1)

canvas = Canvas(main_frame)
canvas.pack(side=LEFT, fill=BOTH, expand=1)

scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

second_frame = Frame(canvas, width=800)
canvas.create_window((500, 0), window=second_frame, anchor='n')

third_frame = Frame(canvas)
canvas.create_window((960, 71), window=third_frame, anchor='n')
title = ttk.Label(second_frame, text=" Panorama and Paint by Number ")
title.config(font=('Courier', 20), background='white')
title.pack(pady=15)

forth_frame = Frame(canvas)
canvas.create_window((0, 71), window=forth_frame, anchor='n')

list_frame = Frame(forth_frame, width=30)
# vscrollbar_list = Scrollbar(list_frame, orient=VERTICAL)
# listbox = Listbox(list_frame, yscrollcommand=vscrollbar_list.set)
# vscrollbar_list.config(command=listbox.yview)
# vscrollbar_list.pack(side=RIGHT, fill=Y)
hscrollbar_list = Scrollbar(list_frame, orient=HORIZONTAL)
listbox = Listbox(list_frame, xscrollcommand=hscrollbar_list.set)
hscrollbar_list.config(command=listbox.xview)
hscrollbar_list.pack(side=BOTTOM, fill=X)


def myClick():
    mylabel = ttk.Label(second_frame, text="myclick clicked")
    mylabel.pack()


def open_img(event):
    ind = listbox.curselection()
    image_name = listbox.get(ind)
    os.startfile(image_name)


listbox.bind('<Double-Button>', open_img)

def open_output(file_name):
    try:
        os.startfile(file_name)
    except:
        if file_name == 'output-panorama.png':
            Label(second_frame, text="No file ").pack()
        if file_name == 'output-paint.png':
            Label(third_frame, text="No file ").pack()


# -------- input field ---------
label_paint = ttk.Label(third_frame, text="Paint Section", borderwidth=3, relief="sunken")
label_paint.config(font=('Courier', 13), background='white', width=20, anchor='center')
label_paint.pack(pady=10)
Label(third_frame, text="Insert a number : ").pack(pady=10)


def only_numbers(char):
    return char.isdigit()


validation = gui.register(only_numbers)
input1 = Entry(third_frame, width=30, validate="key", validatecommand=(validation, '%S'))


def browse_button():
    global folder_path

    filename = filedialog.askdirectory()
    folder_path = filename
    lbl_path = Label(forth_frame, text=folder_path)
    lbl_path.pack()
    print(filename)

    images.clear()
    listbox.delete(0, END)
    myList = os.listdir(folder_path)
    print(f'Total no of images detected : {len(myList)}')
    print(len(images))
    for imgN in myList:
        listbox.insert(END, f'{folder_path}/{imgN}')
        curImg = cv2.imread(f'{folder_path}/{imgN}')
        curImg = cv2.cvtColor(curImg, cv2.COLOR_BGR2RGB)
        images.append(curImg)

    # when folder have only 1 image - save that 1 image to stitchedImage
    stitchedImage.clear()
    if len(images) == 1:
        stitchedImage.append(images[0])


def showImages():
    top = Toplevel()
    top.title("Image Insert")

    for i in range(len(images)):
        canvas = Canvas(gui)
        canvas.pack()
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
    Label(top, image=myImg).pack()


def stitchingImage():
    stitcher = cv2.Stitcher.create()
    stitchedImage.clear()
    print('stitching')

    if len(images) == 1:
        Label(second_frame, text='Not Enough Image. Skip to Paint Section').pack()

    try:
        (status, result) = stitcher.stitch(images)
        if status == cv2.STITCHER_OK:
            print('success')

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

            output_name = 'output-panorama.png'
            stitched = cv2.cvtColor(stitched, cv2.COLOR_BGR2RGB)
            stitchedImage.append(stitched)
            cv2.imwrite(output_name, stitched)
            Label(second_frame, text='Stitching Success. \n Save Panorama as output-panorama.png').pack()

            print("done crop...")
            os.startfile(output_name)

            # result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            # cv2.imwrite("output not crop.png", result)

        else:
            if status == 1:
                errMsg = "Not Enough Keypoints. \nNeed More Images"

            if status == 2:
                errMsg = "Homography Estimation Fail. \nNot Enough Unique Texture or Object to be Matched"

            if status == 3:
                errMsg = "Camera Parameters Adjust Fail"

            Label(second_frame, text='Stitching Unsucessful.\n' + errMsg).pack()
    except:
        Label(master=gui, textvariable='Images cannot be stitched').pack()


def run_painting(num):
    # use stitchedImage[0] - RGB
    stitched = stitchedImage[0]
    # stitched = cv2.cvtColor(stitchedImage[0], cv2.COLOR_BGR2RGB)
    cv2.imwrite('terbalik.png', stitched)
    os.startfile('terbalik.png')
    Label(third_frame, text=num).pack()

    # output_name = 'output-paint.png'
    # cv2.imwrite(output_name, stitched)
    # Label(second_frame, text='Stitching Success. \n Save Panorama as output-panorama.png').pack()
    # os.startfile(output_name)



def main_page():
    # =========================== Panorama section
    label_panorama = ttk.Label(second_frame, text="Panorama Section", borderwidth=3, relief="sunken")
    label_panorama.config(font=('Courier', 13), background='white', width=30, anchor='center')
    label_panorama.pack(pady=10)

    btn_stitch = ttk.Button(second_frame, text="Start Stitching", command=stitchingImage)
    btn_stitch.pack(pady=10)

    output_pano_name = 'output-panorama.png'
    btn_pano_output = ttk.Button(second_frame,
                                 text='Open Panorama Output',
                                 command=lambda: open_output(output_pano_name))
    btn_pano_output.pack(pady=10)

    # ============================= Paint section
    input1.pack()
    ttk.Button(third_frame, text="Start Painting", command=lambda: run_painting(int(input1.get()))).pack(pady=10)

    output_paint_name = 'output-paint.png'
    btn_paint_output = ttk.Button(third_frame,
                                  text='Open Paint Output',
                                  command=lambda: open_output(output_paint_name))
    btn_paint_output.pack(pady=10)

    # ============ File Browse Section
    label_file = ttk.Label(forth_frame, text="File Browse Section", borderwidth=3, relief="sunken")
    label_file.config(font=('Courier', 13), background='white', width=25, anchor='center')
    label_file.pack(pady=10)

    list_frame.pack(pady=10)
    listbox.pack()

    btn_fpath = ttk.Button(forth_frame, text="Browse", command=browse_button)
    btn_fpath.pack(pady=10)

    gui.mainloop()


main_page()

# to run
# python.exe vip-project.py

# to compile
# pyinstaller.exe --onefile --icon=vip-icon.ico vip-project.py
