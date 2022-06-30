import pygsheets
import pandas as pd
import os
import requests
import numpy as np
import json

OUTPUT_DIR = "data"

if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

client = pygsheets.authorize(service_file='creds/creds.json')

match_scouting = client.open_by_key("148_FIdHWUOmvvGvaobdIy7A1ntfWnFT3VngE6dZNFNw")  # "1_eD7UIIPd2i80rG3tlP05caS3HfCHnYJBJdqu14djzs"
match_wks = match_scouting[0]
match_df = match_wks.get_as_df()
match_skip_rows = 0

match_df.to_csv(os.path.join(OUTPUT_DIR, "match_scouting.csv"))

pit_scouting = client.open_by_key("1Uo1BhNSr_cs34ZTiruoAyUsws7KmLwcO3Bswy_istpQ") # "1Lx3fo22lIt7SGAvMddEl2_pNUh1ULW_EWRoKQ77xhCs"
pit_wks = pit_scouting[0]
pit_df = pit_wks.get_as_df()
pit_skip_rows = 0

pit_df.to_csv(os.path.join(OUTPUT_DIR, "pit_scouting.csv"))


#######Fun stuff to auto import team data and almost works######

team_num = '5006'
event_key = '2022iacf'
Blue_Key = '?X-TBA-Auth-Key=n9E8B929GHcZ2gbzqLvnhoWMT1iHsLiiQlPIpwReFEBxK9Dh4MJR3DaXqjvfS8XT'

#Team_Info = requests.get('https://www.thebluealliance.com/api/v3/team/frc'+team_num+'/events/keys'+Blue_Key+'')
Event_Team_Num = requests.get('https://www.thebluealliance.com/api/v3/event/'+event_key+'/teams/keys'+Blue_Key+'')
Event_Total = requests.get('https://www.thebluealliance.com/api/v3/event/'+event_key+'/teams'+Blue_Key+'')
open('data/Event_Team_Num.json', 'wb').write(Event_Team_Num.content)
open('data/Event_Total.json', 'wb').write(Event_Total.content)
#open('data/Team_Info.json', 'wb').write(Team_Info.content)




p = 'data/Event_Total.json'
stuff = pd.read_json('data/Event_Total.json')

#print(stuff.get(0)[1])
#print(stuff.infer_objects())
#print(stuff.size/18)
for i in range((stuff.size/18).astype(int)):
    print(stuff.iat[i,11])
    print(stuff.iat[i,16])
    print()
