import cv2 
import sys
import json

if len(sys.argv) == 0:
	print("No hintfile specified! Exiting..")
	exit(1)
else:
	try:
		f = json.load(open(sys.argv[1]))
	except:
		print("File not found! Exiting...")
		exit(1)
	try:
		cap = cv2.VideoCapture(int(sys.argv[2]))
	except:
		print("Camera not specified/not found. Attempting to use default camera")
		cap = cv2.VideoCapture(0)
	detector = cv2.QRCodeDetector()
	print("Starting scanner..")
	while True: 
		_, img = cap.read()
		data, bbox, _ = detector.detectAndDecode(img)
		if data:
			print("Scanned data:",data)
			for i in f:
				if i["id"] == data:
					print("Hint is:",i["description"])
					break
			else:
				print("Invalid code!")
