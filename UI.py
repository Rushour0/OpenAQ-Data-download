from PySimpleGUI import *
from datetime import datetime
import os

def make_date(year,month,day):
	return datetime(year=int(year),month=int(month),day=int(day)).strftime("%Y-%m-%d")

def date_check(year,month,day):
	try:
		datetime(year=int(year),month=int(month),day=int(day))
	except:
		return False
	return True

theme('DarkAmber')
def createLayout():

	layout =[
				[Text("Dataset download from OpenAQ",key = 'title',font = ('Cambria',20))],
				[Text()],
				[Text()],
				[Text("Enter city name",size = (20,1),key = 'city_',font = ('Leelawadee',12)),Input(size = (20,1),key = 'city' )],
				[Text("Date from : (YYYY MM DD)",key = 'from',font = ('Cambria',12)),Input(size = (5,1),key = 'fY' ),Input(size = (4,1),key = 'fM' ),Input(size = (4,1),key = 'fD' )],
				[Text("Date to : (YYYY MM DD)",key = 'to',font = ('Cambria',12)),Input(size = (5,1),key = 'tY' ),Input(size = (4,1),key = 'tM' ),Input(size = (4,1),key = 'tD' )],
				[Text("",size = (50	,1),key = "out")],
				[Button('  Download  ')],
				[Text()],
				[Text(" "*27),Button(button_text = 'QUIT',key = 'quit')]
			]
	return layout

def loop():    
	layout = createLayout()

	#Create window with given layout
	window = Window('Download from OpenAQ', layout,margins = (100,100))

	flag = 0
	while True:

		# Get the events and values from inputs
		event, values = window.Read()

		# Checking if the window is closed
		if event == WINDOW_CLOSED:
			break

		# Start downloader
		if flag:
			subprocess.Popen(["downloader.exe"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			# os.spawnl(os.P_DETACH,"downloader.exe")
			flag = 0
			window["out"].update("Done!")

		# Download action
		if event == "  Download  ":
			
			try:
				date_check(values['fY'],values['fM'],values['fD'])
			except:
				window["out"].update("Wrong date format in the from date")
				continue

			try:
				date_check(values['tY'],values['tM'],values['tD'])
			except:
				window["out"].update("Wrong date format in the to date")
				continue
			
			date_from = make_date(values['fY'],values['fM'],values['fD'])
			date_to = make_date(values['tY'],values['tM'],values['tD'])

			temp_dict = {"city":values["city"],"date_from":date_from,"date_to":date_to}

			with open("global_variables.json","w") as file:
				file.write(json.dumps(temp_dict, indent = 4))

			window["out"].update("Download started")
			flag = 1

		if event == 'quit':
			res = popup_yes_no("Do you want to quit?")
			if res.lower() == "yes":
				break
			else:
				pass

	window.close()
loop()
        





