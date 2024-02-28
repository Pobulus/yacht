
def describe(topic):
    match topic:
        case "sail":
            print("sail lets you create a simple http server to test you yacht page")
            print("available parameters are:")
            print(" ☸  -a ADDR     address for the server")
            print(" ☸  -p PORT     port which the server should be opened")
            print(" ☸  -r PATH     path to your server's root directory")
            print(" ☸  -m MOD1[,MOD2[...]]")
            print("         list of modules with anchors to load")
            print("         they should be .py files in root directory of your website")
        case "convert":
            print("convert a given yaml into html and print the results to stdout")

        case _:
            print(f"No help available for {topic}")

if __name__ == "__main__":
    import sys
    try:
        describe(sys.argv[1])
    except IndexError:
        print("This is a help topic for yacht")
        print("available topics are:")
        print(" ☸  sail")
        print(" ☸  convert")
        print(" ☸  anchor")
        
        
