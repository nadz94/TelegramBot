import os
import telebot
from replit import db
import re
from functions import start_of_week, barchart
  

#Initiate bot
API_KEY = os.environ['API_KEY']
bot = telebot.TeleBot(API_KEY)


###############
#Start command#
###############
@bot.message_handler(commands=["start"])
def send_start_message(msg):
  """
  markup = types.ReplyKeyboardMarkup(row_width=2)
  btn1 = types.KeyboardButton("/help")
  btn2 = types.KeyboardButton("/mytotal")
  btn3 = types.KeyboardButton("/")
  btn4 = types.KeyboardButton("/close")
  markup.add(btn1, btn2, btn3, btn4)
  """
  bot.send_message(
    chat_id=msg.chat.id,
    text=
    "Welcome skinny boy. what would you like to do? (see /help for instructions)")
    #,reply_markup=markup)


##############
#Help command#
##############
@bot.message_handler(commands=["help"])
def send_help_message(msg):
  bot.reply_to(
    msg, """The following commands are available:
  
  /start -> to initiate the bot
  /addcount X -> to add your weekly count of gym attendance where 'X' is a number between 0-7
  /updatecount X -> update an existing count
  /mytotal -> your total number of gym days since Jan 2023
  /myweeklycount -> your total number of days for the current week
  /weeklyview -> a graph of your weekly attendance
  """)


#######################
#Add your weekly count#
#######################
@bot.message_handler(commands=["addcount"])
def add_count(msg):
  # Print for debugging purpose
  print('name: ', msg.from_user.first_name, '\n w\c: ',
        start_of_week(msg.date), '\n count: ', msg.text[-1], '\n chat type: ',
        msg.chat.type)

  # Unique key for each week for each person
  msg_key = "(" + msg.from_user.first_name + "," + start_of_week(
    msg.date) + ")"

  # Extract count from message
  count = msg.text[-1]

  # Check if value is double digits
  if re.match(r'\d', msg.text[-2]):
    bot.reply_to(msg,"single digit brev")
    
  # Checking if count already exists in database
  elif msg_key in db.keys():
    bot.reply_to(msg, "You have already submitted a count for this week")

  else:
    """if /addcount function is called without specifying a number, don't add to database"""
    # Check if last character is a number, if so push to DB
    if re.match(r'\d', count):
      # Check if count is between 0 and 7
      if int(count) not in range(0, 8):
        bot.reply_to(msg, "There are only 7 days in a week you donut")
      else:
        db[msg_key] = count
        bot.reply_to(
          msg, """The following count has been added:
        name: %s, 
        w\c: %s, 
        count: %s
        """ % (msg.from_user.first_name, start_of_week(msg.date), count))
    else:
      bot.reply_to(msg, "You did not specify a number")


##########################
#Update your weekly count#
##########################
@bot.message_handler(commands=["updatecount"])
def update_count(msg):
  # Checking for double digits
  if re.match(r'\d', msg.text[-2]):
    bot.reply_to(msg, "there are only 7 days in a week you donut")

  else:
    if re.match(r'\d', msg.text[-1]) and int(msg.text[-1]) in range(0, 8):
      # Finding database entries for specific user
      msg_key = "(" + msg.from_user.first_name + "," + start_of_week(
        msg.date) + ")"
      # drop the entry
      try:
        del db[msg_key]
      except KeyError:
        pass
      # add new entry
      add_count(msg)
  
    else:
      bot.reply_to(msg, "You did not specify a number")
  

#######################################
#Return total count for full database#
#######################################
@bot.message_handler(commands=["mytotal"])
def return_year_total(msg):
  # Finding database entries for specific user
  users_counts = [
    int(db[k]) for k in db if msg.from_user.first_name in k
  ]
  bot.reply_to(msg, sum(users_counts))


###########################
#Return count for the week#
###########################
@bot.message_handler(commands=["myweeklycount"])
def return_weekly_count(msg):
  # Finding database entry for specific user
  user_key = "(" + msg.from_user.first_name + "," + start_of_week(
    msg.date) + ")"
  try:
    bot.reply_to(msg, db[user_key])

  # Otherwise return nothing
  except:
    bot.reply_to(msg, "You have not submitted a count for this week")


#########################################
#Return a chart showing weekly breakdown#
#########################################
@bot.message_handler(commands=["weeklyview"])
def return_specified_week_count(msg):

  # Finding database entries for specified date
  name = msg.from_user.first_name

  # Generate graph
  barchart(name,db)

  # Send image of graph
  bot.send_photo( msg.chat.id, open("chart.png", "rb") )

bot.polling()
















'''
@bot.message_handler(func=lambda msg: msg.from_user.username == "ElRataAlada"))
def send_help_message(msg):
  print(msg.from_user.id, msg.from_user.username)
  bot.reply_to(msg,"What colour is your deadlift?")
'''