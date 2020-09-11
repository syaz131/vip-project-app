try:
    import numpy as np
    import pandas as pd
    import streamlit as st
    import cv2

    from PIL import Image
    from enum import Enum
    from io import BytesIO, StringIO
    from typing import Union



except Exception as e:


    print(e)

STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""


class FileUpload(object):

    def __init__(self):
        self.fileTypes = ["csv", "png", "jpg"]

    def run(self, countFile):
        """
        Upload File on Streamlit Code
        :return:
        """
        st.info(__doc__)
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
    st.image(gray)
    return gray


countFile = 1

if __name__ == "__main__":
    helper = FileUpload()

    # for i in range(0, 2):
    img1 = helper.run(countFile)
    countFile += 1

    if img1 is not None:
        gray1 = img2gray(img1)

    if img1 is not None:
        img2 = helper.run(countFile)
    try:
        img2 = img2
    except NameError:
        print('No Second File')
    else:
        if img2 is not None:
            gray2 = img2gray(img2)
