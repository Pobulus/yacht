from http.server import BaseHTTPRequestHandler, HTTPServer
import time, sys
from convert import convertFile
hostName = "localhost"
serverPort = 42069

rootPath = ""

class YachtServer(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path;
        if path[-1] == '/':
            path += 'index.yaml'
        path = rootPath+path

        try:
            print("serving file ")
            document = convertFile(path)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(document, "utf-8"))

        except FileNotFoundError:
            print('File does not exist')
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(f"<html><body><h1>404</h1><hr/><h3>file {path} was not found</h3></body></html>", "utf-8"))
        

if __name__ == "__main__":
    rootPath = sys.argv[1] if len(sys.argv)>1 else "." 
    webServer = HTTPServer((hostName, serverPort), YachtServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")