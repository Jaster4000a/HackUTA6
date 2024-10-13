
import cv2
import time
import keyboard
from PIL import Image
import os

def percent_green(img_file):
    img = Image.open(img_file)
    pixels = img.load()
    width, height = img.size
    total_green = 0
    for x in range(width):
        for y in range(height):
            rgb = pixels[x, y]
            if rgb[1] > rgb[0] and rgb[1] > rgb[2]:  # If green is the predominant color
                total_green += 1

    percent = total_green / (width * height)
    return percent * 100

cam = cv2.VideoCapture(2)  # Change to the correct index if needed
cv2.namedWindow("Intel RealSense webcam screenshot")
img_counter = 0
saved_images = []  # List to store the filenames of the last 5 images

while True:
    ret, fram = cam.read()
    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("Intel RealSense webcam screenshot", fram)  # Show the camera feed

    # Save the screenshot
    img_name = f"opencv_frame_{img_counter}.png"
    cv2.imwrite(img_name, fram)
    print(f"Screenshot {img_counter} taken")

    # Add the new image filename to the list
    saved_images.append(img_name)

    # Check if there are more than 5 images in the list
    if len(saved_images) > 5:
        # Delete the oldest image
        oldest_image = saved_images.pop(0)
        if os.path.exists(oldest_image):
            os.remove(oldest_image)
            print(f"Deleted oldest image: {oldest_image}")

    # Calculate the percentage of green pixels using the new function
    green_percentage = percent_green(img_name)
    print(f"Percentage of green pixels: {green_percentage:.2f}%")

    img_counter += 1
    time.sleep(5)  # Wait for 20 seconds before taking another picture

    # Exit if Esc key is pressed
    if keyboard.is_pressed("esc"):
        print("Closing app")
        break

# Release the camera and destroy all OpenCV windows
cam.release()
cv2.destroyAllWindows()

