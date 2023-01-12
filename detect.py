import cv2
import time
from RPi import GPIO
 
cascade_src = 'cars1.xml'
#line a
ax1=0
ay=180
ax2=640
#line b
bx1=0
by=300
bx2=640
#car num
i = 1
t1=0
z=0
def Speed_Cal(time1):
   #Here i converted m to Km and second to hour then divison to reach Speed in this form (KM/H)
   try:
       Speed = (10*3600)/(time1*1000) + 30
       print("Car Number "+str(i)+" Speed: "+str(Speed)+" KM/H")       
       if Speed > 60:
           GPIO.output(7,1)
           t1= time.time()
           while (time.time() - t1)<1:
               pass
           GPIO.output(7,0)
   except ZeroDivisionError:
       print (5)
     
start_time = time.time()
#video ....
dispW=640
dispH=480
flip=2 #rotate
camSet=' tcpclientsrc host=192.168.0.107 port=8554 ! gdpdepay ! rtph264depay ! h264parse ! nvv4l2decoder  ! nvvidconv flip-method='+str(flip)+' ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+',format=BGR ! appsink  drop=true sync=false '
cam=cv2.VideoCapture(camSet)
car_cascade = cv2.CascadeClassifier(cascade_src) 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
#Save video
cod = cv2.VideoWriter_fourcc(*'XVID')
savevideo = cv2.VideoWriter('savevideo.avi',cod,20.0,(640,480)) 
while True:
   ret, img = cam.read()
   if (type(img) == type(None)):
       break
   blurred = cv2.blur(img,ksize=(15,15))
   gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
   cars = car_cascade.detectMultiScale(gray, 1.1, 2)
 
   cv2.line(img,(ax1,ay),(ax2,ay),(255,255,0),2)
   cv2.line(img,(bx1,by),(bx2,by),(255,0,0),2)
 
   for (x,y,w,h) in cars:
       cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2) 
       cv2.circle(img,(int((x+x+w)/2),int((y+y+h)/2)),1,(0,255,0),-1)
     
       while int(ay-10) <= int((y+y+h)/2) and int(ay+10) >= int((y+y+h)/2):
           start_time = time.time()
           z=1
           print("1")
           break
         
       while int(ay) <= int((y+y+h)/2):
           print("2")
           if int(by-10) <= int((y+y+h)/2) and int(by+10) >= int((y+y+h)/2) and z==1:
               print("Trigger")
               Speed_Cal(time.time() - start_time)
               z=0
           break
   savevideo.write(img)
   cv2.imshow('video', img)
    
   if cv2.waitKey(5) == ord('q'):
       break
cam.release()
savevideo.release()
cv2.destroyAllWindows()
