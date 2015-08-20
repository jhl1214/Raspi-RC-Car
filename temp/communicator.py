import serial
import syslog
import time

port = '/dev/ttyACM0'
arduino = serial.Serial(port, 9600, timeout=5)

i = 0
while (i < 2):
	arduino.write('g')
	time.sleep(3)

	arduino.write('r')
	time.sleep(1)

	arduino.write('l')
	time.sleep(1)

	arduino.write('f')
	arduino.write('s')
	time.sleep(3)
	i += 1
else:
	print "terminating"

exit()
