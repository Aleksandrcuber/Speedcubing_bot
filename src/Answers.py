from telebot import types
from src.Recording_struct import *


hello_string = """\
Hello! This is a bot for keeping your speedcubing results!
"""

to_start = "Back to start"

log_in_string = """\
You need to log in. Please type in your nickname (if you don't have it yet, just create one)!
"""

no_results = "No results yet!"

select_event_string = "You need to select event! Choose from this options below:"

not_enough_solves = "You don't have so many solves yet!"

again_password_string = """ Enter it again """

diff_passwords_string = """ Something is wrong! Passwords should be the same! Try again."""

success_reg_string = """ You successfully logged in! Choose event to practice! """

name_is_free = """\
There's no account with such a name yet! You can create one by setting\
a password for it. Or type /reg to start over again.
"""

name_is_locked = """\
There's already a player with this nickname. If it's you, type in\
 a password for this account. Or type /reg to start over again.
"""

slash_message = " Name can't start with slash! "

wrong_format = " Can't understand you! Please try again! "

wrong_event = "You entered something wrong! Choose from the list below"

wrong_password = "Password is wrong. Try again."

number_after_last = "After '/last' you should put a positive number of solves you want to see"

solve_added = "Result's saved!"


def help_solve_input(event):
    help_solve_input = f"""\
You chosed '{event}' event! Now you can start \
your practice session! Just type in the time you got on the solve. 
 Optionally you can add comments for the solve. Format you messages like this: 
 'mm:ss:mm your_comment'. This app will save your result.
 Type in '/stats' to see your statistics on current discipline. 
 Type in '/last _number_' to see last _number_ your solves.
 Type in '/event' to change current event.
 Type in '/reg' to change account.
    """
    return help_solve_input


def new_record(diff):
    new_record_string = f" Congratulations! New best! You've just beaten your previous record by {str(diff)}"
    return new_record_string


def get_stats(results):
    count = len(results["solves"])
    if count == 0:
        return "You haven't done any solves yet"
    answer = f"You have done {count} solves!\n"
    best_single = results["best"]
    answer += f"Your best single is {str(best_single)}\n"
    for n in [5, 12, 50, 100]:
        if count >= n:
            answer += f"Current ao{n} is {str(count_avg(results['solves'], n))}. \
Your best ao{n} is {str(results[f'bao{n}'])}\n"
    return answer


help_string = """\
Use '/start' to start the bot
Use '/reg' to log in. If you don't have account yet, you can create it by setting username \
and password via '/reg' command. If you do have account, just type in username and password \
for that
Use '/stats' to see your statistics on current discipline
Use '/last _number_' to see last _number_ your solves
Use '/event' to change current event
Use '/global' to see other people's results on selected discipline
To enter a solve result, just type in your time (use mm:ss:mm format) and optionally comment on the solve
"""

event_choice_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
item_btn_1 = types.KeyboardButton('2x2')
item_btn_2 = types.KeyboardButton('3x3 two-handed')
item_btn_3 = types.KeyboardButton("3x3 one-handed")
event_choice_markup.row(item_btn_1, item_btn_2, item_btn_3)
item_btn_4 = types.KeyboardButton('4x4')
item_btn_5 = types.KeyboardButton('5x5')
item_btn_6 = types.KeyboardButton('Megaminx')
event_choice_markup.row(item_btn_4, item_btn_5, item_btn_6)