import cv2
import numpy as np
import argparse
import time
import os

def main(): 
	pass


if __name__ == '__main__' :
	parser = argparse.ArgumentParser(description='Script to run haarcascade detetcion method')
	parser.add_argument("--video", help="path to video file. If empty, camera's stream will be used")
	parser.add_argument("--write", help="Write output to file")
	parser.add_argument("--length", type=int, default=20, help="Max processing time in second for video, default is 20 seconds")
	args = parser.parse_args()

	car_cascade = cv2.CascadeClassifier(os.path.dirname(os.path.realpath(__file__)) + '\\cars.xml')

	if args.video :
				cap = cv2.VideoCapture(args.video)
				nFrames = int(cap.get(7))
				pseudoWidth = int(cap.get(3))
				pseudoHeight = int(cap.get(4))
				fps = cap.get(5)
				bShouldContinue = True
				counter = 30 * args.length

				if args.write :
					fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
					out = cv2.VideoWriter(args.write, fourcc, 30.0, (pseudoWidth,pseudoHeight)) #must be the exact same resolution for MJPG ENCODING

				while counter > 0 :

						if cap.isOpened() :
								ret, frame = cap.read()

								if not ret :
										bShouldContinue = False
										break

								width, heigth = frame.shape[1], frame.shape[0]
								xroi, yroi, wroi, hroi = 5*heigth/12, width/12, 11*heigth/12, 11*width/12
								roi = frame[xroi:wroi, yroi:hroi]

								cv2.putText(frame, "Region of interest", (yroi,xroi-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
								cv2.rectangle(frame, (yroi,xroi),(hroi,wroi),(255,255,255),1)

								gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
								cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(70, 70))

								for (x,y,w,h) in cars :
										cv2.rectangle(roi,(x,y),(x+w,y+h),(0,0,255),4)


								if args.write :
									out.write(frame)
								else :
									cv2.imshow('Cars processed', frame)
									cv2.waitKey(int(1/fps*1000))
								counter -= 1

	else :
				img = cv2.imread(os.path.dirname(os.path.realpath(__file__)) + '\\Ressources' + '\\1.png');
				print(os.path.dirname(os.path.realpath(__file__)) + '\\Ressources' + '\\1.png')
				gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

				print(cars)

				for (x,y,w,h) in cars :
						cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),4)


				cv2.imshow('Cars processed', img)

				if cv2.waitKey() >= 0:
					bShouldContinue = False

cv2.destroyAllWindows()
