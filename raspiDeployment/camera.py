import cv2
import time
import keyboard

cam = cv2.VideoCapture(2)

cv2.namedWindow("Intel RealSense webcam screenshot")

img_counter = 0

while True:
    ret,fram = cam.read()
    if not ret:
        print("failed to grab frame")
        break

    cv2.imshow("test", fram)

    # k = cv2.waitKey(1)  ---- this is so the spacebar will take a pic
    
    img_name = f"opencv_frame_{img_counter}.png"
    cv2.imwrite(img_name, fram)
    print(f"screenshot {img_counter} taken")
    img_counter += 1

    time.sleep(20) #wait for 10 seconds

    #exit if Esc is pressed
    if keyboard.is_pressed("esc"):
        print("Closing app")
        break



cam.release()
cv2.destroyAllWindows()

