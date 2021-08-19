from deepface import DeepFace
import cv2 
video_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
while (True):
    ret, frame = video_capture.read()
    demo=DeepFace.analyze(frame,actions=['emotion','age'])
    print("Emotion: ",demo["dominant_emotion"])
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()
