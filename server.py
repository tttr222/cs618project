#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import cgi, learn, json

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		
		if self.path == '/client':
			self.send_response(200)
			self.send_header('Access-Control-Allow-Origin','*')
			self.send_header('Content-type','text/html')
			self.end_headers()
			data = ''
			with open('client.html') as f:
				data = f.read()
			
			self.wfile.write(data)
		elif self.path == '/request':
			self.send_response(200)
			self.send_header('Access-Control-Allow-Origin','*')
			self.send_header('Content-type','text/html')
			self.end_headers()
			
			self.wfile.write("{'test':'hello world'}")
		
		return
		
	def do_POST(self):
		if self.path == '/request':
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				postvars = cgi.parse_multipart(self.rfile, pdict)
			elif ctype == 'application/x-www-form-urlencoded':
				length = int(self.headers.getheader('content-length'))
				postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
			else:
				postvars = {}

			self.send_response(200)
			self.send_header('Access-Control-Allow-Origin','*')
			self.send_header('Content-type','text/json')
			self.end_headers()
			request = str(postvars['text'][0])
			#rsp = "HELLO GELLO, The request was: " + request
			rsp = learn.execute(request)
			obj = {}
			obj['request'] = request
			obj['response'] = rsp
			print obj
			self.wfile.write(json.dumps(obj))

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
