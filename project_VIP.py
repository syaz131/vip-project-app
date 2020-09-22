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

# =================== dictionary tak function====================
# @st.cache(allow_output_mutation=True)
def get_static_store() -> Dict:
    """This dictionary is initialized once and can be used to store the files uploaded"""
    return {}

def get_static_image() -> Dict:
    return {}
# =================== dictionary tak function====================


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
            # show_file.image(file)
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
    if isinstance(gray, np.ndarray):
        st.image(gray)
    return gray


def showAnImage(image):
    if isinstance(image, np.ndarray):
        st.image(image)


def showImages(images):
    # if isinstance(images[0], None):
    #     st.warning(len(images))
    #     st.warning(type(images[0]))
    #     st.warning(type(images[1]))

    for i in range(len(images)):
        showAnImage(images[i])


def showMultipleImages(images):
    plt.subplots(1, len(images), figsize=(7, 7))

    # plt.figure(figsize=(5, 5))
    # plt.subplot(131), plt.imshow(img), plt.title('Original')
    # plt.xticks([]), plt.yticks([])
    # plt.show()

    for i in range(len(images)):
        plt.subplot(1, 5, i + 1), plt.imshow(images[i]), plt.title('Image ' + str(i + 1))
        plt.xticks([]), plt.yticks([])

    st.pyplot()


def resizeImage(images):
    for i in range(len(images)):
        if isinstance(images[i], np.ndarray):
            curImg = cv2.resize(images[i], (0, 0), None, 0.2, 0.2)
            images[i] = curImg
    return images


def stichingImage(images):
    result = np.ndarray(shape=(2, 2))
    try:
        images = resizeImage(images)
        stitcher = cv2.Stitcher.create()
        (status, result) = stitcher.stitch(images)
        if status == cv2.STITCHER_OK:
            st.write('Panorama Generated')
            # showAnImage(result)
        else:
            st.write('Panorama Generation Unsuccessful')
    except:
        st.write('Not enough image')
    return result

# =================== function tak function====================
def readFolder():
    static_store = get_static_store()
    static_image = get_static_image()
    file = st.file_uploader("Upload", type=["png", "jpg"])
    if file:
        # Process you file here
        value = file.getvalue()
        # show_file = st.empty()
        # if isinstance(file, BytesIO):
        # show_file.image(file)
        # change from byteIO to array

        # And add it to the static_store if not already in
        if not value in static_image.values():
            static_store[file] = value
            image = Image.open(file)
            img_array = np.array(image)
            static_image[file] = img_array

    else:
        static_image.clear()  # Hack to clear list if the user clears the cache and reloads the page
        st.info("Upload one or more images files.")

    if st.button("Clear file list"):
        static_store.clear()
        static_image.clear()
    if st.checkbox("Show file list?", True):
        st.write(list(static_store.keys()))
    # if st.button('Update Image'):
    #     for bytes in static_store:
    #         image = Image.open(bytes)
    #         img_array = np.array(image)
    #         static_image.append(img_array)
    #     return static_image
# =================== function tak function====================


# ============================ streamlit UI ===========================
colourNumber = st.sidebar.slider('Colour', 1, 10, 2)
colourNumber = int(colourNumber)
# countImage = st.sidebar.number_input('Number of image insert')
countImage = st.sidebar.slider('Number of image', 1, 10, 3)
countImage = int(countImage)
st.set_option('deprecation.showfileUploaderEncoding', False)
# ============================ streamlit UI ===========================

if __name__ == "__main__":

    inputImages = []
    st.title('Panorama and Paint by Numbers')

    st.write('*********')
    st.header('Upload Image Section')
    helper = FileUpload()

    for i in range(0, countImage):
        inputImages.append(helper.run(i))

    # showMultipleImages(inputImages)
    st.subheader('Image Inserted')
    if st.checkbox("Show Images?", True):
        try:
            showImages(inputImages)
        except:
            st.warning('No Image or Not Update Image')

    if st.button('Run Stitching'):
        stitchedImage = stichingImage(inputImages)
        showAnImage(stitchedImage)
