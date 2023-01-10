import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Date function to find start of the week
def start_of_week(input):
  day = datetime.utcfromtimestamp(int(input)).strftime("%d-%m-%Y")
  dt = datetime.strptime(day, '%d-%m-%Y')
  start = dt - timedelta(days=dt.weekday())
  return (start.strftime("%d-%m-%Y"))

# Function to return graph of weekly attendance for a specific user
def barchart(name,db):
  # Plotting the graph
  counts = [ int(db[k]) for k in db if name in k ]
  dates = [ k[-11:-1] for k in db if name in k ]
  plt.bar(dates, counts, align='center')
  plt.title(name + "\'s total")
  plt.savefig('chart.png', dpi = 200)
  plt.close()