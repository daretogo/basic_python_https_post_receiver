from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
import ssl

hostName = "train-effbws1"
hostPort = 443


class ListenToPostandWriteToFile(BaseHTTPRequestHandler):
	def do_POST(self):
		content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
		post_data = self.rfile.read(content_length) # <--- Gets the data itself
		self.send_response(200) # <--- Sends https 200 OK message
		i = 0
		while os.path.exists("alert%s.xml" % i):
			i += 1
		with open("alert%s.xml" % i,'wb') as output:
			output.write(post_data)

httpd = HTTPServer((hostName, hostPort), ListenToPostandWriteToFile)
	
httpd.socket = ssl.wrap_socket (httpd.socket,
		keyfile=r'C:\Users\Administrator\Desktop\train-effbws1.jeppesen.com.20180315-20230315\train-effbws1.jeppesen.com.key',
		certfile=r'C:\Users\Administrator\Desktop\train-effbws1.jeppesen.com.20180315-20230315\train-effbws1.jeppesen.com.crt',
		server_side=True) 

print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
	httpd.serve_forever()
except KeyboardInterrupt:
	pass

httpd.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))