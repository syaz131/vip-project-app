try:
    import numpy as np
    import pandas as pd
    import streamlit as st
    import cv2
    import os

    from PIL import Image
    from enum import Enum
    from io import BytesIO, StringIO
    from typing import Union, Dict

    from matplotlib import pyplot as plt



except Exception as e:

    print(e)

STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""


@st.cache(allow_output_mutation=True)
def get_static_store() -> Dict:
    """This dictionary is initialized once and can be used to store the files uploaded"""
    return {}


class FileUpload(object):

    def __init__(self):
        self.fileTypes = ["csv", "png", "jpg"]

    def run(self, countFile):
        """
        Upload File on Streamlit Code
        :return:
        """
        # st.info(__doc__)
        st.markdown(STYLE, unsafe_allow_html=True)
        file = st.file_uploader("Upload file", type=self.fileTypes, key=countFile)
        show_file = st.empty()
        if not file:
            show_file.info("Please upload a file of type: " + ", ".join(["png", "jpg"]))  # join(["csv", "png", "jpg"])
            return
        content = file.getvalue()
        if isinstance(file, BytesIO):
            show_file.image(file)
            # change from byteIO to array
            image = Image.open(file)
            img_array = np.array(image)
            return img_array
        else:
            data = pd.read_csv(file)
            st.dataframe(data.head(10))
        file.close()


def img2gray(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if isinstance(img[i], np.ndarray):
        st.image(gray)
    return gray


def showAnImage(image):
    if isinstance(image, np.ndarray):
        st.image(image)


def showImages(images):
    for i in range(len(images)):
        showAnImage(images[i])


def showMultipleImages(img):
    plt.subplots(1, len(img), figsize=(7, 7))

    # plt.figure(figsize=(5, 5))
    # plt.subplot(131), plt.imshow(img), plt.title('Original')
    # plt.xticks([]), plt.yticks([])
    # plt.subplot(132), plt.imshow(blur1), plt.title('Averaging Filter')
    # plt.xticks([]), plt.yticks([])
    # plt.subplot(133), plt.imshow(blur2), plt.title('Gaussian Filter')
    # plt.xticks([]), plt.yticks([])
    # plt.show()

    for i in range(len(img)):
        plt.subplot(1, 5, i + 1), plt.imshow(img[i]), plt.title('Image ' + str(i + 1))
        plt.xticks([]), plt.yticks([])

    st.pyplot()


def resizeImage(img):
    for i in range(len(img)):
        if isinstance(img[i], np.ndarray):
            curImg = cv2.resize(img[i], (0, 0), None, 0.2, 0.2)
            img[i] = curImg
    return img


def stichingImage(img):
    result = np.ndarray(shape=(2, 2))
    try:
        img = resizeImage(img)
        stitcher = cv2.Stitcher.create()
        (status, result) = stitcher.stitch(img)
        if status == cv2.STITCHER_OK:
            st.write('Panorama Generated')
            showAnImage(result)
        else:
            st.write('Panorama Generation Unsuccessful')
    except:
        st.write('Not enough image')
    return result


# def file_selector(folder_path='.'):
#     filenames = os.listdir(folder_path)
#     selected_filename = st.selectbox('Select a folder', filenames)
#     return os.path.join(folder_path, selected_filename)

def readFolder():
    images = []
    static_store = get_static_store()
    file = st.file_uploader("Upload", type=["png", "jpg"])
    if file:
        # Process you file here
        value = file.getvalue()
        show_file = st.empty()
        if isinstance(file, BytesIO):
            # show_file.image(file)
            # change from byteIO to array
            image = Image.open(file)
            img_array = np.array(image)
            images.append(img_array)

        # And add it to the static_store if not already in
        if not value in static_store.values():
            static_store[file] = value
    else:
        static_store.clear()  # Hack to clear list if the user clears the cache and reloads the page
        st.info("Upload one or more `.py` files.")

    if st.button("Clear file list"):
        static_store.clear()
        images.clear()
    if st.checkbox("Show file list?", True):
        st.write(list(static_store.keys()))
    if st.button('Upload Images'):
        return images


# =========== streamlit UI =======================
colourNumber = st.sidebar.slider('Colour', 1, 10, 2)
colourNumber = int(colourNumber)
# countImage = st.sidebar.number_input('Number of image insert')
countImage = st.sidebar.slider('Number of image', 1, 10, 2)
countImage = int(countImage)
st.set_option('deprecation.showfileUploaderEncoding', False)

if __name__ == "__main__":
    img = []

    st.title('Panorama and Paint by Numbers')

    st.header('Image from folder')
    img = readFolder()
    # imageFromFolder = readFolder()
    # showImages(imageFromFolder)

    st.write('*********')
    st.header('Upload Image Section')
    # helper = FileUpload()


    # for i in range(0, countImage):
    #     img.append(helper.run(i))

    # showMultipleImages(img)
    st.subheader('Image Inserted')
    st.write(len(img))
    showImages(img)

    if st.button('Run Stitching'):
        stitchedImage = stichingImage(img)
