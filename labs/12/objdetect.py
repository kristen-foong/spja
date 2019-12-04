import cv2
import numpy as np
import pyyolo

darknet_path = 'pyyolo/darknet'
datacfg = 'cfg/coco.data'
cfgfile = 'cfg/yolov3-tiny.cfg'
weightfile = '../yolov3-tiny.weights'

thresh = 0.4
hier_thresh = 0.4
delay = 10
frame = 0

cam = cv2.VideoCapture(-1)
# cam = cv2.VideoCapture("http://192.168.1.23:4747/video")
outputs = []

pyyolo.init(darknet_path, datacfg, cfgfile, weightfile)

while True:
    frame += 1
    _, img = cam.read()

    if frame % 4 == 0:
        height, width, channels = img.shape[:3]
        transposed = img.transpose(2, 0, 1)     # move channels to beginning

        data = transposed.ravel() / 255.0       # linearize and normalize
        data = np.ascontiguousarray(data, dtype=np.float32)
        outputs = pyyolo.detect(width, height, channels, data, thresh, hier_thresh)

    color = (255, 255, 255)
    for output in outputs:
        if output["prob"] >= 0.2:
            color = list(np.random.random(size=3) * 256)
            tl = (output["left"], output["top"])
            cv2.rectangle(img, tl, (output["right"], output["bottom"]), color)
            cv2.putText(img, "{} ({:.2f} %)".format(output["class"], output["prob"] * 100),
                        (tl[0] - 20, tl[1] - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, color)
    cv2.imshow("win", img)
    key = cv2.waitKey(delay) & 0xFF

pyyolo.cleanup()
