#simple WEB server
#CGI-script
#work dir for script
#Preview\cgi-bin или Preview\htbin
import os, sys

from http.server import HTTPServer, CGIHTTPRequestHandler

Preview = '.'	 # место, где находятся файлы html и подкаталог cgi-bin
port = 8080 		 # http://localhost:80/
os.chdir(Preview) 
srvraddr = ("", port) 
srvrobj = HTTPServer(srvraddr, CGIHTTPRequestHandler)
srvrobj.serve_forever() # infinity loop