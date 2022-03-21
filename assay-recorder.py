# Imports
import RPi.GPIO as gp
import os
import cv2 as cv
import numpy as np
import time


# Probably later want to put this in a module, and have a config file but for now it's fine.
# logging function
def log(string):
    st = "[" + time.strftime("%Y-%m-%d %H:%M:%S",
                             time.localtime()) + "] " + string
    print(st)
    with open("assay-log.txt", "a") as f:
        f.write(st + "\n")


log("==== Starting Assay Recorder ====")

log("Imports Sucessful")

# Define adapter GPIO pins and i2c commands
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


# define function to allow for easy switching of camera
def choose_channel(index):
    channel_info = adapter.get(index)
    if channel_info == None:
        print("Can't get the correct channel info")
    os.system(channel_info["i2c_cmd"])  # i2c write
    gpio_sta = channel_info["gpio_sta"]  # gpio write
    gp.output(7, gpio_sta[0])
    gp.output(11, gpio_sta[1])
    gp.output(12, gpio_sta[2])


camera = cv.VideoCapture(-1)

gp.setwarnings(False)
gp.setmode(gp.BOARD)
gp.setup(7, gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)

log("Camera Adapter Setup Sucessful")
log("Detecting Cameras...")

cameraArray = [0, 0, 0, 0]
print(
    "Automatic Camera Detection currently not working, please enter the camera index manually"
)
cameras = input("Please enter names of cameras plugged in: ").upper()
for i in range(4):
    if chr(i + 65) in cameras:
        cameraArray[i] = 1
# Automatic Detection not working

# create directory for assay data
log("Creating Directories")
home = time.strftime("%Y-%m-%d", time.localtime()) + "-assay"
os.mkdir(home)
for i in ["A", "B", "C", "D"]:
    if cameraArray[ord(i) - 65] == 1:
        os.mkdir(time.strftime("%Y-%m-%d", time.localtime()) + "-assay/" + i)
log("Finished Creating Directories")

# Main loop
while True:
    log("Starting periodic capture...")
    for i in ["A", "B", "C", "D"]:
        if cameraArray[ord(i) - 65] == 1:
            choose_channel(i)
            time.sleep(1)
            ret, frame = camera.read()

            cv.imwrite(
                home + "/" + i + "/" +
                time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + "-" +
                i + ".jpg", frame)

            # Can add analysis here, or save and add later (async during sleeping time)

            log("Captured image from camera " + i)
    log("Ended Capture, sleeping for 15 minutes...")
    time.sleep(60 * 15)
