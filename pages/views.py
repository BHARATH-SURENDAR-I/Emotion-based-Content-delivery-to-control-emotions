from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .forms import LoginForm,Registrationform
from django.contrib.auth import authenticate, login
import os
from django.urls import path, include
import face_recognition
import cv2 
from imutils.video import VideoStream
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import argparse
import imutils
import time
import cv2
import time
import numpy as np
import gmplot
import time
import geopy
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
from deepface import DeepFace

def facedect(loc):
        cam = cv2.VideoCapture(0)  
        while(True):
            s, img = cam.read()
            cv2.imshow('press c to capture',img)
            if(cv2.waitKey(1) & 0xFF == ord('c')):
                break
        if s:   
                
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                MEDIA_ROOT =os.path.join(BASE_DIR,'pages')

                loc=(str(MEDIA_ROOT)+loc)
                face_1_image = face_recognition.load_image_file(loc)
                print("face_1_image",face_1_image)
                print("loc",loc)
                print("face_encodings",face_recognition.face_encodings(face_1_image))
                face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0]
               # print("face_encodings",face_encodings(face_1_image)[0])

                #

                small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

                rgb_small_frame = small_frame[:, :, ::-1]

                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                if len(face_encodings)==0:
                    return False

                check=face_recognition.compare_faces(face_1_face_encoding, face_encodings)
                cam.release()
                cv2.destroyAllWindows()
                print(check)
                if check[0]:
                        return True

                else :
                    cam.release()
                    cv2.destroyAllWindows()
                    return False   
        else :
            cam.release()
            cv2.destroyAllWindows()
            return False 

       
               
def about(request):
    return render(request,"about.html",{})

def base(request):
        if request.method =="POST":
                form =LoginForm(request.POST)
                if form.is_valid():
                        username=request.POST['email']
                        password=request.POST['password']
                        user = authenticate(request,username=username,password=password)
                        if user is not None:
                            if facedect(user.userprofile.head_shot.url):
                                login(request,user)
                                return redirect('index1')
                            else:
                                return redirect('about')

                        else:
                                return redirect('about')        
        else:
                MyLoginForm = LoginForm()
                return render(request,"base.html",{"MyLoginForm": MyLoginForm})  

def home(request):
   return render(request, 'home.html', {})

#from django.contrib.auth.forms import UserCreationForm



def index(request):
    return render(request,"index.html",{})


def register(request):
        form =Registrationform(request.POST)
        if request.method =="POST":
                
                if form.is_valid():
                        form.save()
                        username=form.cleaned_data['username']
                        password=form.cleaned_data['password1']
                        user = authenticate(username=username,password=password)
                        login(request,user)
                        return redirect('error')
                else:
                        return redirect('index')        

        form =Registrationform()
        return render(request,'registration/register.html',{'form':form})        

def profile(request):
        return render(request,'profile.html',{})


def common(request):
        return render(request,'common.html',{})
def takeimg(request):
    videoCaptureObject =cv2.VideoCapture(0)
    while(True):
        ret,frame=videoCaptureObject.read()
        cv2.imshow('Capturing Video',frame)
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            cv2.imshow("CAPTURED IMAGE",frame)
            n=input("ENTER NAME OF THE PERSON OR FILE:  ")
            n="./prof/"+n+".jpg"
            cv2.imwrite(n,frame)
            videoCaptureObject.release()
            cv2.destroyAllWindows()
            break
    return render(request,'common.html',{})
def index1(request):
    print("success")
    return render(request, 'index1.html',{}) 
def manageemotions(request):
    emo={'sad':0,'angry':0,'surprise':0,'fear':0,'happy':0,'disgust':0,'neutral':0}
    age=0
    font = cv2.FONT_HERSHEY_SIMPLEX
    video_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
    i=0
    while (i<5):
        ret, frame = video_capture.read()
        #"VGG-Face", "Facenet", "OpenFace", "DeepFace"
        #def analyze(img_path, actions = ['emotion', 'age', 'gender', 'race'], models = {}, enforce_detection = True, detector_backend = 'mtcnn'):
        demo=DeepFace.analyze(frame,actions=['emotion','age'])
        result=demo["dominant_emotion"]+","+str(demo["age"])
        emo[demo["dominant_emotion"]]+=1
        age+=demo["age"]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow(result, frame)
        i+=1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print(age/5)
    em=max(emo,key=emo.get)
    print(em)
    video_capture.release()
    cv2.destroyAllWindows()
    if(em=="happy"):
        return render(request, 'happy.html',{}) 
    elif(em=="sad"):
        return render(request, 'sad.html',{}) 
    elif(em=="angry"):
        return render(request, 'angry.html',{}) 
    elif(em=="surprise"):
        return render(request, 'surprise.html',{}) 
    elif(em=="neutral"):
        return render(request, 'neutral.html',{}) 
    elif(em=="fear"):
        return render(request, 'neutral.html',{})
    elif(em=="disgust"):
        return render(request, 'surprise.html',{})

    return redirect('https://www.youtube.com/watch?v=DMrrhhS1BV0')
