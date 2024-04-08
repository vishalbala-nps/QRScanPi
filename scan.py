import cv2 
import sys
import json
import configparser
if len(sys.argv) == 0:
	print("No config file specified! Exiting..")
	exit(1)
else:
	cnf = configparser.ConfigParser()
	cl = cnf.read(sys.argv[1])
	if len(cl) == 0:
		print("Config file not found! Exiting")
		exit(1)
	else:
		try:
			camera = int(cnf.get("Options","camera"))
		except:
			camera = 0
		try:
			hints = cnf.get("Options","hints")
		except:
			print("Hints not found! Exiting..")
			exit(1)
		try:
			scanner = cnf.get("Options","scanner")
			if scanner == "pyzbar" or scanner == "zbar":
				from pyzbar.pyzbar import decode
				zbar = True
			else:
				zbar = False
		except:
			zbar = False
	try:
		cap = cv2.VideoCapture(camera)
	except:
		print("Unable to access. Attempting to use default camera")
		cap = cv2.VideoCapture(0)
	try:
		height = cnf.get("Options","height")
	except:
		height = None
	try:
		width = cnf.get("Options","width")
	except:
		width = None
	try:
		wd = cnf.get("Options","window")
		if wd == "yes":
			window = True
		else:
			window = False
	except:
		window = False
	if height != None:
		cap.set(3,int(height))
	if width != None:
		cap.set(4,int(width))
	if zbar:
		print("Using pyzbar")
	else:
		print("Using OpenCV QRCodeDetector")
	try:
		f = json.load(open(hints))
	except:
		print("Hints not found! Exiting..")
		exit(1)
	detector = cv2.QRCodeDetector()
	print("Starting scanner..")
	prv = None
	while True: 
		_, img = cap.read()
		if window:
			cv2.imshow('frame',img)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
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
if window:
	cap.release()
	cv2.destroyAllWindows()
