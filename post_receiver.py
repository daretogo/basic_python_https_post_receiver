from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
import ssl

hostName = "HOSTNAME"  # <--- Can be localhost, or hostname
hostPort = 443


class ListenToPostandWriteToFile(BaseHTTPRequestHandler):
	def do_POST(self):
		content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
		post_data = self.rfile.read(content_length) # <--- Gets the data itself
		self.send_response(200) # <--- Sends https 200 OK message
		i = 0
		while os.path.exists("alert%s.xml" % i):
			i += 1
		with open("alert%s.xml" % i,'wb') as output:    # <---  right now filename ouputs will be alert#.xml, this can be changed here. 
			output.write(post_data)

httpd = HTTPServer((hostName, hostPort), ListenToPostandWriteToFile)
	
httpd.socket = ssl.wrap_socket (httpd.socket,
		keyfile=r'RAW\WINDOWS\PATH\TO\KEY\CERTIFICATE\FILE.KEY',   # <--- note the prepended r'  indicating raw paths
		certfile=r'RAW\WINDOWS\PATH\TO\CERTIFICATE\FILE.CRT',
		server_side=True) 

print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
	httpd.serve_forever()
except KeyboardInterrupt:
	pass

httpd.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
