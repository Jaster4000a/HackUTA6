import cv2
import time
from produceDetection import roboflow
import base64
from mongo_client import Mongo

# # Open the default camera
# cam = cv2.VideoCapture(0)

# # Get the default frame width and height
# frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
# frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

MongoClient = Mongo()

while True:

    # Open the default camera
    cam = cv2.VideoCapture(0)

    # Get the default frame width and height
    frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    ret, frame = cam.read()

    # Write the frame to the output file
    cv2.imwrite("inference.jpeg",frame)

    # Display the captured frame
    cv2.imshow('Camera', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

    # Load base64 encoded image directly from file
    with open("inference.jpeg", "rb") as image_file:
        image_data = image_file.read()
        base64_image = base64.b64encode(image_data).decode("utf-8")

    response=roboflow(base64_image)
    predictions=response["predictions"]
    bounded_image=[]
    if len(predictions) > 0:
        bounded_image=cv2.imread("inference.jpeg")
        for prediction in predictions:
            if prediction['confidence'] > .60:
                
                if bounded_image is None:
                    print("Error: Could not load image.")
                    exit()

                print(bounded_image.shape)
                window_name = "Image"
                x1 = int(prediction['x']-prediction['width']/2)
                y1 = int(prediction['y']-prediction['height']/2)
                x2 = int(prediction['x']+prediction['width']/2)
                y2 = int(prediction['y']+prediction['height']/2)

                thickness = 10
                color = (0,255,0)
                print(f"conf: {prediction['confidence']} x1: {prediction['x']} y1: {prediction['y']} x2: {prediction['x']+prediction['width']} y3: {prediction['y']+ prediction['height']}")
                bounded_image = cv2.rectangle(bounded_image, (x1, y1), (x2,y2),color ,thickness)
        cv2.imwrite("bounded_image.jpeg", bounded_image)

            #mongodb
        current_time = time.time()
   
        DataFromCamera = {
            "Time":current_time,
            "DateTime":time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time)),
            "CVData": {
                "Name":"camera2",
                "lat":32.733372,
                "lon":-97.106638,
                "ApplesWidth":prediction['width']
            }
        }
        print(DataFromCamera)
        MongoClient.insert(DataFromCamera)
        print("Pushed to Mongo!")
    # Release the capture and writer objects
    cam.release()
    #out.release()
    cv2.destroyAllWindows()
    #time.sleep(1)




