#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import cgi

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		
		if self.path == '/client':
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			data = ''
			with open('client.html') as f:
				data = f.read()
			
			self.wfile.write(data)
		elif self.path == '/request':
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			
			self.wfile.write("{'test':'hello world'}")
		
		return
		
	def do_POST(self):
		
		
		#if self.path == '/request':
		self.send_response(200)
		self.send_header('Content-type','text/json')
		self.end_headers()
		
		self.wfile.write("{'test':'hello world'}")

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
