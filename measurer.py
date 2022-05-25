import cv2
import math
from tkinter import filedialog
import os
import json
from workbook import *

IMG_PATH = "/home/lab/Documents/Работа/1_09.05.22/7_00024.jpg" 

pixel_distance = 0
ref_point = []
size_data = {}

def browse():
    filename = filedialog.askdirectory()
    print(filename)
    return filename

folder_path = browse()

def get_distance(x, y, xc, yc):
    return math.floor((((xc - x )**2) + ((yc-y)**2) )**0.5)

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

def shape_selection(event, x, y, flags, param):
    global pixel_distance
    global ref_point

    if pixel_distance == 0:
        if event == cv2.EVENT_LBUTTONDOWN:
            ref_point = [(x, y)]

        elif event == cv2.EVENT_LBUTTONUP:
            ref_point.append((x, y))
            pixel_distance = get_distance(ref_point[0][0], ref_point[0][1], ref_point[1][0], ref_point[1][1])

            cv2.line(resized, ref_point[0], ref_point[1], (0, 255, 0), 2)
            cv2.putText(resized, str(pixel_distance) + " (1 cm)", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
            cv2.imshow("image", resized)
    else:
        if event == cv2.EVENT_LBUTTONUP:
            ref_point.append((x, y))
            if len(ref_point) % 2 == 0:
                length = get_distance(ref_point[-1][0], ref_point[-1][1], ref_point[-2][0], ref_point[-2][1])
                cv2.line(resized, ref_point[-1], ref_point[-2], (0, 255, 0), 1)
                cv2.putText(resized, str(length) + " (" + str(length / pixel_distance)[:4] + " cm)", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
                cv2.imshow("image", resized)


for filename in os.listdir(folder_path):
    f = os.path.join(folder_path, filename)
    if os.path.isfile(f) and f[-4:] == ".jpg":
        print(f)

        image = cv2.imread(f)

        scale_percent = 30
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)

        resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        #resized = increase_brightness(resized, value=40)
        cv2.imshow("image", resized)
        cv2.setMouseCallback("image", shape_selection)
        k = cv2.waitKey(0)
        size_data[f] = {'cm': pixel_distance, 'points': ref_point, 'pixel_lengths': [get_distance(ref_point[i][0], ref_point[i][1], ref_point[i+1][0], ref_point[i+1][1]) for i in range(0, len(ref_point), 2)]}
        size_data[f]['cm_lengths'] = [(pixel_length / pixel_distance) for pixel_length in size_data[f]['pixel_lengths']]
        if k == 32:
            dump = json.dumps(size_data)
            f = open("size_data.json", "w")
            f.write(dump)
            print(dump)
            f.close()
            write_excel(size_data)
        #print(pixel_distance)
        #print(ref_point)
        
        pixel_distance = 0
        ref_point = 0

dump = json.dumps(size_data)
f = open("size_data.json", "w")
f.write(dump)
print(dump)
f.close()
write_excel(size_data)