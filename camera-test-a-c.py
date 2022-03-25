import RPi.GPIO as gp
import os
import cv2 as cv
import numpy as np
import time


def choose_channel(index):
    channel_info = adapter.get(index)
    if channel_info == None:
        print("Can't get the correct channel info")
    os.system(channel_info["i2c_cmd"])  # i2c write
    gpio_sta = channel_info["gpio_sta"]  # gpio write
    gp.output(7, gpio_sta[0])
    gp.output(11, gpio_sta[1])
    gp.output(12, gpio_sta[2])


adapter = {
    "A": {
        "i2c_cmd": "i2cset -y 0 0x70 0x00 0x04",
        "gpio_sta": [0, 0, 1],
    },
    "B": {
        "i2c_cmd": "i2cset -y 0 0x70 0x00 0x05",
        "gpio_sta": [1, 0, 1],
    },
    "C": {
        "i2c_cmd": "i2cset -y 0 0x70 0x00 0x06",
        "gpio_sta": [0, 1, 0],
    },
    "D": {
        "i2c_cmd": "i2cset -y 0 0x70 0x00 0x07",
        "gpio_sta": [1, 1, 0],
    },
}

camera = cv.VideoCapture(-1)

gp.setwarnings(False)
gp.setmode(gp.BOARD)
gp.setup(7, gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)

#choose_channel("A")
#ret, frame = camera.read()
#if frame:
#	cv.imwrite("A.jpg", frame)

#choose_channel("B")
#ret, frame = camera.read()
#if frame:
#	cv.imwrite("B.jpg", frame)

choose_channel("C")
ret, frame = camera.read()
if frame is not None:
    cv.imwrite("C.jpg", frame)

choose_channel("A")
ret, frame = camera.read()
if frame is not None:
    cv.imwrite("A.jpg", frame)
