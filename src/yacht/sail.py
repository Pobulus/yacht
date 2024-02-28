from http.server import BaseHTTPRequestHandler, HTTPServer

import time, sys, re, json, os
import importlib, importlib.util
from yacht.convert import convertFile
import yacht.anchor
def createYachtServer(anchorModules):
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
        def do_POST(self):
            items = self.path.split('/')
            
            if(len(items) == 4 and items[1] == 'anchor'):
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                
                
                response = ""
                moduleName = items[2]
                anchorName = items[3]
                try:   
                    response = anchorModules[moduleName].get(anchorName, lambda n: f"{moduleName}:{anchorName} not found")(self)
                    # the anchor can modify headers to alter cookies
                except KeyError:
                    response = f"no such module {moduleName}"
                self.end_headers() 
                self.wfile.write(bytes(response, "utf-8"))
                return YachtServer
            
        def do_GET(self):
            path = "."+self.path;
            if path[-1] == '/':
                path += 'index.yaml'
            print(f"serving file {path}")
            if re.search(r"\.py$", path):
                self.send_response(403)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(f"<html><body><h1>403</h1><hr/><h3>You don't have permission to view {path}</h3></body></html>", "utf-8"))
                return YachtServer  
            try:
                document = convertFile(path,0,[]) if re.search(r"\.ya..?$", path) else open(path).read()
                self.send_response(200)
                self.send_header("Content-type", self.detectContentType(path))
                self.end_headers()
                self.wfile.write(bytes(document, "utf-8"))

                

            except FileNotFoundError:
                if(path == "./anchors.js"):
                    #  if a version of anchors.js was not provided, send a builtin one
                    self.send_response(200)
                    self.send_header("Content-type", "text/plain")
                    self.end_headers()
                    self.wfile.write(bytes(yacht.anchor.anchorsJS, "utf-8"))
                    return YachtServer
                print('File does not exist')
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(f"<html><body><h1>404</h1><hr/><h3>file {path} was not found</h3></body></html>", "utf-8"))
    return YachtServer        
def startServer(args):
    
    serverAddress = "localhost"
    serverPort = 55555

    
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
                            os.chdir(rootPath)
                            sys.path.append(rootPath)
                            print(sys.path)
                        case "-a":
                            serverAddress = args[index+1]
                        case "-m":
                            moduleNames = args[index+1].split(',')
                            for name in moduleNames:
                                try:
                                    spec = importlib.util.spec_from_file_location(name, f"{os.getcwd()}/{name}.py")
                                    mod = importlib.util.module_from_spec(spec)
                                    spec.loader.exec_module(mod)
                                    print(f" ✅ Successfully loaded [{name}]:")
                                    for anch in yacht.anchor._anchorModules[name].keys():
                                        print(f" ⚓  {name}/{anch}")

                                except ModuleNotFoundError:
                                    print(f" ❌ error loading [{name}]")
                                    print(f"No such module {name}")
                                except FileNotFoundError:
                                    print(f" ❌ error loading [{name}]")
                                    print(f"    No such file: {os.getcwd()}/{name}.py")
                        case _:
                            print(f"Unknown parameter {arg}")
                except IndexError:
                    print(f"missing value for parameter {arg}")
    webServer = HTTPServer((serverAddress, serverPort), createYachtServer(yacht.anchor._anchorModules))
    print("Server started http://%s:%s" % (serverAddress, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

if __name__ == "__main__":
    startServer(sys.argv[1:] if len(sys.argv)>1 else []) 