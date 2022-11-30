from durakonline import durakonline
from datetime import datetime
from threading import Thread
from colorama import init
from colorama import Fore, Back, Style
import time
import json

def read(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

cfg = read("config.json")
MAIN_TOKEN: str = cfg["MAIN"]
BOT_TOKEN: str = cfg["BOT"]
BET: str = cfg["bet"] 
PASSWORD: str = cfg["pw"]
servers =["u1","u2","u3","u4","u5"]
DEBUG_MODE = False
FULL_STOP = False


init()
def s_log(msg: str, delay: float):
    for i in msg:
        print(i, end="", flush=True)
        time.sleep(delay)
    print()
s_log(Fore.RED + ">> [CONSOLE] Durak-Farm software started..\n>> [INFO] Version 1.0\n>> [Author] t.me/nawum\n" + Style.RESET_ALL, 0.06)



def start_game(main, bot, s) -> None:
    global FULL_STOP

    game = bot.game.create(BET, PASSWORD, 2, 36, ch=True, fast=True)
    
    main.game.join(PASSWORD, game.id)
    main._get_data("game")
    for i in range(bot.info['points']//BET):
        main.game.ready()
        bot.game.ready()
        if FULL_STOP:
            time.sleep(1)
            
            bot.game.surrender()
            break
        print(f">> [Thread-{s}]:[{datetime.now().strftime('%H:%M:%S')}] Game {i+1}")
        for card in range(4):
            try:
                main_cards = main._get_data("hand")["cards"]
            except:
                pass
            try:
                bot_cards = bot._get_data("hand")["cards"]
            except:
                pass
            mode = bot._get_data("mode")
            if mode["0"] == 1:
                bot.game.turn(bot_cards[0])
                time.sleep(0.1)
                main.game.take()
                time.sleep(0.1)
                bot.game._pass()
            else:
                main.game.turn(main_cards[0])
                time.sleep(0.1)
                bot.game.take()
                time.sleep(0.1)
                main.game._pass()
        bot.game.surrender()
        bot._get_data("game_over")
    main.game.leave(game.id)
    bot.game.leave(game.id)    

def main(server) -> None:   
    main = durakonline.Client(MAIN_TOKEN, server_id=server, tag="[MAIN]", debug=DEBUG_MODE, pl="ios")
    bot = durakonline.Client(BOT_TOKEN, server_id=server, tag="[BOT]", debug=DEBUG_MODE, pl="ios")
    start_game(main = main, bot = bot, s = server)
    main.close_connection()
    bot.close_connection()

            
i = 0
for serv in servers:
    i += 0.5
    drain_Thread = Thread(target=main, args=(serv,))
    drain_Thread.daemon = True
    drain_Thread.start()
    time.sleep(i)


while not FULL_STOP:
    inp = input("<< Type stop to stop lmao: ")
    if inp=="stop":
        FULL_STOP=True
        