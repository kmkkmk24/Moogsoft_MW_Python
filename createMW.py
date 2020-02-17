#############################################################################
#  Purpose : To create Maintenance Window in Moogsoft with API  -Kaushik KM #	
#############################################################################
import requests
import json
import datetime as dt
from tkinter.filedialog import askopenfilename
import csv
import shutil
import os
import time
###############################
#  	Global Variables		  #
###############################
dir 		= os.path.abspath(r'E:\MonitoringScripts\MOOG_MW_PY')
bin 		= os.path.join(dir,'bin')
archive		= os.path.join(dir,'archive')
Dtformat = '%m/%d/%Y %H:%M'
MOOG_UAT_URL = 'https://loblaw-uat.moogsoft.io/graze/v1/createMaintenanceWindow'
MOOG_PROD_URL = 'https://loblaw.moogsoft.com/graze/v1/createMaintenanceWindow'
datestring  = time.strftime('%d%m%Y%H%M%S')
###############################
#  	Sub Functions			  #
###############################
def CalcTimeDelta():
	StartTime = input("Start data and time ? Format mm/dd/yyyy HH:MM: ")
	EndTime = input("End data and time ? format mm/dd/yyyy HH:MM: ")
	Startdatetime_object = dt.datetime.strptime(StartTime, Dtformat)
	Enddatetime_object = dt.datetime.strptime(EndTime, Dtformat)
	duration = Enddatetime_object.timestamp() - Startdatetime_object.timestamp()
	return(duration,Startdatetime_object.timestamp())
def Get_PayLoad_Details():
	MW_INC_Name = input("Please enter REF INC: ")
	MW_Manager = input("Please enter Manager Name or Enter \"ALL\" for Everything: ")
	var = input("Please press \"y\" to choose source file: ")
	if (var == 'y'):
		SrcFileName = askopenfilename()
	else:
		print("Please enter y to choose file, Exit!")
		exit(0)
	TimeDelta,starttime = (CalcTimeDelta())
	with open(SrcFileName) as csvfile:
		Servers=list(csv.reader(csvfile, delimiter=','))
	source_list = str(Servers[0])[1:-1]
	if (MW_Manager == 'ALL'):
		mypayload = {"name":f"{MW_INC_Name}", "description":f"{MW_INC_Name}", "filter": f"Source IN ({source_list})", "start_date_time": int(starttime), "duration": int(TimeDelta), "forward_alerts": 'false', "recurring_period": 1, "recurring_period_units": 4}
	else:
		mypayload = {"name":f"{MW_INC_Name}", "description":f"{MW_INC_Name}", "filter": f"Manager MATCHES {MW_Manager} AND Source IN ({source_list})", "start_date_time": int(starttime), "duration": int(TimeDelta), "forward_alerts": 'false', "recurring_period": 1, "recurring_period_units": 4}
	mypayload_dumps = json.dumps(mypayload)
	return(mypayload_dumps)
###############################
#  	Main Function			  #
###############################
if __name__ == "__main__":
	global SrcFileName
	global MW_INC_Name
	Payload = Get_PayLoad_Details()
	resp = requests.post(MOOG_UAT_URL, data=Payload,headers={'Content-type': 'application/json'},auth=(r'graze',r'graze'))
	if(resp.status_code == 200):
		print("Maintainance Window created successfully!!")
	else:
		print("Error in Maintainance Window creation, Try again!! :",resp.reason)