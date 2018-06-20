#https://pypi.org/project/colorama/
#pip install colorama
#pip install python-telegram-bot --upgrade

#telegram info https://github.com/python-telegram-bot/python-telegram-bot/blob/master/telegram/bot.py

from colorama import init
init()
from colorama import Fore, Back, Style

import time
import datetime
import sys

from notifier import *
from miner import *

check_interval = 300 #seconds

#TelegramBot Setup
telegramApiKey = ""
#how to find chat
#https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id
#https://api.telegram.org/bot<telegramApiKey>/getUpdates
telegramChatID = 0

miners = []

#example config
#miners.append(Miner('Miner1', '192.168.1.11', 10))
#miners.append(Miner('Miner2', '192.168.1.22', 11)) 

def main():
    
    if telegramApiKey != "":
        print Miner.getDate() + "Telegram setup in progress"
        if telegramChatID != 0:
            print Miner.getDate() + "Telegram chat ID is privided"
        else:
            print Miner.getDate() + "Telegram chat ID is not privided"
        
        #TELEGRAM  INIT
        """Run bot."""
        updater = Updater(telegramApiKey)

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", start))
        dp.add_handler(CommandHandler("list", list))
        
        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(Filters.text, start))
        
        # log all errors
        dp.add_error_handler(error)

        # Start the Bot
        updater.start_polling()

        # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
        # SIGABRT. This should be used most of the time, since start_polling() is
        # non-blocking and will stop the bot gracefully.
        # updater.idle()
        print Miner.getDate() + "Telegram setup done"
  
      

    #RESTARTER INIT
    print Miner.getDate() + "Lets start!"

    if telegramApiKey != "" and telegramChatID != 0:
        updater.bot.send_message(telegramChatID, Miner.getDate() + "Restarter init - lets start!", 0)

    print Miner.getDate() + "Miners to check count: ", len(miners)
    print Miner.getDate() + "Miners check interval: ", check_interval, "seconds"

    if len(miners) == 0:
        print Miner.getDate() + "Nothing to do - no miners in configuration array exitting."
        sys.exit(0)

    while True:
        print "-----------------------------------------------"
        for miner in miners:
            if miner.ping() == True:
                print Fore.GREEN + Miner.getDate() + miner.name + " IP: " + miner.ip + " GPIO: " + str(miner.pin) + " is online" + Fore.RESET
            else:
                if telegramApiKey != "" and telegramChatID != 0:
                    updater.bot.send_message(chatID, Miner.getDate() + miner.name + " is offline - restart attempt", 0)
                print Fore.RED + Miner.getDate() + miner.name + " IP: " + miner.ip + " GPIO: " + str(miner.pin) + " is offline, restart attempt" + Fore.RESET
                miner.restart()
                print Fore.YELLOW + Miner.getDate() + miner.name + " IP: " + miner.ip + " GPIO: " + str(miner.pin) + " restarted" + Fore.RESET
                
        print "Starting timer for ", check_interval, "seconds"
        print "-------------------------------------------"
        time.sleep(check_interval)

if __name__ == '__main__':
    main()
