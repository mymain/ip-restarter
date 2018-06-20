
class Miner:
    def __init__(self, name, ip, pin):
        self.name = name
        self.ip = ip
        self.pin = pin
        self.setPinOutMode()

    def ping(self):
        import os
        import subprocess
        from platform   import system as system_name  # Returns the system/OS name
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """

        # Ping command count option as function of OS
        param = '-n' if system_name().lower()=='windows' else '-c'

        # Building the command. Ex: "ping -c 1 google.com"
        command = ['ping', param, '3', self.ip]

        # Pnging
        with open(os.devnull, 'w') as DEVNULL:
            try:
                subprocess.check_call(
                    command,
                    stdout=DEVNULL,  # suppress output
                    stderr=DEVNULL
                )
                is_up = True
            except subprocess.CalledProcessError:
                is_up = False

            return is_up

    def shutDown(self):
        import os
        import time
        os.system("gpio write " + str(self.pin) + " 0")
        time.sleep(5)
        os.system("gpio write " + str(self.pin) + " 1")
        return True

    def turnOn(self):
        import os
        import time
        os.system("gpio write " + str(self.pin) + " 0")
        time.sleep(0.1)
        os.system("gpio write " + str(self.pin) + " 1")
        return True

    def restart(self):
        import time
        self.shutDown()
        self.turnOn()
        return True 

    def setPinOutMode(self):
        import os
        print self.getDate() + " GPIO: " + str(self.pin) + " mode out, def val: 1"
        os.system("gpio mode " + str(self.pin) + " out")
        os.system("gpio write " + str(self.pin) + " 1")
        return True
    
    def getStatus(self):
        if self.ping() == True:
            return "on"
        else:
            return "off"
    
    @staticmethod 
    def getDate():
        import datetime
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")

