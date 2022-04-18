import cv2
import os
from dotenv import load_dotenv
from datetime import datetime
from pushbullet import Pushbullet

camera = cv2.VideoCapture(0)
average_frame = None
motion = False  # flag used to know when to notify / upload pic
motion_counter = 0

# setup for sending messages to user's phone
load_dotenv()
token = os.getenv('PUSHBULLET_TOKEN')
bullet = Pushbullet(token)
my_phone = bullet.devices[1]  # is a list of all devices connected to pb account, 1 is my phone

while True:
    ret, frame = camera.read()
    # mark time to know when motion was detected
    time = datetime.now().strftime('%A %d %B %Y %I:%M:%S%p')

    # grayscale image to improve accuracy and blur image to reduce background noise
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (21, 21), 0)

    # sets the "background" image if the program has not been run
    if average_frame is None:
        average_frame = blurred.copy().astype('float')

    # gets the average frames from current and past iterations
    cv2.accumulateWeighted(blurred, average_frame, 0.5)
    delta = cv2.absdiff(blurred, cv2.convertScaleAbs(average_frame))

    # displays movement on black and white img, white is a pixel that is different from the average frame.
    threshold = cv2.threshold(delta, 5, 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold, None, iterations=2)  # fills in holes in image

    # finds the edges of the motion
    contours, _ = cv2.findContours(threshold.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # reduces bg noise in img for box placement
        if cv2.contourArea(contour) < 5000:
            continue

        # create box around the motion
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        motion = True  # todo upload photo to dropbox or some form of image hosting to save them

    # adds time to screen
    cv2.putText(frame, time, (5, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 230), 1)

    if motion:
        # only sends notif if there was a large amount of movement in frame
        if motion_counter > 50:
            cv2.imwrite('Frame.jpg', frame)

            with open('Frame.jpg', 'rb') as pic:
                file_data = bullet.upload_file(pic, 'Frame.jpg')

            my_phone.push_note('Movement Detected', 'Movement in basement')
            my_phone.push_file(**file_data)

            # delete file after use
            os.remove('Frame.jpg')
            motion_counter = 0

        motion_counter += 1
        motion = False

    # close out of loop on 'q' press
    if cv2.waitKey(1) == ord('q'):
        break

    cv2.resize(frame, (0, 0), fx=0.2, fy=0.2)
    cv2.imshow('Frame', frame)
    # cv2.imshow('delta', threshold)


camera.release()
cv2.destroyAllWindows()
