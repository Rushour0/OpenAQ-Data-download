import requests
import json
import pandas as pd

# Functions

def makeCSV( jsonfile, city ):
	
	# Create main csv if not present
	try:
		file = open(f"{city}_data.csv","r")
		file.close()

	except:

		# Make a dictionary for the dataframe
		temp_dict = {}

		for i in jsonfile["results"][0]:
			if i == "date":
				temp_dict["utc"] = []
				temp_dict["local"] = []
				continue

			elif i == "coordinates":
				for j in jsonfile["results"][0][i]:
					temp_dict[j] = []
				continue

			else:
				temp_dict[i] = []

		df = pd.DataFrame(temp_dict)

		df.to_csv( f"{city}_data.csv",index=False,header=True )
		del df


	# Making temporary dictionary for making the dataframe
	temp_df_dict = {}

	for i in jsonfile["results"][0]:
		if i == "date":
			temp_df_dict["utc"] = []
			temp_df_dict["local"] = []
			continue

		elif i == "coordinates":
			for j in ["latitude","longitude"]:
				temp_df_dict[j] = []
			continue

		else:
			temp_df_dict[i] = []

	# Filling the dictionary
	for location in jsonfile["results"]:
		for attr in location:
			if attr == "date":
				temp_df_dict["utc"].append(location[attr]["utc"])
				temp_df_dict["local"].append(location[attr]["local"])
				continue

			elif attr == "coordinates":
				for j in ["latitude","longitude"]:
					if location[attr] == None:
						temp_df_dict[j].append(location[attr])
						continue
					temp_df_dict[j].append(location[attr][j])
				continue

			else:
				temp_df_dict[attr].append(location[attr])

	# Create temp dataframe
	temp_df = pd.DataFrame( temp_df_dict )

	# CLI confirmation
	print("DataFrame created : ", True if not temp_df.empty else False)

	# Saving the main file
	temp_df.to_csv(f"{city}_temp_data.csv",index = False, header = False)

	# CLI confirmation
	print("Saved CSV")

	# Appending to the data
	with open(f"{city}_data.csv","a") as main_file:
		with open(f"{city}_temp_data.csv","r") as temp_file:
			main_file.write(temp_file.read())
	
	del temp_df,temp_df_dict


def makeRequest( date_from, date_to, filecounter, limit = 100000, city = "Delhi" ):

	# API link for response in json format
	response = requests.get(f"https://api.openaq.org/v2/measurements?limit={limit}&page=1&date_from={date_from}&date_to={date_to}&city={city}")

	# Get the response json file
	jsonfile = response.json()

	# Print json
	print("Received json response : ", True if jsonfile else False)

	# Get the date for next date_to
	new_date_to = jsonfile["results"][-1]["date"]["utc"].split("T")[0]

	if jsonfile["results"] == []:
		return None

	# make and append to the csv file
	makeCSV( jsonfile, city )

	# Make counter dictionary
	counter_json = {"filecounter":filecounter ,"date_to":new_date_to,"city":city }

	# Save counter
	with open("global_variables.json", "w") as file:
		file.write(json.dumps( counter_json , indent = 4 ))

	print( "New date_to :",new_date_to )
	return new_date_to