def drugscheck(request):
    video_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    flag=0
    count=0
    ll=getLocation()
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.reverse(ll)
    f1 = open(".\\location.txt","w+")
    f1.truncate(0)
    f2=open(".\Statistics.txt","w+")
    f2.truncate(0)
    f2.write("Last few Emotions Recognized- Respond Immediately if I am in danger:\n")
    f1.write("Location details:\n")
    f1.write("Address: "+location.raw['display_name']+"\n")
    f1.write("Latitude: "+str(location.raw['lat'])+"\nLongitude: "+str(location.raw['lon'])+ "\n")
    f1.close()
    a,b=zip(*[(location.raw['lat'],location.raw['lon'])])
    gmap = gmplot.GoogleMapPlotter(location.raw['lat'],location.raw['lon'],13)
    gmap.apikey = ''#google map API key
    gmap.scatter(a,b,'#FF0000',size=200,marker=False)
    gmap.draw( "C:\HCI\mysite\map.html")
    while (True and flag==0):
        ret, frame = video_capture.read()
        demo=DeepFace.analyze(frame,actions=['emotion','age'])
        result=demo["dominant_emotion"]+","+str(demo["age"])
        em=demo["dominant_emotion"]
        f2.write(em+"\n")
        if(em=="fear" or em=="anger"):
            count+=1
            if(count>5):
                f2.close()
                email = 'barathsure17'#sender mail address
                password =''#sender mail password 
                send_to_email = 'roshinithangavel@gmail.com'#recevier mail address
                subject = '*****ALERT*****'
                message = '*****I AM IN DANGER, RESCUE ME****'
                file_location = os.getcwd()+'\\Statistics.txt'
                file_location1 = os.getcwd()+'\\location.txt'
                file_location2 = os.getcwd()+'\\map.html'
                msg = MIMEMultipart()
                msg['From'] = email
                msg['To'] = send_to_email
                msg['Subject'] = subject
                msg.attach(MIMEText(message, 'plain'))
                filename = os.path.basename(file_location)
                attachment = open(file_location, "rb")
                part = MIMEBase('application', 'octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= %s" %filename)
                msg.attach(part)
                filename1= os.path.basename(file_location1)
                attachment1 = open(file_location1, "rb")
                part1 = MIMEBase('application', 'octet-stream')
                part1.set_payload((attachment1).read())
                encoders.encode_base64(part1)
                part1.add_header('Content-Disposition', "attachment; filename= %s" %filename1)
                msg.attach(part1)
                filename2= os.path.basename(file_location2)
                attachment2 = open(file_location2, "rb")
                part2 = MIMEBase('application', 'octet-stream')
                part2.set_payload((attachment2).read())
                encoders.encode_base64(part2)
                part2.add_header('Content-Disposition', "attachment; filename= %s" %filename2)
                msg.attach(part2)
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(email, password)
                text = msg.as_string()
                server.sendmail(email, send_to_email, text)
                server.quit()
                flag=1
        cv2.imshow(result, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()
    return render(request, 'index1.html',{})



def getLocation():
    options = Options()
    driver = webdriver.Chrome(executable_path = './chromedriver.exe',options=options)
    timeout = 30
    driver.get("https://mycurrentlocation.net/")
    wait = WebDriverWait(driver, timeout)
    time.sleep(1)
    longitude = driver.find_elements_by_xpath('//*[@id="longitude"]')
    longitude = [x.text for x in longitude]    
    longitude = str(longitude[0])    
    latitude = driver.find_elements_by_xpath('//*[@id="latitude"]')    
    latitude = [x.text for x in latitude]
    latitude = str(latitude[0])
    driver.quit()
    return latitude+","+longitude