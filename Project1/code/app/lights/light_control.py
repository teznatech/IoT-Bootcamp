import threading, os, sys

class LightControl():
    
    def __init__(self):
        self.thread = None

    def lightSwitch(self, red, green, blue, brightness):
        LightControl.thread = threading.Thread(target=self._thread(red, green, blue, brightness))
        LightControl.thread.start()

    def _thread(self, red, green, blue, brightness):
        basedir = os.path.abspath(os.path.dirname(__file__))
        lightFile = os.path.join(basedir, "lightController.py")
        cmd = "sudo python3 " + lightFile + " " +  str(red) + " "\
             + str(green) + " " + str(blue) + " " + str(brightness)
        if int(red) == -1 and int(green) == -1 and int(blue) == -1:
            lightFile = os.path.join("app", "lights", "rainbow.py")
            cmd = "sudo python3 " + lightFile + " " + str(brightness)
        elif int(red) == -2 and int(green) == -2 and int(blue) == -2:
            lightFile = os.path.join("app", "lights", "effects.py")
            cmd = "sudo python3 " + lightFile + " " + str(brightness)
        os.system(cmd)


if __name__ == "__main__":
    light = LightControl()
    light.lightSwitch(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])