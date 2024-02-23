import sys
from yacht.help import describe
from yacht.sail import startServer
from yacht.convert import convertFile
welcomeMessage = """
=== Welcome aboard the yacht! ⛵ ===

"""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(welcomeMessage)
        print("If you don't know how to get started run again with: yacht.help")
        print("or check out the documentation at https://github.com/Pobulus/yacht")
        print("")
        quit()
    command = sys.argv[1]
    match command:
        case "help":
            print(welcomeMessage)
            if len(sys.argv) == 2:
                print("The following modules can be accessed by running yacht <name> or directly as modules with yacht.<name>")
                print("☸ help - display this help message")
                print("☸ sail - setup a simple http server")
                print("☸ convert - generate html from a yaml file")
                print("")
                print("Type yacht help <name> to learn more about each topic")
                print("")
            else:
                describe(sys.argv[2])
                print("")
        case "sail":
            startServer(sys.argv[2:])
        case "convert":
            print(convertFile(sys.argv[2] if len(sys.argv) > 2 else "input.yaml"))
        case _:
            print(f"Unknown command {command}")
            print(f"Try running with help")
            print("")