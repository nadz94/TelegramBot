import os
import telebot
import re
from functions import start_of_week, barchart
from pymongo import MongoClient

#Initiate bot
API_KEY = os.environ['API_KEY']
bot = telebot.TeleBot(API_KEY)

#Connect to MongoDB server
cluster = "mongodb+srv://nadz94:Gangster123@projects.mb1ub5c.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(cluster)
db = client.Strand.GymTracker

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

  week_start = start_of_week(msg.date)
  
  # Print for debugging purpose
  print('name: ', msg.from_user.first_name, '\n w\c: ',
        week_start, '\n count: ', msg.text[-1], '\n chat type: ',
        msg.chat.type)

  # Extract count from message
  try:
    count = msg.text.split(" ")[1]
    
    if not count:
      bot.reply_to(msg,"You did not specify a number")
  
    # Check if value is within range 0-7
    elif re.match(r"^[0-9]+$",count):
      if int(count) not in range(0,8):
        bot.reply_to(msg, "There are only 7 days in a week you donut")
        
      # Checking if count already exists in database
      elif db.find_one({"WeekStarting":week_start,"User_id":msg.from_user.id}):
        bot.reply_to(msg, "You have already submitted a count for this week")
        

      else:
        db.insert_one({"WeekStarting":week_start,
                       "DateSubmitted":msg.date,
                       "User_id":msg.from_user.id,
                       "Username":msg.from_user.username,
                       "Name":msg.from_user.first_name,
                       "Count":count})
        
        bot.reply_to(
          msg, """The following count has been added:
        name: %s, 
        w\c: %s, 
        count: %s
        """ % (msg.from_user.first_name, week_start, count))

    else:
      bot.reply_to(msg,"You did not specify a number")
    
  except IndexError:
      bot.reply_to(msg, "You did not specify a number")


##########################
#Update your weekly count#
##########################
@bot.message_handler(commands=["updatecount"])
def update_count(msg):

  try:
    count = msg.text.split(" ")[1]
  
    # Checking for count
    if not count:
      bot.reply_to(msg, "You did not specify a number")

    elif re.match(r"^[0-9]+$",count):
      if int(count) not in range(0,8):
        bot.reply_to(msg, "There are only 7 days in a week you donut")

      else:
        db.update_one({"WeekStarting":start_of_week(msg.date),"User_id":msg.from_user.id},
                      {"$set": {"Count":count}})
        
        bot.reply_to(msg, f"Your count has been updated to: {count}")
        
  except IndexError:
    bot.reply_to(msg, "You did not specify a number")
  

#######################################
#Return total count for full database#
#######################################
@bot.message_handler(commands=["mytotal"])
def return_year_total(msg):
  # Finding database entries for specific user
  all_entries = list(db.find({"User_id":msg.from_user.id}))

  total_count = sum([int(x['Count']) for x in all_entries])

  bot.reply_to(msg, f"Your overall total attendace is: {total_count}")

  
###########################
#Return count for the week#
###########################
@bot.message_handler(commands=["myweeklycount"])
def return_weekly_count(msg):
  # Finding database entry for specific user
  week_start = start_of_week(msg.date)
  
  try:
    count = db.find_one({"WeekStarting":week_start,"User_id":msg.from_user.id})["Count"]
    bot.reply_to(msg, f"Your total for this week is: {count}")

  # Otherwise return nothing
  except TypeError:
    bot.reply_to(msg, "You have not submitted a count for this week")


#########################################
#Return a chart showing weekly breakdown#
#########################################
@bot.message_handler(commands=["weeklyview"])
def return_specified_week_count(msg):

  # Generate graph
  barchart(msg,db)

  # Send image of graph
  bot.send_photo( msg.chat.id, open("chart.png", "rb") )

bot.polling()
















'''
@bot.message_handler(func=lambda msg: msg.from_user.username == "ElRataAlada"))
def send_help_message(msg):
  print(msg.from_user.id, msg.from_user.username)
  bot.reply_to(msg,"What colour is your deadlift?")
'''