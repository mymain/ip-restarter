#https://pypi.org/project/colorama/
#pip install colorama
from colorama import init
init()
from colorama import Fore, Back, Style

import time
import datetime
import sys

check_interval = 300 #seconds

def main():
  print Miner.getDate() + "Lets start!"

  miners = []
  
  #example config
  #miners.append(Miner('Miner1', '192.168.1.11', 10))
  #miners.append(Miner('Miner2', '192.168.1.22', 11)) 


  print Miner.getDate() + "Miners to check count: ", len(miners)
  print Miner.getDate() + "Miners check interval: ", check_interval, "seconds"

  if len(miners) == 0:
    print Miner.getDate() + "Nothing to do - no miners in configuration array exitting."
    sys.exit(0)
  
  while True:
    print "-----------------------------------------------------------------------------------------------"
    for miner in miners:
      if miner.ping() == True:
        print Fore.GREEN + Miner.getDate() + miner.name + " IP: " + miner.ip + " GPIO: " + str(miner.pin) + " is online" + Fore.RESET
      else:
        print Fore.RED + Miner.getDate() + miner.name + " IP: " + miner.ip + " GPIO: " + str(miner.pin) + " is offline, restart attempt"
        miner.restart()
        print Fore.GREEN + Miner.getDate() + miner.name + " IP: " + miner.ip + " GPIO: " + str(miner.pin) + " restarted" + Fore.RESET
    print "Starting timer for ", check_interval, "seconds"
    print "-----------------------------------------------------------------------------------------------"
    time.sleep(check_interval)

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
    command = ['ping', param, '1', self.ip]

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

  @staticmethod 
  def getDate():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")

if __name__ == '__main__':
    main()
