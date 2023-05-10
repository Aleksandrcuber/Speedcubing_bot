from src.Recording_struct import *
from src.Answers import *
import json
import telebot

results = 'data/data.json'
chats = 'data/chat.json'
token = "6260535787:AAEBQ_CVSWlPBvDKNBxFFBqRYpvicqA7GQ4"
bot = telebot.TeleBot(token)


class PlayerError(Exception):
    pass


class EventError(Exception):
    pass


def decode_object(dic):
    if 'comment' not in dic.keys():
        return dic
    seconds = str(dic['seconds'])
    mils = str(dic['mils'])
    if len(seconds) == 1:
        seconds = '0' + seconds
    if len(mils) == 1:
        mils = '0' + mils
    string = f"{dic['minutes']}:{seconds}:{mils} {dic['comment']}"
    return Record(string)


def add_solve(message):
    user_id = message.chat.id
    player = get_player(user_id)
    if player == '':
        raise PlayerError
    event = get_event(user_id)
    if event == '':
        raise EventError

    data = open(results, 'r')
    current = json.load(data, object_hook=decode_object)
    try:
        solve = Record(message.text)
    except ValueError:
        incorrect_format(user_id)
        return
    current[player][event]["solves"].append(solve)
    bot.send_message(user_id, solve_added)
    if current[player][event]["best"] >= solve:
        if len(current[player][event]["solves"]) > 1:
            new_best(user_id, current[player][event]["best"] - solve)
        current[player][event]["best"] = solve
    for n in [5, 12, 50, 100]:
        avg = count_avg(current[player][event]["solves"], n)
        current[player][event][f"bao{n}"] = min(current[player][event][f"bao{n}"], avg)
    data = open(results, "w")
    json.dump(current, data, default=lambda x: x.__dict__)


def add_new_user(nickname, password):
    data = open(results, "r")
    current = json.load(data, object_hook=decode_object)
    current[nickname] = {
        "password": password,
        "3x3 two-handed": {
            "solves": [],
            "best": Record("100000:00:00"),
            "bao5": Record("100000:00:00"),
            "bao12": Record("100000:00:00"),
            "bao50": Record("100000:00:00"),
            "bao100": Record("100000:00:00")
        },
        "3x3 one-handed": {
            "solves": [],
            "best": Record("100000:00:00"),
            "bao5": Record("100000:00:00"),
            "bao12": Record("100000:00:00"),
            "bao50": Record("100000:00:00"),
            "bao100": Record("100000:00:00")
        },
        "2x2": {
            "solves": [],
            "best": Record("100000:00:00"),
            "bao5": Record("100000:00:00"),
            "bao12": Record("100000:00:00"),
            "bao50": Record("100000:00:00"),
            "bao100": Record("100000:00:00")
        },
        "4x4": {
            "solves": [],
            "best": Record("100000:00:00"),
            "bao5": Record("100000:00:00"),
            "bao12": Record("100000:00:00"),
            "bao50": Record("100000:00:00"),
            "bao100": Record("100000:00:00")
        },
        "5x5": {
            "solves": [],
            "best": Record("100000:00:00"),
            "bao5": Record("100000:00:00"),
            "bao12": Record("100000:00:00"),
            "bao50": Record("100000:00:00"),
            "bao100": Record("100000:00:00")
        },
        "Megaminx": {
            "solves": [],
            "best": Record("100000:00:00"),
            "bao5": Record("100000:00:00"),
            "bao12": Record("100000:00:00"),
            "bao50": Record("100000:00:00"),
            "bao100": Record("100000:00:00")
        }
    }
    data = open(results, 'w')
    json.dump(current, data, default=lambda x: x.__dict__)


def check_if_exists(nickname):
    data = open(results, "r")
    current = json.load(data)
    if nickname not in current.keys():
        return None
    return current[nickname]["password"]


def add_chat(user_id):
    data = open(chats, "r")
    current = json.load(data)
    if user_id in current.keys():
        return
    current[user_id] = {
        "player": '',
        "event": ''
    }
    data = open(chats, "w")
    json.dump(current, data)


def set_player(user_id, player):
    data = open(chats, "r")
    current = json.load(data)
    current[str(user_id)]["player"] = player
    data = open(chats, "w")
    json.dump(current, data)


def get_player(user_id):
    data = open(chats, "r")
    current = json.load(data)
    return current[str(user_id)]["player"]


def set_event(user_id, event):
    data = open(chats, "r")
    current = json.load(data)
    current[str(user_id)]["event"] = event
    data = open(chats, "w")
    json.dump(current, data)


def get_event(user_id):
    data = open(chats, "r")
    current = json.load(data)
    return current[str(user_id)]["event"]


def get_result(user_id):
    player = get_player(user_id)
    if player == '':
        raise PlayerError
    event = get_event(user_id)
    if event == '':
        raise EventError
    data = open(results, "r")
    current = json.load(data, object_hook=decode_object)
    return current[player][event]


def incorrect_format(chat_id):
    bot.send_message(chat_id, wrong_format)
    bot.send_message(chat_id, help_solve_input(get_event(chat_id)))


def new_best(chat_id, diff):
    bot.send_message(chat_id, new_record(diff))


def get_all_results(event):
    data = open(results, "r")
    current = json.load(data, object_hook=decode_object)

    answer = {}
    for player in current.keys():
        answer[player] = (current[player][event]["best"],
                          current[player][event]["bao5"],
                          current[player][event]["bao100"])
    return answer
