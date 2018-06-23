#https://pypi.org/project/colorama/
#pip install colorama
#pip install python-telegram-bot --upgrade

#telegram info https://github.com/python-telegram-bot/python-telegram-bot/blob/master/telegram/bot.py
#telegram exceptions https://github.com/python-telegram-bot/python-telegram-bot/blob/9e7314134e786eb8589b01d7218991e42acc8c03/examples/echobot.py#L48
#wiringpi http://wiringpi.com/

from colorama import init
init()
from colorama import Fore, Back, Style

import time, datetime
import sys, traceback
import telegram, json

from notifier import *
from miner import *

#check_interval = 300 #seconds

#TelegramBot Setup
#telegramApiKey = ""
#how to find chat
#https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id
#https://api.telegram.org/bot<telegramApiKey>/getUpdates
#telegramChatID = 0

with open('config.json') as config_file:
    config = json.load(config_file)

miners = []

for miner in config['Miners']:
    miners.append(Miner(miner['Name'], miner['IP'], miner['GPIO']))

def main():
    try:
        if config['TelegramAPIKey'] != "":
            print Miner.getDate() + "Telegram setup in progress"
            if config['TelegramChatID'] != 0:
                print Miner.getDate() + "Telegram chat ID is privided"
            else:
                print Miner.getDate() + "Telegram chat ID is not privided"
            
            #TELEGRAM  INIT
            """Run bot."""
            updater = Updater(config['TelegramAPIKey'])

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

        if config['TelegramAPIKey'] != "" and config['TelegramChatID'] != 0:
            try:
                updater.bot.send_message(config['TelegramChatID'], Miner.getDate() + "Restarter init - lets start!", 0)
            except telegram.TelegramError as e:
                print Fore.RED + Miner.getDate() + "Telegram messaging exception: " + e.message + Fore.RESET
                time.sleep(1)
            except URLError as e:
                # These are network problems on our end.
                print Fore.RED + Miner.getDate() + "Telegram messaging exception: " + e.message + Fore.RESET
                time.sleep(1)

        print Miner.getDate() + "Miners to check count: ", len(miners)
        print Miner.getDate() + "Miners check interval: ", config['Interval'], "seconds"

        if len(miners) == 0:
            print Miner.getDate() + "Nothing to do - no miners in configuration array exitting."
            sys.exit(0)

        while True:
            print "-----------------------------------------------"
            for miner in miners:
                if miner.ping() == True:
                    print Fore.GREEN + Miner.getDate() + miner.name + " IP: " + miner.ip + " GPIO: " + str(miner.pin) + " is online" + Fore.RESET
                else:
                    if config['TelegramAPIKey'] != "" and config['TelegramChatID'] != 0:
                        try:
                            updater.bot.send_message(config['TelegramChatID'], Miner.getDate() + miner.name + " is offline - restart attempt", 0)
                        except telegram.TelegramError as e:
                            print Fore.RED + Miner.getDate() + "Telegram messaging exception: " + e.message + Fore.RESET
                            time.sleep(1)
                        except URLError as e:
                            # These are network problems on our end.
                            print Fore.RED + Miner.getDate() + "Telegram messaging exception: " + e.message + Fore.RESET
                            time.sleep(1)
                    print Fore.RED + Miner.getDate() + miner.name + " IP: " + miner.ip + " GPIO: " + str(miner.pin) + " is offline, restart attempt" + Fore.RESET
                    miner.restart()
                    print Fore.YELLOW + Miner.getDate() + miner.name + " IP: " + miner.ip + " GPIO: " + str(miner.pin) + " restarted" + Fore.RESET
                    
            print "Starting timer for ", config['Interval'], "seconds"
            print "-------------------------------------------"
            time.sleep(config['Interval'])
    except KeyboardInterrupt:
        print "Shutdown requested...exiting"
        updater.stop()
    except Exception:
        print "Exception... Tracebak: "
        traceback.print_exc(file=sys.stdout)
        updater.stop()
    sys.exit(0)
if __name__ == '__main__':
    main()
