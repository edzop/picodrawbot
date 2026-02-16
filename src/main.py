
import config
import sys
import rp2

import command_processor
import command_handler


# create a file config.py containing:
# ssid = yourssid
# password = yourpassword

import time

time.sleep(0.5)

print("Starting stepper motor test.")

import network
import socket

def connect():
	wlan = network.WLAN(network.STA_IF)
	print("Connecting...")
	wlan.active(True)
	attempts=0
	wlan.connect(config.ssid, config.password)
	while wlan.isconnected() == False:
		if rp2.bootsel_button() == 1:
			sys.exit()
		print('Waiting for connection...(%d)'%attempts)

		time.sleep(0.5)
		attempts = attempts+1

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



CycleCount=0

@app.route('/', methods=['GET', 'POST'])
async def index(request):

	response="OK"

	command="400"
	global CycleCount
	
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


	
	while True:
		data = await ws.receive()
		print(data)

		response=""

		theCommandProcesser = command_processor.CommandProcessor()

		theCommandProcesser.process_raw_input(data)

		#theCommandProcesser.dump_commands()

		commandlist = theCommandProcesser.get_commands()

		for command in commandlist:
			#print(command)
			response = response + "." + command_handler.handle_command(command)

		await ws.send(response)


def web_server():
	try:
		connect()
		app.run(port=8080,debug=True)
	except RuntimeError as e:
		print(e)
		sys.exit()

if __name__ == '__main__':
	web_server()

print("Finished.")
