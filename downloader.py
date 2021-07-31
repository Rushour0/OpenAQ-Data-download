from functions import *
from datetime import datetime
	
# CLI confirmation
print("Imported")


# Program start

# Loading dates

# Downloader
def download():

	# Checking for a past date_to in the store
	try:
		data = json.load(open("global_variables.json","r"))
		date_from = data["date_from"]
	except:
		date_from = datetime(2015,1,1).strftime("%Y-%m-%d")

	# Checking for a past date_to in the store
	try:
		date_to = data["date_to"]
	except:
		date_to = datetime(2021,7,30).strftime("%Y-%m-%d")

	print(f"\n{date_from} : {date_to}")

	# Load the file counter (Unnecessary)
	try:
		counter = data["filecounter"]
	except:
		counter = 0

	# Load the city
	try:
		data = json.load(open("global_variables.json","r"))
		city = data["city"]
	except:
		city = "Delhi"
		print("No City selected -> Delhi selected by default")

	# Starting the data downloading loop
	while ( datetime.fromisoformat(date_from) <= datetime.fromisoformat(date_to) ):
		prev_date_to = date_to

		# Get the next date
		date_to = makeRequest( date_from = date_from, date_to = date_to, filecounter = counter, city = city )

		# CLI confirmation
		print(f"Stored Data from {date_to} to {prev_date_to}\n")
		counter+=1

	print("Check if done, else execute program again")

if __name__ == "__main__":
	download()