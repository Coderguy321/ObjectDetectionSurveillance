# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())
 
# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	camera = cv2.VideoCapture(0)
	time.sleep(0.25)
 
# otherwise, we are reading from a video file
else:
	camera = cv2.VideoCapture(args["video"])
 
# initialize the first frame in the video stream
firstFrame = None
count = 0


cap = cv2.VideoCapture(0) # Capture video from camera

# # Get the width and height of frame
# width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)

# Define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use the lower case
# out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (width, height))

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
# frame_width = int(cap.get(3))
# frame_height = int(cap.get(4))
 
# # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
# out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

# Save the Video
# Tip for read the frame size
ret, frame_record = cap.read()
print('ret =', ret, 'W =', frame_record.shape[1], 'H =', frame_record.shape[0], 'channel =', frame_record.shape[2])
FPS= 20.0
FrameSize=(frame_record.shape[1], frame_record.shape[0]) # MUST set or not thing happen !!!! vtest is 768,576.
isColor=1# flag for color(true or 1) or gray (0)
fourcc = cv2.VideoWriter_fourcc(*'X264')
out = cv2.VideoWriter('Video_output.avi', fourcc, FPS, FrameSize)


# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	(grabbed, frame) = camera.read()
	text = "No changed"
 
	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if not grabbed:
		break
 
	# resize the frame, convert it to grayscale, and blur it
	ret, frame_record = cap.read()
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)


 
	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		continue

	if count%30 == 0:
		firstFrame = gray

	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	# (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	# 	cv2.CHAIN_APPROX_SIMPLE)
	image, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 	
	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < args["min_area"]:
			text = "No changed"
			continue

		
		# out.write(frame)

        # # write the flipped frame
        # out.write(frame)
        # cv2.imshow('frame',frame)

		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Change Detected"

		cv2.putText(frame_record, "Room Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
		cv2.putText(frame_record, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
		out.write(frame_record)



	count += 1



	# draw the text and timestamp on the frame
	cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
 
	# show the frame and record if the user presses a key
	cv2.imshow("Security Feed", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break



def on_connect(lbClient, userdata,flags, rc):
	if rc == 0:
		print('Connection established successfully!')
		
		lbClient.subscribe('getUP', 1)
		lbClient.message_callback_add('getUP',getUP)
		print('Subscribing to getUP... To listen for Username and Passwords.')

		lbClient.subscribe('sync', 1)
		lbClient.message_callback_add('sync',sync)
		print('Subscribing to sync... To listen sync Requests.')

		lbClient.subscribe('resetPanel', 1)
		lbClient.message_callback_add('resetPanel',resetPanel)
		print('Subscribing to resetPanel... To resetPanel panel.')
				

def on_disconnect(lbClient, userdata, rc):
	if rc!=0:
		print "Unexpected disconnection!" + str(rc)
	else:
		print "Disconnected Successfully!" +str(rc)

def on_subscribe(lbClient, userdata, mid, granted_qos):
	print("Topic subscribed successfully!")
	

def on_unsubscribe(lbClient, userdata, mid, granted_qos):
	print("unsubscribed successfully!")


def on_publish(lbClient, userdata, mid):
	print "published successfully!"

def getUP(lbClient, userdata, msg):
		global checkNetworkThreadFlag
		checkNetworkThreadFlag = False
		while checkNetworkThreadFlagRunning:
			pass
		#result = checkUP(ssid, pswd, maxtime)  # Pass ssid and pswd received here

		checkNetworkThreadFlag = True

def sync(lbClient, userdata, msg):
		global checkNetworkThreadFlag
		checkNetworkThreadFlag = False
		while checkNetworkThreadFlagRunning:
			pass
		#changeMode(2)
		checkNetworkThreadFlag = True

def resetPanel(lbClient, userdata, msg):
		global checkNetworkThreadFlag
		checkNetworkThreadFlag = False
		while checkNetworkThreadFlagRunning:
			pass
		#changeMode(1)
		checkNetworkThreadFlag = True
############################################################

def removeWiFiConfig():
	print 'Checking if any previous configuration stored?'
	confPresent = True
	while confPresent:
		confFile = open('uConsole_io.txt', 'w')
		subprocess.call('uci get wireless.@wifi-config[0].ssid', shell=True, stdout = confFile)
		confFile.close()
		confFile = open('uConsole_io.txt', 'r')
		line = confFile.read()
		print line
		time.sleep(3)
		
		if not line :
			print 'Not Present.'
			global confPresent
			confPresent = False
		else :
			confFile.seek(0)
			print 'PRESENT!! Deleting it.'
			tss = confFile.readline()
			print tss
			subprocess.call('wifisetup remove -ssid '+line, shell=True) # removing any config present
		confFile.close()
	print 'Removed all previously stored Configurations.'


def resetIface(tssid, tpswd, tauth, tencryp, enableSTA):          # x: wheather to bring up apcli0 after WiFi module reset
	print '\nResetting Apcli0 configuration settings forthe new network.'                    
	subprocess.call( 'uci set wireless.@wifi-iface[0].ApCliSsid={}'.format(tssid), shell=True )
	subprocess.call( 'uci set wireless.@wifi-iface[0].ApCliPassWord={}'.format(tpswd), shell=True )
	subprocess.call( 'uci set wireless.@wifi-iface[0].ApCliAuthMode={}'.format(tencryp), shell=True )
	subprocess.call( 'uci set wireless.@wifi-iface[0].ApCliEncrypType={}'.format(tauth), shell=True )
	subprocess.call( 'uci set wireless.@wifi-iface[0].ApCliEnable={}'.format(enableSTA), shell=True )
	subprocess.call( 'uci commit wireless' , shell=True )
	subprocess.call( 'uci show wireless' , shell=True )
	print '\nReset of Apcli0 configuration COMPLETE.'
	time.sleep(3)


# Updating mosquitto_2.conf to append homeID
def updateSession2ConfigFile(b):   ############################################################
	subprocess.call('sudo rm /etc/mosquitto/mosquitto_2.conf', shell=True)
	file_1 = open('/etc/mosquitto/mosquitto.conf', 'r')
	data_1 = file_1.read()
	file_2 = open('/etc/mosquitto/tempConfig.conf', 'r')
	data_2 = file_2.read()
	file_1.close()
	file_2.close()
	with open('/etc/mosquitto/mosquitto_2.conf', 'a') as file :
		file.write(data_1)
		file.writelines('\n')
		data_2 = data_2.replace('home', b)
		file.write(data_2)
		file.close()



# Kill Tasks
def killTask(task):
	searchTask = "ps w | grep "
	killPID = "kill -9 "
	taskToKill = []
	print "Killing tasks related to : "+task
	fileObj = open('uConsole_killedTasks.txt', 'w')
	subprocess.call(searchTask+task, shell=True, stdout= fileObj)
	fileObj.close()
	fileObj = open('uConsole_killedTasks.txt', 'r')
	for line in fileObj:
		k = line.split()
		taskToKill.append(k[0])
	fileObj.close()
	print "Following are the task PIDs related to {} that need to be killed!!".format(task)
	print taskToKill,"\n\n"
	for i in taskToKill:
		j = killPID + i
		subprocess.call(j, shell=True)
	del taskToKill[:]    # Clearing the list of PIDs killed    

def waitForApcli0Up():
	n = 0
	line = ''
	while not line:
		n = n + 1
		confFile = open('uConsole_io.txt', 'w')
		subprocess.call('ifconfig | grep apcli0', shell=True, stdout = confFile)
		confFile.close()
		confFile = open('uConsole_io.txt', 'r')
		line = confFile.read()
		print "Count : {}".format(n) 
		time.sleep(1)       
	print "APCLI0 MODULE IS UP!!!!!!!!!!!!!"

def waitForApcli0Down():
	n = 0
	line = 'unnova'
	while line:
		n = n + 1
		confFile = open('uConsole_io.txt', 'w')
		subprocess.call('ifconfig | grep apcli0', shell=True, stdout = confFile)
		confFile.close()
		confFile = open('uConsole_io.txt', 'r')
		line = confFile.read()
		print "Count : {}".format(n) 
		time.sleep(1)       
	print "APCLI0 MODULE IS DOWN!!!!!!!!!!!!!"

def waitForRa0Up():
	n = 0
	line = ''
	while not line:
		n = n + 1
		confFile = open('uConsole_io.txt', 'w')
		subprocess.call('ifconfig | grep ra0', shell=True, stdout = confFile)
		confFile.close()
		confFile = open('uConsole_io.txt', 'r')
		line = confFile.read()
		print "Count : {}".format(n) 
		time.sleep(1)       
	print "RA0 MODULE IS UP!!!!!!!!!!!!!"

def waitForRa0Down():
	n = 0
	line = 'unnova'
	while line:
		n = n + 1
		confFile = open('uConsole_io.txt', 'w')
		#subprocess.call('ifconfig | grep ra0', shell=True, stdout = confFile)
		subprocess.call('ifconfig | grep ra0', shell=True, stdout = confFile)
		confFile.close()
		confFile = open('uConsole_io.txt', 'r')
		line = confFile.read()
		print "Count : {}".format(n) 
		time.sleep(1)       
	print "RA0 MODULE IS DOWN!!!!!!!!!!!!!"
	

# Check Username Password
def checkUP(tssid, tpswd, maxTime):
	global apcli0WiFiVerifiedStatus
	global checkNetworkThreadFlag
	checkNetworkThreadFlag = False
	apcli0WiFiVerifiedStatus = False
	subprocess.call('ifconfig apcli0 down', shell=True)
	i = 0

	subprocess.call('rm uConsole_scanResults.json', shell=True)
	subprocess.call("""ubus call onion wifi-scan '{"device":"ra0"}' >> uConsole_scanResults.json """, shell=True)
	print 'Network Scanned. Publishing Results:'
	with open('uConsole_scanResults.json') as scanR :
		data =json.load(scanR)
	listNetworks = data['results']
	n = len(listNetworks)
	print "Number of Networks available: {}.".format(n)
	k = 0
	for j in listNetworks:
		k = k + 1
		print j['ssid']
		if j['ssid'] == tssid:
			pos = k-1
			i = i + 1
			print "Found at index: {}.".format(k)
			break
	if i == 0:
		print "Network not Found!!!"
		checkNetworkThreadFlag = True
		return i
	else:
		print 'Checking connectivity to {}.'.format( listNetworks[pos]['ssid'] )
		print 'Gathering required Network Information..'
		tempSsid = listNetworks[pos]['ssid']
		tempPassWord = tpswd
		tempAuth = listNetworks[pos]['authentication']
		tempEncryp = listNetworks[pos]['encryption']
		print 'SSID:     ',tempSsid
		print 'PassWord: ',tempPassWord
		print 'Auth:     ',tempAuth
		print 'Encryp:   ',tempEncryp

		subprocess.call( 'ifconfig apcli0 down' , shell=True )
		removeWiFiConfig()
		resetIface(tempSsid, tempPassWord, tempAuth, tempEncryp, 1)
		subprocess.call( 'wifi' , shell=True )
		#waitForRa0Carrier()
		waitForApcli0Up()

		print "LETS CHECK FOR IP ADDRESS"
		n = 0
		line = 'unnova'
		while line and n <= maxTime:
			n = n + 1
			print n
			confFile = open('uConsole_io.txt', 'w+')
			subprocess.call('ifconfig | grep apcli0', shell=True, stdout = confFile)
			confFile.seek(0)
			line = confFile.readline()
			confFile.close()
			confFile2 = open('uConsole_io2.txt', 'w+')
			subprocess.call('ip addr | grep apcli0 | grep global', shell=True, stdout = confFile2)
			confFile2.seek(0)
			ip = confFile2.readline()
			confFile2.close()
			print ip
			if ip:
				i = i + 1
				break
			time.sleep(1)

		if i == 1:  
			subprocess.call( 'ifconfig apcli0 down' , shell=True )
			print "No IP alloted. Password Wrong."
			#waitForApcli0Up()
			#subprocess.call( 'ifconfig apcli0 down' , shell=True )
			killTask('wifimanager')
			resetIface( 'abcd', 'abcd', 'abcd', 'abcd', 0)
			return i
		elif i == 2:
			print "IP Address alloted. Connected to network."
			return i
		'''    
		print ('\nMaking Pings...')
		checkP = open('pingResults.txt', 'w')
		pTest=subprocess.Popen('ping google.com >> pingResults.txt', shell=True )
		time.sleep(6)
		pTest.kill()  # Proper way of killing/terminating the task and chek if terminated
		print('Checking Ping Results.')
		checkP.seek(0);
		#if checkP.readline() == 1:
		checkP.close()
		'''


# Thread Subclass
class unnovaThread(threading.Thread):
	def __init__(self, target, args, name = None, daemon = None): # Overridig thread init function
		threading.Thread.__init__(self)     # Parent class init function
		self._target = target
		self._args = args
		self._name = name

	def run(self):
		print "{} has been Triggerred!".format(self._name)
		time.sleep(2)

		try:
			self._target(*self._args) 
		finally:
			del self._target, self._args, self._name
		print "{} has Ended!".format(sef._name)


def checkNetworkThread():      #############################################3
	global ra0ModuleStatus
	global apcli0ModuleStatus
	global session1complete
	global checkNetworkThreadFlag
	global checkNetworkThreadFlagRunning
	while True:
		if checkNetworkThreadFlag:
			checkNetworkThreadFlagRunning = True
			time.sleep(3)
			ra0ModuleStatus = False
			apcli0ModuleStatus = False
			
			netFile = open('uConsole_connectionDetails.txt', 'w+')        
			subprocess.call( 'ifconfig | grep ra0' , shell=True , stdout = netFile )
			eof = netFile.tell()
			if eof != 0:
				ra0ModuleStatus = True
			netFile.seek(0)
			subprocess.call( 'ifconfig | grep apcli0' , shell=True , stdout = netFile )
			eof = netFile.tell()
			if eof != 0:
				apcli0ModuleStatus = True
			netFile.close()


			print "ra0 Module : {}.".format(ra0ModuleStatus)
			print "apcli0 Module : {}.".format(apcli0ModuleStatus)

			if ra0ModuleStatus and session1Complete :
				print 'Session1 Complete. Hence, bringing down Acces Point.'
				subprocess.call( 'ifconfig ra0 down' , shell=True )
				waitForRa0Down()
			elif not ra0ModuleStatus and not session1Complete:
				print 'Session1 incomplete. Bringing up Access Point.'
				subprocess.call( 'ifconfig ra0 up' , shell=True )
				waitForRa0Up()

			if not apcli0ModuleStatus and session1Complete:
				print 'Session1 Complete. Bringing up Station Mode.'
				subprocess.call( 'wifi' , shell=True )
				waitForApcli0Up()
			elif apcli0ModuleStatus and not session1Complete:
				print 'Session1 incomplete. Bringing down Station Mode.'
				subprocess.call( 'ifconfig apcli0 down' , shell=True )
				waitForApcli0Down()
			
			checkNetworkThreadFlagRunning = False


# Change Session
def changeMode(x):   # x = 1 : Change to session 1, x = 2 : Change to session 2
	global checkNetworkThreadFlag
	global checkNetworkThreadFlagRunning
	global session1Complete
	checkNetworkThreadFlag = False  # Need to set this flag after changing mode
	while checkNetworkThreadFlagRunning:
		pass
	subprocess.call( '/etc/init.d/mosquitto stop' , shell=True , stdout = f)
	killTask('mosquitto')
	if x == 1:
		subprocess.call( 'mosquitto -c /etc/mosquitto/mosquitto.conf -d' , shell=True , stdout = f)
		session1Complete = False
	elif x == 2:
		updateSession2ConfigFile(homeid)
		subprocess.call( 'mosquitto -c /etc/mosquitto/mosquitto_2.conf -d' , shell=True , stdout = f)
		session1complete = True
	subprocess.call( '/etc/init.d/mosquitto stop' , shell=True , stdout = f)
	checkNetworkThreadFlag = True

# Initialization
def initState():
	print "Running Initialization Process..."
	global session1Complete
	global lbClient

	'''
	subprocess.call( '/etc/init.d/mosquitto stop' , shell=True )
	subprocess.call('ifconfig wlan0 down', shell=True)
	subprocess.call('ifconfig uap0 down', shell=True)
	'''
	print "Killing old threads and daemons."
	killTask('uScript_init.py')
	killTask('wifimanager')
	killTask('pingResults')
	
	session1Complete = True   # Update session1complete flag. Check from database for session1complete flag
	'''
	if session1Complete:
		changeMode(2)
	else:
		changeMode(1):
	'''
	# Initializing Mqtt Client
	lbClient = mqtt.Client(client_id ="session1",clean_session = True,protocol=mqtt.MQTTv311)
	#lbClient.username_pw_set("unnova","unnovaclient")
	lbClient.on_connect = on_connect
	lbClient.on_disconnect = on_disconnect
	lbClient.on_publish = on_publish
	lbClient.on_subscribe = on_subscribe
	lbClient.on_unsubscribe = on_unsubscribe

t_checkNetwork = unnovaThread(target=checkNetworkThread, args=(), name ='checkNetworkThread')
 
# cleanup the camera and close any open windows
out.save()
out.release()
cap.release()
camera.release()
cv2.destroyAllWindows()