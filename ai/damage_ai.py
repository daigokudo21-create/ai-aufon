
import cv2
import numpy as np
import requests
from PIL import Image
from io import BytesIO

def detect_damage(image_url):

    try:

        r=requests.get(image_url)

        img=Image.open(BytesIO(r.content))

        img=np.array(img)

        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        edges=cv2.Canny(gray,100,200)

        score=edges.sum()

        if score>500000:

            return "screen"

        return "unknown"

    except:

        return "unknown"
