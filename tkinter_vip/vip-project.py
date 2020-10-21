from tkinter import filedialog
from tkinter import *
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
import skimage.color as color
from skimage.segmentation import slic
import imutils

import os
import numpy as np
import cv2

images = []
stitchedImage = []
paintedImage = []
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
        if file_name == 'PBN_OUTPUT.png' or file_name == 'PBN_OUTLINE.png':
            Label(third_frame, text="No file ").pack()


# -------- input field ---------
label_paint = ttk.Label(third_frame, text="Paint Section", borderwidth=3, relief="sunken")
label_paint.config(font=('Courier', 13), background='white', width=20, anchor='center')
label_paint.pack(pady=10)


def only_numbers(char):
    return char.isdigit()


validation = gui.register(only_numbers)
input_color = Entry(third_frame, width=30, validate="key", validatecommand=(validation, '%S'))
input_segment = Entry(third_frame, width=30, validate="key", validatecommand=(validation, '%S'))


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

    print('append 1 image : ')
    print(len(images))
    print('\n')


def stitchingImage():
    stitcher = cv2.Stitcher.create()
    stitchedImage.clear()
    print('stitching')

    if len(images) == 1:
        output_name = 'output-panorama.png'
        singleImg = cv2.cvtColor(images[0], cv2.COLOR_BGR2RGB)
        cv2.imwrite(output_name, singleImg)
        Label(second_frame, text='Not Enough Image. Proceed to Paint Section').pack()

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


