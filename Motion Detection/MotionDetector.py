import cv2, time
import pandas
from datetime import datetime


firstFrame = None
#Need two items so when comparing later on in loop it doesnt give an error (lines 66 & 70)
statusList= [None,None]

times=[]
df = pandas.DataFrame(columns = ["Start", "End"])

#put path to video or 0,1,2,etc. for webcam
#Turns webcam on
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    
    #data from webcam stored in frame
    #check is bool set to True when cam is on and False when cam is off
    check, frame = video.read()
    
    #status is zero unless there is motion detected
    status = 0

    #changing image to gray and then blurring it
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21),0)

    #setting the first frame
    if firstFrame is None:
        firstFrame = gray
        continue
    
    #Creating the difference frame
    deltaFrame = cv2.absdiff(firstFrame,gray)

    #Making the deltaFrame black or white based on difference threshhold, 
    #returns a tuple with thresh info in first item and new frame in second
    threshDelta = cv2.threshold(deltaFrame, 30, 255, cv2.THRESH_BINARY)[1]
    
    #Makes the Black and white clearer
    threshDelta = cv2.dilate(threshDelta, None, iterations = 2)
    
    #Find the contours in frame
    (contours,_) = cv2.findContours(threshDelta.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for cont in contours:
        #If the area of motion is big enough then it will be recognized otherwise it is ignored
        if cv2.contourArea(cont) < 5000:
            continue
        
        #Shows that motion is detected
        status = 1
        
        #draws a rectangle around the motion
        (x,y,w,h) = cv2.boundingRect(cont)
        cv2.rectangle(frame,(x,y), (x+w,y+h), (0,0,255), 3)

    statusList.append(status)
    
    #makes the list only the last two items, saves memory if camera is on for a while
    statusList = statusList[-2:]

    #adds time to list when motion is detected
    if statusList[-1] == 1 and statusList[-2] == 0:
        times.append(datetime.now())
    
    #adds time to list when motion goes away
    if statusList[-1] == 0 and statusList[-2] == 1:
        times.append(datetime.now())
    
    #The outputs from the different frames
    cv2.imshow("True Capture", frame)
    cv2.imshow("Blurry Frame", gray)
    cv2.imshow("Delta Frame", deltaFrame)
    cv2.imshow("Threshold Frame", threshDelta)
    
    #Refreshes the frame being taken every 1ms
    key = cv2.waitKey(1)

    #closes loop when q is pressed
    if key == ord('q'):     
        #Makes so there is always an even number of times in list
        #even if camera is closed while there is motion
        if status == 1:
            times.append(datetime.now())
        break

#puts the times of motion into a dataframe so it can be turned into a csv file    
for i in range(0, len(times), 2):
    df = df.append({"Start":times[i],"End":times[i+1]}, ignore_index = True)    

#makes df into a csv file.
df.to_csv("Times.csv")

#closes camera and the frame windows
video.release()
cv2.destroyAllWindows()
