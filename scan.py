import cv2 
import sys
import json
try:
	usez = sys.argv[3]
	if usez == "pyzbar" or usez == "zbar":
		zbar = True
		from pyzbar.pyzbar import decode
	else:
		zbar = False
except:
	zbar = False
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
	cap.set(3,384)
	cap.set(4,288)
	if zbar:
		print("Using pyzbar")
	else:
		print("Using OpenCV QRCodeDetector")
	detector = cv2.QRCodeDetector()
	print("Starting scanner..")
	prv = None
	while True: 
		_, img = cap.read()
		if zbar:
			if len(decode(img)) != 0:
				data = decode(img)[0].data.decode("utf-8")
			else:
				data = ""
				pass
		else:
			data, bbox, _ = detector.detectAndDecode(img)
		if data and prv != data:
			prv = data
			print("Scanned data:",data)
			for i in f:
				if i["id"] == data:
					print("Hint is:",i["description"])
					break
			else:
				print("Invalid code!")
