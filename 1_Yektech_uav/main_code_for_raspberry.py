from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
# Import libraries
import RPi.GPIO as GPIO
from time import sleep

import numpy as np

# kütüphane ithal etmek için
cap = PiCamera()

cap.resolution = (1080, 720)
rawCapture = PiRGBArray(cap, size=(1080, 720))


# görüntü yü çekmek için
def getContours(img):
    # kenarları almak için fonksiyon contour ün türkçesi yok sanırım
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # 1kontor bulucudan aldmız değeri contours a ve hierarchy e atıyoruz hiyerarşi katman direk
    # açıklama için link https://docs.opencv.org/3.4/d9/d8b/tutorial_py_contours_hierarchy.html
    # retr externalın açıklaması üsteki linkte  sadece en önde kalan katmanı alıyor diyebilirz
    # approx none da almadığımız detay yok gibi
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # alanı bulcak contours içindeki
        # print(area)
        cv2.drawContours(imgcontour, cnt, -1, (0, 256, 0), 4)
        # contourları çizmesi için bi nevi canvy nin değerini çizio
        if area > 400:
            # eğer çok küçük bi alansa iş yapmasın diye koyduk
            cv2.drawContours(imgcontour, cnt, -1, (0, 256, 0), 4)
            # contourları çizmesi için bi nevi canvy nin değerini çizio
            peri = cv2.arcLength(cnt, True)
            # perimater uzunluk için
            # print(peri)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            # print (approx)
            # bize köşe noktalarını veriyor
            # print("kenar sayisi",len(approx))
            # bu da köşe nin uzunluğunu bi nevi adedi yani
            objCor = (len(approx))
            # print()
            # sonuç olarak objcor direk kaç köşesi olduğu
            x, y, w, h = cv2.boundingRect(approx)
            merkez = (x + (w // 2), y + (h // 2))

            # boundingliyoruz yani bize karenin köşelerinin kordinatlarını alcaz

            # cv2.rectangle(imgcontour,(x,y),(x+w,y+h),(0,255,255),3) bu sanırım kare yapan
            # karenin köşelerini direk kareye alıyor teknik olarak mantıksız gibi ama oranın kordinatları lazım

            # cv2.putText(imgcontour,Objtpye,
            # (x+(w//2)-10,y+(h//2)-10),cv2.FONT_HERSHEY_COMPLEX,0.5,
            # (256,0,0),2)
            # üstüne köşe sayısını yazdrma şart değik bu
            # print("genişlik",w,"yükseklik",h)
            # x başlanıgcı w tamamı genişiğin w bölü iki de ortası yani merkez
            if objCor > 4:
                # üste ve kırmızı ise dicez ama nası
                cv2.line(imgcontour, (x + (w // 2), y + (h // 2)), ((x + (w // 2), 0)), (255, 0, 0), 7)
                # üsteki satır kenara uzaklıklarını çizmek için 4 tane olcak sağ sol yukarı aşşa
                cv2.line(imgcontour, (x + (w // 2), y + (h // 2)), ((x + (w // 2), 900)), (255, 0, 0), 7)
                cv2.line(imgcontour, (x + (w // 2), y + (h // 2)), (0, (y + (h // 2))), (255, 0, 0), 7)
                cv2.line(imgcontour, (x + (w // 2), y + (h // 2)), (900, (y + (h // 2))), (255, 0, 0), 7)
                # img, pt1, pt2, color, thickness=None, lineType=None, shift=None
                cv2.circle(imgcontour, (x + (w // 2), y + (h // 2)), 10, (0, 0, 255), 20)
                merkezx = merkez[0]
                merkezy = merkez[1]
                smerkezx = str(merkezx)
                smerkezy = str(merkezy)

                soluzaklık = (x + w // 2)
                sağuzaklık = (640 - (x + w // 2))
                yukarıuzaklık = (y + (h // 2))
                aşşauzaklık = 480 - (y + (h // 2))
                ssoluzaklık = str(soluzaklık)
                ssağuzaklık = str(sağuzaklık)
                syukarıuzaklık = str(yukarıuzaklık)
                saşşauzaklık = str(aşşauzaklık)

                cv2.putText(imgcontour, "merkezx:", (0, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                cv2.putText(imgcontour, "merkezy:", (0, 425), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                cv2.putText(imgcontour, (smerkezx), (70, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                cv2.putText(imgcontour, (smerkezy), (70, 425), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                # ekranım 640 a 480
                # x sağa y aşşa artıyor
                cv2.putText(imgcontour, "soluzak:", (0, 275), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                cv2.putText(imgcontour, "saguzak:", (0, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                cv2.putText(imgcontour, "yukuzak:", (0, 325), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                cv2.putText(imgcontour, "asuzak:", (0, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

                cv2.putText(imgcontour, (ssoluzaklık), (70, 275), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                cv2.putText(imgcontour, (ssağuzaklık), (70, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                cv2.putText(imgcontour, (syukarıuzaklık), (70, 325), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                cv2.putText(imgcontour, (saşşauzaklık), (70, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

                cv2.circle(imgcontour, (approx[1][0][0], approx[1][0][1]), 10, (255, 0, 0), 20)
                # bu bi tane köşesi çember olduğu için çokta önemli değil bizim için hangisi olması zaten tamamı köşe
                # bi köşeye olan uzaklığı yarıçap banko bir
                # yarıçap çarpı2 direk çap
                # alan için pi r*r
                # çevre için 2 pi r mis

                cv2.line(imgcontour, (x + (w // 2), y + (h // 2)), (approx[1][0][0], approx[1][0][1]), (0, 255, 0), 7)
                # bu yarıçap için
                ycapmerkezx = x + (w // 2) - approx[1][0][0]
                ycapmerkezy = y + (h // 2) - approx[1][0][1]

                yaricapa = (ycapmerkezx * ycapmerkezx + ycapmerkezy * ycapmerkezy)
                yaricapa = np.sqrt(yaricapa)
                cevre = 2 * np.pi * yaricapa
                cemberalan = np.pi * yaricapa * yaricapa

                syaricapa = int(yaricapa)
                scemberalan = int(cemberalan)
                scevre = int(cevre)

                syaricapa = str(syaricapa)
                scemberalan = str(scemberalan)
                scevre = str(scevre)

                cv2.putText(imgcontour, "yaricap:", (0, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                cv2.putText(imgcontour, syaricapa, (70, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                # yaricap
                cv2.putText(imgcontour, "alan:", (0, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                cv2.putText(imgcontour, scemberalan, (70, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                # alan
                cv2.putText(imgcontour, "cevre:", (0, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                cv2.putText(imgcontour, scevre, (70, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                # çevre
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(11, GPIO.OUT)
                pwm = GPIO.PWM(11, 50)

                pwm.start(0)

                def SetAngle(angle):
                    duty = angle / 18 + 2
                    GPIO.output(11, True)
                    pwm.ChangeDutyCycle(duty)
                    sleep(1)
                    GPIO.output(11, False)
                    pwm.ChangeDutyCycle(0)

                SetAngle(80)
                pwm.stop()
                GPIO.cleanup()


while True:
    for frame in cap.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        img = frame.array

        # sonsuz doğru loop

        # mutlak doğru img a okduğmuz değeri atıyoruz
        imgcontour = img.copy()

        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # 0 12 51 233 124 204
        # 0 66 157 255 200 255
        # 0 29 181 255 173 255
        # rengin değeri duruma göre değişmektedir güneş ışığı için ilerde napıcaz bilmiyorum
        lower = np.array([0, 181, 173])
        upper = np.array([29, 255, 255])
        mask = cv2.inRange(imgHSV, lower, upper)

        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        # kopya yaptık ki orjinalin üstünde contour ları göstersin

        imgGray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        # resmi gri yaptık
        imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
        # blurladık
        imgCanny = cv2.Canny(imgBlur, 30, 30)

        # cannyledik bu bi nevi sadece hatları göstermek gibi bişi
        getContours(imgCanny)
        # doğruluk , resim kameranın okduğu değere eşitlendi

        # cv2.imshow("imgcanny",imgCanny)
        cv2.imshow("imgcontour", imgcontour)
        rawCapture.truncate(0)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
# 0 203 159 242 158 255
