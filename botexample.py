import telebot
import ast
import time
import config
import schedule
from telebot import types
from telegram.ext import Updater
from telegram.ext import CommandHandler
import datetime
#update = Updater(config.TOKEN)
#user = update.message.from_user
#print(user)
bot=telebot.TeleBot(config.TOKEN1)
stringList = {"yes": "no"}
crossIcon = u"\u274C"
checkmark=u"\u2705"
heart=u"\u2764"
name=''
flag=False

global id,data
user_name=''

current_time = datetime.datetime.now().day

def func():
    print("doing func")
    with open('attinit.txt','r') as f:
        new_file_content = ""
        for line in f:
            stripped_line = line.strip()             
            new_file_content += stripped_line +"\n"
        f.close()
    writing_file = open("attendance.txt", "w")
    writing_file.write(new_file_content)
    writing_file.close()

#schedule.every().day.at("00:05").do(func)

def makeKeyboard():
    markup = types.InlineKeyboardMarkup()

    for key, value in stringList.items():
        markup.add(types.InlineKeyboardButton(text=checkmark,
                                              callback_data="['value', '" + value + "', '" + key + "']"),
        types.InlineKeyboardButton(text=crossIcon,
                                   callback_data="['key', '" + key + "']"),
        types.InlineKeyboardButton(text="List",
                                   callback_data="list")
                                   )

    return markup



@bot.message_handler(commands=['start'])
def handle_command_adminwindow(message):
    global id,data,current_time
    id=message.chat.id
    #data=message.data
    #schedule.every().day.at("00:00").do(func)
    curr_time= datetime.datetime.now().day
    if curr_time!=current_time:
        func()
        current_time=curr_time
    global name,user_name
    name = message.from_user.first_name
    user_name=message.from_user.username
    print(name)
    bot.send_message(chat_id=message.chat.id,
                     text="Esti prezent?",
                     reply_markup=makeKeyboard(),
                     parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    global name,id,user_name
    name= '@'+name
    print(name)
    if (call.data.startswith("['value'")):
        flag=True
        print(f"call.data : {call.data} , type : {type(call.data)}")
        print(f"ast.literal_eval(call.data) : {ast.literal_eval(call.data)} , type : {type(ast.literal_eval(call.data))}")
        valueFromCallBack = ast.literal_eval(call.data)[1]
        keyFromCallBack = ast.literal_eval(call.data)[2]
        bot.answer_callback_query(callback_query_id=call.id,
                              show_alert=True,
                              text="Thank you "+heart)
        with open('attendance.txt',"r") as f:
            new_file_content = ""
            for line in f:
                stripped_line = line.strip()
                if name not in stripped_line:
                    new_line=stripped_line
                elif name in stripped_line or user_name in stripped_line:
                    new_line = stripped_line.replace("-", "+")
                
                    
                new_file_content += new_line +"\n"
            f.close()
        writing_file = open("attendance.txt", "w")
        writing_file.write(new_file_content)
        writing_file.close()
    name=name[1:]

    if (call.data.startswith("['key'")):
        flag=False
        keyFromCallBack = ast.literal_eval(call.data)[1]
        valueFromCallBack = ast.literal_eval(call.data)[1]
        bot.answer_callback_query(callback_query_id=call.id,
                              text="Hope you are OK, thank you "+heart,
                              show_alert=True)
        with open('attendance.txt',"r") as f:
            new_file_content = ""
            for line in f:
                stripped_line = line.strip()
                if name not in stripped_line:
                    new_line=stripped_line
                elif name in stripped_line:
                    new_line = stripped_line.replace("-", "--")
                
                    
                new_file_content += new_line +"\n"
            f.close()
        writing_file = open("attendance.txt", "w")
        writing_file.write(new_file_content)
        writing_file.close()

    if call.data.startswith("list"):
        
        with open('attendance.txt',"r") as f:
            new_file_content = ""
            for line in f:
                stripped_line = line.strip()
                new_file_content += stripped_line +"\n"
            f.close()
        bot.send_message(text=new_file_content,chat_id=id)
        
        #bot.answer_callback_query(callback_query_id=call.id,
         #                     show_alert=True,
          #                    text=new_file_content)
    
while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=0)
    except:
        time.sleep(10)