def SLIC_Kmeans(n_segments, n_colours):
    img_name = 'output-panorama.png'

    image = cv2.imread(img_name)

    try:
        cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    except:
        Label(third_frame, text="No file ").pack()

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # img = stitchedImage[0].copy()

    r = img.shape[0]
    c = img.shape[1]
    segments_slic = slic(img, n_segments=n_segments, sigma=1.0)
    segmented_pano = color.label2rgb(segments_slic, img, kind='avg')
    pixels = np.float32(segmented_pano.reshape(-1, 3))
    # user input number colours
    n_colors = n_colours
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)
    img_rb = np.reshape(labels, (r, c))

    # colourize
    colourize = color.label2rgb(img_rb, img, kind='avg')

    row = colourize.shape[0]
    column = colourize.shape[1]
    dim = colourize.shape[2]
    colourize_reshape = np.reshape(colourize, (row * column, dim))
    unique_colour = np.unique(colourize_reshape, axis=0)

    img_output = cv2.cvtColor(colourize, cv2.COLOR_RGB2BGR)
    paintedImage.clear()
    paintedImage.append(img_output)
    cv2.imwrite("PBN_OUTPUT.png", img_output)
    print("PBN created")

    # Outline
    outline = np.zeros((r, c, 3), np.uint8)
    outline[outline == 0] = 255

    for idx, val in enumerate(unique_colour):
        r = val[0]
        g = val[1]
        b = val[2]
        low_1 = np.array([r, g, b])
        high_1 = np.array([r, g, b])
        # Creaing a mask rom the original image
        mask_1 = cv2.inRange(colourize, low_1, high_1)

        # threshold
        ret, outImg = cv2.threshold(mask_1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        outImg[outImg == 255] = 1

        # contours
        cnts = cv2.findContours(outImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        for c in cnts:
            # compute the center of the contour
            M = cv2.moments(c)
            cX = int(M["m10"] / (M["m00"] + 0.000000001))
            # print(cX)
            cY = int(M["m01"] / (M["m00"] + 0.000000001))
            # print(cY)

            font = cv2.FONT_HERSHEY_SIMPLEX
            index = idx + 1
            # draw the contour and center of the shape on the image
            cv2.drawContours(outline, [c], -1, (0, 0, 0), 1),
            cv2.putText(outline, str(index), (cX, cY), font, 0.5, (0, 0, 0), 1)
            # show the image

    Label(third_frame, text="Paint Success").pack()
    cv2.imwrite("PBN_OUTLINE.png", outline)
    print("Outline created")

    indices = np.argsort(counts)[::-1]
    freqs = np.cumsum(np.hstack([[0], counts[indices] / float(counts.sum())]))
    rows = np.int_(colourize.shape[0] * freqs)
    dom_patch = np.zeros(shape=colourize.shape, dtype=np.uint8)
    for i in range(len(rows) - 1):
        dom_patch[rows[i]:rows[i + 1], :, :] += np.uint8(unique_colour[indices[i]])

    for idx, val in enumerate(unique_colour):
        r = val[0]
        g = val[1]
        b = val[2]
        low_1 = np.array([r, g, b])
        high_1 = np.array([r, g, b])
        # Creating a mask rom the original image
        mask_1 = cv2.inRange(dom_patch, low_1, high_1)

        # contours
        cnts = cv2.findContours(mask_1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        for c in cnts:
            # compute the center of the contour
            M = cv2.moments(c)
            cX = int(M["m10"] / (M["m00"] + 0.000000001))
            # print(cX)
            cY = int(M["m01"] / (M["m00"] + 0.000000001))
            # print(cY)

            font = cv2.FONT_HERSHEY_COMPLEX_SMALL
            index = idx + 1
            # draw the contour and center of the shape on the image
            # cv2.drawContours(img_palette, [c], -1, (0,0,0), 1),
            cv2.putText(dom_patch, str(index), (cX, cY), font, 0.5, (255, 255, 255), 1)
            # show the image

        final_palette = cv2.cvtColor(dom_patch, cv2.COLOR_RGB2BGR)
        cv2.imwrite("PALETTE_OUTPUT.png", final_palette)
        print("PALETTE created")

    os.startfile("PBN_OUTLINE.png")
    os.startfile("PBN_OUTPUT.png")
    os.startfile("PALETTE_OUTPUT.png")


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
    Label(third_frame, text="Insert number of Colours (recommended 10 - 25) : ").pack(pady=10)
    input_color.pack()
    Label(third_frame, text="Insert number of Segments (recommended 300 - 800) : ").pack(pady=10)
    input_segment.pack()

    # ttk.Button(third_frame, text="Start Painting", command=lambda: run_painting(int(input_color.get()))).pack(pady=10)

    ttk.Button(third_frame, text="Start Painting",
               command=lambda: SLIC_Kmeans(int(input_segment.get()), int(input_color.get()))).pack(pady=10)

    output_paint_name = 'PBN_OUTPUT.png'
    btn_paint_output = ttk.Button(third_frame,
                                  text='Open Paint Output',
                                  command=lambda: open_output(output_paint_name))
    btn_paint_output.pack(pady=10)

    output_paintOutline_name = 'PBN_OUTLINE.png'
    btn_paintOutline_output = ttk.Button(third_frame,
                                  text='Open Outline Output',
                                  command=lambda: open_output(output_paintOutline_name))
    btn_paintOutline_output.pack(pady=10)

    output_palette_name = 'PALETTE_OUTPUT.png'
    btn_palette_output = ttk.Button(third_frame,
                                         text='Open Palette Output',
                                         command=lambda: open_output(output_palette_name))
    btn_palette_output.pack(pady=10)

    # ============ File Browse Section
    label_file = ttk.Label(forth_frame, text="File Browse Section", borderwidth=3, relief="sunken")
    label_file.config(font=('Courier', 13), background='white', width=25, anchor='center')
    label_file.pack(pady=10)

    list_frame.pack(pady=10)
    listbox.pack()
    Label(forth_frame, text="Double click on list to open image").pack()

    btn_fpath = ttk.Button(forth_frame, text="Browse", command=browse_button)
    btn_fpath.pack(pady=10)

    gui.mainloop()


main_page()

# to run
# python.exe vip-project.py

# to compile
# pyinstaller.exe --onefile --icon=vip-icon.ico vip-project.py
# pyinstaller.exe --onedir --icon=vip-icon.ico vip-project.py
# pyinstaller.exe --onefile vip-project.py
