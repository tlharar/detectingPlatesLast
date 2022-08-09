import io
import cv2
import requests
from PIL import Image
from requests_toolbelt import MultipartEncoder
import json
from detectPlates import detectPlates
img = cv2.imread(r"C:\Users\tlhar\Desktop\cars_train\00788.jpg")
def detectCars():
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pilImage = Image.fromarray(image)
    buffered = io.BytesIO()
    pilImage.save(buffered, quality=100, format="JPEG")
    m = MultipartEncoder(fields={'file': ("imageToUpload", buffered.getvalue(), "image/jpeg")})
    response = requests.post("https://detect.roboflow.com/car-detecting/1?api_key=9yYwopat9oRquPV9pUFm", data=m, headers={'Content-Type': m.content_type})
    h = json.loads(response.text)
    a = h["predictions"]
    aracSayi = int(len(a))
    cars1=list()

    for i in range(0,aracSayi):
        cars = a[i]
        cars1.append(cars)
        fx = int(cars["x"])
        fy = int(cars["y"])
        fw = int(cars["width"])
        fh = int(cars["height"])
        fc = int(cars["confidence"]*100)
        xSolDeger = int(fx - fw/2)
        ySolDeger = int(fy+fh/2)
        xSagDeger = int(fx+fw/2)
        ySagDeger = int(fy-fh/2)
        img2 = img.copy()
        cv2.rectangle(img2,(xSolDeger,ySolDeger),(xSagDeger,ySagDeger),(0,0,255),2)
        cv2.putText(img = img2,text=str(fc)+"%",org=(xSolDeger+10,ySolDeger-fh+17),fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,fontScale=1.0,color=(0,0,0))
        img2 = img2[ySagDeger:ySolDeger,xSolDeger:xSagDeger]
        img3 = img2.copy()
        cv2.imshow("CAR",img3)
        try:
            detectPlates(img3)
        except:
            print("This car have no plates.")
        cv2.waitKey()
        cv2.destroyAllWindows()
    if len(cars1) == 0:
        print("Any car can't detected but let me look can I find any plates.")
        detectPlates(img)
    else:
        print("There is", aracSayi,"cars in this photo.")

detectCars()