import tensorflow as tf
import os
import cv2
import numpy as np
from keras.models import load_model
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
video_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
font = cv2.FONT_HERSHEY_SIMPLEX
flag=0
count=0
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
ll=getLocation()
locator = Nominatim(user_agent="myGeocoder")
location = locator.reverse(ll)
f1 = open(".\\location.txt","w+")
f1.truncate(0)
f1.write("Location details:\n")
f1.write("Address: "+location.raw['display_name']+"\n")
f1.write("Latitude: "+str(location.raw['lat'])+"\nLongitude: "+str(location.raw['lon'])+ "\n")
f1.close()
a,b=zip(*[(location.raw['lat'],location.raw['lon'])])
gmap = gmplot.GoogleMapPlotter(location.raw['lat'],location.raw['lon'],13)
gmap.apikey = ''#google map API key
gmap.scatter(a,b,'#FF0000',size=200,marker=False)
gmap.draw( "C:\HCI\mysite\map.html")
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
while (flag==0):
	ret, frame = video_capture.read()
	demo=DeepFace.analyze(frame,actions=['emotion','age'])
	result=demo["dominant_emotion"]+","+str(demo["age"])
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1)
	for (x, y, w, h) in faces:
		demo=DeepFace.analyze(frame,actions=['emotion','age'])
		result=demo["dominant_emotion"]
		print("the person is ", result)
		#cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, 5)
		#face_crop = frame[y:y + h, x:x + w]
		#face_crop = cv2.resize(face_crop, (48, 48))
		#face_crop = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
		#face_crop = face_crop.astype('float32') / 255
		#face_crop = np.asarray(face_crop)
		#face_crop = face_crop.reshape(1, 1, face_crop.shape[0],face_crop.shape[1])
		#cv2.putText(frame, result, (x, y), font, 1, (200, 0, 0), 3, cv2.LINE_AA)
		if(result=="fear" or result=="anger"):
			count+=1
			if(count>5):
				email = ''#sender mail address
				password =''#sender mail password 
				send_to_email = ''#recevier mail address
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
	cv2.imshow('Video', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
video_capture.release()
cv2.destroyAllWindows()
