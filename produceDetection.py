#from inference_sdk import InferenceHTTPClient
from PIL import Image, ImageDraw, ImageFont
import base64
import time, requests
import configparser
import os
from pathlib import Path

config=configparser.ConfigParser()
config_path=os.path.join(Path.home(),'config.ini')
config.read(config_path)

# docker run -d \
#   --restart always \
#   --network host \
#   -v /home/cabrejos99/Desktop/triton_test/roboflow:/tmp/cache \
#   roboflow/roboflow-inference-server-cpu:0.23.0


API_KEY=config["ROBOFLOW"]["API_KEY"]
URL="http://127.0.0.1:9001"
MODEL_OBJECT_DETECTION="5class-fruit"
MODEL_OBJECT_DETECTION_VERSION=1
def detect_objects(img_str):
    url = f"{URL}/{MODEL_OBJECT_DETECTION}/{MODEL_OBJECT_DETECTION_VERSION}?api_key={API_KEY}"

    start_time = time.time()
    response = requests.post(
        url, data=img_str, headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    #print("Response: ", response.json())
    #print("Received in ", time.time() - start_time, " seconds")

    if response.status_code == 200:
        return response.json()

    #print(f"Warning: Could not get detections for image.")
    return None

#image_filepath="/home/cabrejos99/Desktop/triton_test/roboflow/360_F_245563558_XH9Pe5LJI2kr7VQuzQKAjAbz9PAyejG1.jpg"

# Load image to PIL for cropping once
#image = Image.open(image_filepath)

# Load base64 encoded image directly from file
#with open(image_filepath, "rb") as image_file:
 #   image_data = image_file.read()
   # base64_image = base64.b64encode(image_data).decode("utf-8")

#print(detect_objects(base64_image))
