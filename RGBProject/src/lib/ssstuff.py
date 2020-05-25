import numpy as np
from PIL import ImageGrab, Image
from mss import mss
import cv2, time, math
from collections import Counter
from sklearn.cluster import KMeans

class breakLoop(Exception): pass

class dominant_color:
    resolution = (80, 80)
    k = 3
    """
    this is a class for extracting dominant color from a numpy image in rgb formatted tuple in high frame rates.
    :param resolution:
        needed for resizing of the input image. Default is (25, 25).Lower values lowers both the accuracy but also calculation time.(set None for no resizing
    :param k:
        k param of the kmeans operation. Default is 3. Lower values Lowers the accuracy
    """
    @classmethod
    def make_solid_image(cls, color):
        shape = cls.resolution
        sample = np.zeros((shape[0], shape[1], 3), np.uint8)
        sample[:] = color
        return sample

    @classmethod
    def get_dominant_color(cls, image):
        k = cls.k
        image_processing_size = cls.resolution
        """
        takes an image as input
        returns the dominant color of the image as a list

        dominant color is found by running k means on the
        pixels & returning the centroid of the largest cluster

        processing time is sped up by working with a smaller image;
        this resizing can be done with the image_processing_size param
        which takes a tuple of image dims as input

        """
        # resize image if new dims provided
        if image_processing_size is not None:
            image = cv2.resize(image, image_processing_size,
                               interpolation=cv2.INTER_AREA)

        # reshape the image to be a list of pixels
        image = image.reshape((image.shape[0] * image.shape[1], 3))

        # cluster and assign labels to the pixels
        clt = KMeans(n_clusters=k)
        labels = clt.fit_predict(image)

        # count labels to find most popular
        label_counts = Counter(labels)

        # subset out most popular centroid
        dominant_color = clt.cluster_centers_[label_counts.most_common(1)[0][0]]

        return list(dominant_color)


    @staticmethod
    def hsv2rgb(color):
        """
        :param color: Color in HSV space.H value is in range of (179, 0) and other values are in range of (0, 255)
        :return: rgb as a tuple in range of (0, 255)
        """
        H_ = float(color[0]/179)
        S_ = float(color[1]/255)
        V_ = float(color[2]/255)

        if S_ == 0.0:
            V_int = int(V_*255)
            return V_int, V_int, V_int

        i = int(H_ * 6.0)  # XXX assume int() truncates!
        f = (H_ * 6.0) - i
        p = int(255 * V_ * (1.0 - S_))
        q = int(255 * V_ * (1.0 - S_ * f))
        t = int(255 * V_ * (1.0 - S_ * (1.0 - f)))
        i = i % 6
        V_int = int(V_*255)
        if i == 0:
            return V_int, t, p
        if i == 1:
            return q, V_int, p
        if i == 2:
            return p, V_int, t
        if i == 3:
            return p, q, V_int
        if i == 4:
            return t, p, V_int
        if i == 5:
            return V_int, p, q
    """ H_n = H_/60
        H_nf = math.floor(H_n)
        Hi = int(H_nf)%6
        f = H_n - H_nf
        p = V_* (1-S_)
        q = V_*(1-f*S_)
        t = V_*(1-(1-f)*S_)

        r, g, b = 0, 0, 0
        if Hi == 0: r, g, b = V_, t, p
        elif Hi == 1: r, g, b = p, V_, t
        elif Hi == 2: r , g, b = p, V_, t
        elif Hi == 3: r, g, b = p, q, V_
        elif Hi == 4: r, g, b = t, p, V_
        elif Hi == 5: r, g, b = V_, p, q
        r, g, b = int(r*255), int(g*255), int(b*255)
        return r, g, b"""


    @classmethod
    def get_dominant_color_from_monitor(cls, monitor=0, img_show=False, wait_key="q", breaks=False):
        """
        Gets screenshot of the specified monitor and return dominant color
        :param monitor: integer specifies which display will the screenshot be taken from. See mss documentation for more info: https://python-mss.readthedocs.io/
            :type: int
        :param img_show: if True, captured image will be visualized
        :param wait_key: (only works when breaks is set to True). When this key is pressed, an breakLoop exception is raised.(Default = "q")
        :param breaks: if set to True, a breakLoop exception is raised.This can be used for handling forever-serve situations
        :return: a tuple of rgb values in range of (0, 255)
        """
        sct = mss()
        sct_img = sct.grab(sct.monitors[1])

        #convert img to cv2 format in HSV space
        img = np.array(sct.grab(sct.monitors[monitor]))
        img_small = cv2.resize(img, cls.resolution,
                           interpolation=cv2.INTER_AREA)

        hsv_oci = cv2.cvtColor(img_small, cv2.COLOR_RGB2HSV)

        #get dominant color
        a = cls.get_dominant_color(hsv_oci)
        return_val = cls.hsv2rgb(a)
        # create a square showing dominant color of equal size to input image
        if img_show:
            dom_color_hsv = cls.make_solid_image(a)
            # convert to bgr color space for display
            dom_color_bgr = cv2.cvtColor(dom_color_hsv, cv2.COLOR_HSV2RGB)
            # concat input image and dom color square side by side for display
            #output_image = np.hstack((img_small, dom_color_bgr))

            # show results to screen
            cv2.imshow('Image Dominant Color', dom_color_bgr)
            if breaks:
                if cv2.waitKey(25) & 0xFF == ord(wait_key):
                    cv2.destroyAllWindows()
                    raise breakLoop
            return return_val
        else:
            return return_val

