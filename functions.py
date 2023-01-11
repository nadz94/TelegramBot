import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Date function to find start of the week
def start_of_week(input):
  day = datetime.utcfromtimestamp(int(input)).strftime("%d-%m-%Y")
  dt = datetime.strptime(day, '%d-%m-%Y')
  start = dt - timedelta(days=dt.weekday())
  return (start.strftime("%d-%m-%Y"))

# Function to return graph of weekly attendance for a specific user
def barchart(msg,db):
  # Plotting the graph

  all_entries = list(db.find({"User_id":msg.from_user.id}))
  users_name = msg.from_user.first_name
  
  counts = [int(x['Count']) for x in all_entries]
  dates = [x['WeekStarting'] for x in all_entries]
  
  
  plt.bar(dates, counts, align='center')
  plt.title( users_name + "\'s total")
  plt.savefig('chart.png', dpi = 200)
  plt.close()