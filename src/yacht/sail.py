from http.server import BaseHTTPRequestHandler, HTTPServer
import time, sys, re
from convert import convertFile

def createYachtServer(rootPath):
    class YachtServer(BaseHTTPRequestHandler):
        def detectContentType(self, path):
            ext = re.search(f"\.([^.]+)$", path).group(1)
            print(ext)
            match ext:
                case "yaml" | "yml" | "html" | "htm":
                    return "text/html"
                case "css"|"yass":
                    return "text/css"
                case "js":
                    return "text/javascript"
                case _: 
                    return "text/plain"

        def do_GET(self):
            
            path = rootPath+self.path;
            if path[-1] == '/':
                path += 'index.yaml'
            print(f"serving file {path}")
            
            try:
                document = convertFile(path,0,[]) if re.search(r"\.ya..?$", path) else open(path).read()
                self.send_response(200)
                self.send_header("Content-type", self.detectContentType(path))
                self.end_headers()
                self.wfile.write(bytes(document, "utf-8"))

                

            except FileNotFoundError:
                print('File does not exist')
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(f"<html><body><h1>404</h1><hr/><h3>file {path} was not found</h3></body></html>", "utf-8"))
    return YachtServer        
def startServer(args):
    
    serverAddress = "localhost"
    serverPort = 55555
    rootPath = "."
    
    if len(args):
        print(args)
        for index, arg in enumerate(args):
            if arg[0] == '-':
                try:
                    match arg:
                        case "-p":
                            try:
                                serverPort = int(args[index+1])
                            except ValueError:
                                print(f"{args[index+1]} is not a valid port number")
                        case "-r":
                            rootPath = args[index+1]
                        case "-a":
                            serverAddress = args[index+1]
                        case _:
                            print(f"Unknown parameter {arg}")
                except IndexError:
                    print(f"missing value for parameter {arg}")
    webServer = HTTPServer((serverAddress, serverPort), createYachtServer(rootPath))
    print("Server started http://%s:%s" % (serverAddress, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

if __name__ == "__main__":
    startServer(sys.argv[1:] if len(sys.argv)>1 else []) 