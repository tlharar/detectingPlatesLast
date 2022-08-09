import imp
import io
import cv2
import requests
from PIL import Image
from requests_toolbelt import MultipartEncoder
import json
def detectPlates(img):
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pilImage = Image.fromarray(image)
    buffered = io.BytesIO()
    pilImage.save(buffered, quality=100, format="JPEG")
    m = MultipartEncoder(fields={'file': ("imageToUpload", buffered.getvalue(), "image/jpeg")})
    response = requests.post("https://detect.roboflow.com/plate-detect/1?api_key=9yYwopat9oRquPV9pUFm", data=m, headers={'Content-Type': m.content_type})
    h = json.loads(response.text)
    a = h["predictions"]
    try:
        firstPlate = a[0]
        fx = int(firstPlate["x"])
        fy = int(firstPlate["y"])
        fw = int(firstPlate["width"])
        fh = int(firstPlate["height"])
        fc = int(firstPlate["confidence"]*100)
        xSolDeger1 = int(fx - fw/2)
        ySolDeger1 = int(fy+fh/2)
        xSagDeger1 = int(fx+fw/2)
        ySagDeger1 = int(fy-fh/2)
        cv2.rectangle(img,(xSolDeger1,ySolDeger1),(xSagDeger1,ySagDeger1),(0,0,255),2)
        img2 = img[ySagDeger1:ySolDeger1,xSolDeger1:xSagDeger1]
        cv2.imshow("Plate",img2)
        cv2.waitKey()
        cv2.destroyAllWindows()
    except:
        print("plate can't detected")

    
