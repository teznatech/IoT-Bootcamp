import os, json, sys

if __name__ == "__main__":
    lightstat = '/home/pi/IoT-Bootcamp/Project1/code/app/static/record/light-status.json'
    with open(lightstat, "r+") as file:
        file.seek(0)
        json.dump({'status':True,
                    'red': sys.argv[1],
                    'green': sys.argv[2],
                    'blue': sys.argv[3],
                    'brightness': sys.argv[4]
                    }, file)
        file.truncate()