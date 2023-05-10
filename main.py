import telebot
from src.Work_with_data import *
from src.Answers import *


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.chat.id
    add_chat(user_id)
    bot.send_message(user_id, text=hello_string)
    nickname = bot.send_message(user_id, text=log_in_string)
    bot.register_next_step_handler(nickname, registration)


@bot.message_handler(commands=['global'])
def show_global(message):
    user_id = message.chat.id
    event = get_event(user_id)

    if event == '':
        select_event(message)
        return

    results = get_all_results(event)
    answer = ''
    for player, result in results.items():
        if str(result[0]) == '':
            continue
        answer += '\n' + player + '\n' + f"Best single is {str(result[0])}\n"
        if str(result[1]) == '':
            continue
        answer += f"Best average of 5 is {str(result[1])}\n"
        if str(result[2]) == '':
            continue
        answer += f"Best average of 100 is {str(result[2])}\n"

    if len(answer) == 0:
        bot.send_message(user_id, no_results)
    else:
        bot.send_message(user_id, answer)


@bot.message_handler(commands=['reg'])
def reg_user(message):
    log_in = bot.send_message(message.chat.id, log_in_string)
    bot.register_next_step_handler(log_in, registration)


@bot.message_handler(commands=['help'])
def help_user(message):
    bot.send_message(message.chat.id, help_string)


@bot.message_handler(commands=['event'])
def select_event(message):
    msg = bot.send_message(message.chat.id, select_event_string, reply_markup=event_choice_markup)
    bot.register_next_step_handler(msg, choose_discipline)


@bot.message_handler(commands=["last"])
def show_last(message):
    txt = message.text
    try:
        number = int(txt.split()[1])
        if number <= 0:
            raise ValueError
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, number_after_last)
        return

    try:
        results_dict = get_result(message.chat.id)
    except PlayerError:
        msg = bot.send_message(message.chat.id, log_in_string)
        bot.register_next_step_handler(msg, registration)
        return
    except EventError:
        msg = bot.send_message(message.chat.id, select_event_string, reply_markup=event_choice_markup)
        bot.register_next_step_handler(msg, choose_discipline)
        return

    answer = ''
    if number > len(results_dict["solves"]):
        answer += not_enough_solves
    else:
        for elem in results_dict["solves"][-number:]:
            answer += str(elem) + ' ' + elem.comment + '\n'
    bot.send_message(message.chat.id, answer)


@bot.message_handler(commands=['stats'])
def show_statistics(message):
    try:
        results_dict = get_result(message.chat.id)
    except PlayerError:
        msg = bot.send_message(message.chat.id, log_in_string)
        bot.register_next_step_handler(msg, registration)
        return
    except EventError:
        msg = bot.send_message(message.chat.id, select_event_string, reply_markup=event_choice_markup)
        bot.register_next_step_handler(msg, choose_discipline)
        return
    bot.send_message(message.chat.id, get_stats(results_dict))


@bot.message_handler(func=lambda x: True)
def get_solve(message):
    try:
        add_solve(message)
    except PlayerError:
        msg = bot.send_message(message.chat.id, log_in_string)
        bot.register_next_step_handler(msg, registration)
        return
    except EventError:
        msg = bot.send_message(message.chat.id, select_event_string, reply_markup=event_choice_markup)
        bot.register_next_step_handler(msg, choose_discipline)
        return


def registration(message):
    user_id = message.chat.id
    set_player(user_id, '')
    player = message.text.strip()

    if check_commands(message):
        return
    if player[0] == '/':
        bot.send_message(user_id, slash_message)
        reg_user(message)
        return

    passwrd = check_if_exists(player)

    def get_password(message_1):
        inpt = message_1.text.strip()
        if check_commands(message):
            return
        if passwrd == inpt:
            event_msg = bot.send_message(user_id, text=success_reg_string, reply_markup=event_choice_markup)
            set_player(user_id, player)
            bot.register_next_step_handler(event_msg, choose_discipline)
        else:
            bot.send_message(user_id, text=wrong_password)
            new_nickname = bot.send_message(user_id, text=log_in_string)
            bot.register_next_step_handler(new_nickname, registration)

    if passwrd is None:
        passwrd_1_msg = bot.send_message(user_id, text=name_is_free)
        bot.register_next_step_handler(passwrd_1_msg, lambda m: get_new_password(m, player))
    else:
        passwrd_1_msg = bot.send_message(user_id, text=name_is_locked)
        bot.register_next_step_handler(passwrd_1_msg, get_password)
        

def get_new_password(message, player):
    password_1 = message.text.strip()
    user_id = message.chat.id

    def repeat_new_password(message_1):
        password_2 = message_1.text.strip()
        if check_commands(message):
            return
        if password_1 != password_2:
            bot.send_message(user_id, text=diff_passwords_string)
            new_nickname = bot.send_message(user_id, text=log_in_string)
            bot.register_next_step_handler(new_nickname, registration)
        else:
            add_new_user(player, password_2)
            change_event = bot.send_message(user_id, text=success_reg_string, reply_markup=event_choice_markup)
            bot.register_next_step_handler(change_event, choose_discipline)

    if check_commands(message):
        return
    else:
        passwrd_2_msg = bot.send_message(user_id, text=again_password_string)
        bot.register_next_step_handler(passwrd_2_msg, repeat_new_password)
        

def choose_discipline(message):
    txt = message.text.strip()
    user_id = message.chat.id
    set_event(user_id, '')

    if txt == "/reg":
        new_nickname = bot.send_message(user_id, text=log_in_string)
        bot.register_next_step_handler(new_nickname, registration)
        return
    if txt == "/start":
        bot.send_message(user_id, to_start)
        start_message(message)
        return
    if txt == "/stats":
        show_statistics(message)
        return
    if txt == "/global":
        show_global(message)
        return
    if txt[:5] == "/last":
        show_last(message)
        return
    if txt == "/help":
        msg = bot.send_message(user_id, help_string, reply_markup=event_choice_markup)
        bot.register_next_step_handler(msg, choose_discipline)
    if txt not in ["2x2", "3x3 two-handed", "3x3 one-handed", "4x4", "5x5", "Megaminx"]:
        answer = bot.send_message(user_id, text=wrong_event, reply_markup=event_choice_markup)
        bot.register_next_step_handler(answer, choose_discipline)
        return
    if txt == "2x2":
        set_event(user_id, "2x2")
    elif txt == "3x3 two-handed":
        set_event(user_id, "3x3 two-handed")
    elif txt == "3x3 one-handed":
        set_event(user_id, "3x3 one-handed")
    elif txt == "4x4":
        set_event(user_id, "4x4")
    elif txt == "5x5":
        set_event(user_id, "5x5")
    else:
        set_event(user_id, "Megaminx")

    bot.send_message(user_id, text=help_solve_input(get_event(user_id)))


def check_commands(message):
    txt = message.text.strip()
    if txt == "/start":
        bot.send_message(message.chat.id, to_start)
        start_message(message)
        return True
    if txt == "/reg":
        reg_user(message)
        return True
    if txt == "/global":
        show_global(message)
        return True
    if txt == "/stats":
        show_statistics(message)
        return True
    if txt[:5] == "/last":
        show_last(message)
        return True
    if txt == "/help":
        help_user(message)
        reg_user(message)
        return True
    return False


bot.infinity_polling()
