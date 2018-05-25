#!usr/bin/python 

import argparse
import datetime
import imutils
import math
import cv2
import numpy as np

width = 1200
height = 1200 
offsetRefLines = 150
minContour = 8000 #original was 12000

textIn = 0
textOut = 0

# def testIntersectionIn(x, y):
#     #157500  #changing it to 180000, makes it count In first (in the video)
#     res = -450 * x + 400 * y + 157500
#     #print ("this is res in {}").format(res)
#     if((res >= -550) and  (res < 550)):
#         print("printing x: ")
#         print(str(x))
#         print("printing y: ")
#         print(str(y))
#         print("printing res: )")
#         print (str(res))
#         return True
#     return False



# def testIntersectionOut(x, y):
#     #180000 #changing it to 157500 makes it count Out second (in the video)
#     res = -450 * x + 400 * y + 180000  #this last number effects in and out (if both are same num they both in or both out)
#     if ((res >= -550) and (res <= 550)):
#         print("printing x: ")
#         print(str(x))
#         print("printing y: ")
#         print(str(y))
#         print("printing res: )")
#         print (str(res))
#         return True

#     return False
#camera = cv2.VideoCapture("test2.mp4") #testing using a video file 
camera = cv2.VideoCapture(0)  #testing using a webcam feed 
firstFrame = None

# loop over the frames of the video
while True:
    # grab the current frame and initialize the occupied/unoccupied
    # text
    (grabbed, frame) = camera.read()
    text = "Unoccupied"

    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if not grabbed:
        break

    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=width)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    #cnts is the contours which helps detect what is in the frame --> gets passed in the following
    #for loop where the rectangle is then drawn
    _, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < minContour:   #12000           
            # print("Printing contour area: ")
            # print(str(cv2.contourArea(c)))
            continue
            #break 

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # cv2.line(frame, (width / 2, 0), (width, 450), (250, 0, 1), 2) #blue line OUT
        # cv2.line(frame, (width / 2 - 50, 0), (width - 50, 450), (0, 0, 255), 2)#red line IN

        yEnterLine = (height / 3) - offsetRefLines #Line for enter - horizontal 
        yExitLine = (height / 3) + offsetRefLines #Line for exit - horizontal 

        #these two lines only draw the line; does not do anything except to display
        cv2.line(frame, (0, yEnterLine), (width, yEnterLine), (250, 0, 1), 2)
        cv2.line(frame, (0, yExitLine), (width, yExitLine), (0, 0, 225), 2)

        #this is the X and Y center for each object rectangle 
        rectangleXCentroid = ((x + x + w) / 2)
        rectangleYCentroid = ((y + y + w) / 2)
        rectangleCentroid = (rectangleXCentroid, rectangleYCentroid)

        #the red center of the rectangle  
        print ("this is rectangleCenter x {}, y {}").format(x,y)
        cv2.circle(frame, rectangleCentroid, 1, (0, 0, 255), 5) 

        if (checkIn(rectangleYCentroid, yEnterLine, yExitLine))

        # if(testIntersectionIn((x + x + w) / 2, (y + y + h) / 2)):
        #     textIn += 1

        # if(testIntersectionOut((x + x + w) / 2, (y + y + h) / 2)):
        #     textOut += 1

        # draw the text and timestamp on the frame

        # show the frame and record if the user presses a key
        # cv2.imshow("Thresh", thresh)
        # cv2.imshow("Frame Delta", frameDelta)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.putText(frame, "In: {}".format(str(textIn)), (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, "Out: {}".format(str(textOut)), (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    cv2.imshow("Security Feed", frame)


# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
