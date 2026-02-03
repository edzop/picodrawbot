from edlib import myled, mybutton, stepper
import config

import time

time.sleep(0.5)

print("Starting stepper motor test.")

import network
import socket

def connect():
	wlan = network.WLAN(network.STA_IF)
	print("Connecting...")
	wlan.active(True)
	wlan.connect(ssid, password)
	while wlan.isconnected() == False:
		if rp2.bootsel_button() == 1:
			sys.exit()
		print('Waiting for connection...')

		time.sleep(0.5)

	ip = wlan.ifconfig()[0]
	print(f'Connected on {ip}')

	return ip

connect()


#from microdot.asyncio
from microdot import microdot, Response, send_file
#from microdot import utemplate
from microdot.utemplate import Template
from microdot.websocket import with_websocket

app = microdot.Microdot()
Response.default_content_type = 'text/html'

Template.initialize("static")


systemLED = myled.myLED("LED");

CycleCount=0

@app.route('/', methods=['GET', 'POST'])
async def index(request):

	response="OK"

	command="400"
	global CycleCount
	
	systemLED.toggle()
	CycleCount = CycleCount + 1
	
	if request.method == 'POST':
		
		#name = request.form.get('command')
		#return Template('index.html').render(name=name)
		command = request.form.get('command')

		print(f"Command: {command} ")
		
		#response = Template("index.html").render(name=name,title="sd")
		
	#return "dd"
	else:
		print("nop post")
	
	response =  Template('home.html').render(command=command,cyclecount=CycleCount)
		
	return response

@app.get('/shutdown')
def shutdown(request):
	request.app.shutdown()
	return "Shutdown..."

@app.route('/counter')
@with_websocket
async def getcounter(request, ws):
	val=0
	while True:
		time.sleep(.3)
		val=val+1
		await ws.send(str(val))

@app.route("/static/<path:path>")
def static(request,path):
	if ".." in path:
		return "Not Found",404
	return send_file("static/" +path)


  
@app.route('/echo')
@with_websocket
async def echo(request, ws):
	global systemLED
	while True:
		data = await ws.receive()
		print(data)
		systemLED.toggle()
		await ws.send(data)


def web_server():
	try:
		connect()
		app.run(port=8080,debug=True)
	except RuntimeError as e:
		print(e)
		sys.exit()

if __name__ == '__main__':
	web_server()

systemLED.toggle()

print("Finished.")
