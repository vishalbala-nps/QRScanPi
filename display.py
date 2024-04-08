from RPLCD.i2c import CharLCD
import sys

try:
	txt = sys.argv[1]
	addr = sys.argv[2]
except Exception as e:
	print("Missing commandline params!")
	exit(1)
lcd = CharLCD(i2c_expander='PCF8574', address=int(addr,0), port=1, cols=16, rows=2, dotsize=8)
lcd.clear()

lcd.write_string(txt)
