import gspread
import re
import time
import collection
#from collection import Counter
from GSpreadFunctions import CreateDatabaseSpreadsheet,movedata,formatcells
'''
#Have to go in  about once every week to change the token credentials
gc = gspread.service_account(filename= 'service_account.json')
nameofspreadsheet = 'DruidHillsVolunteerEvents8/30/2024'
sh = gc.create(nameofspreadsheet)
sh.share('jamoffatt.411@gmail.com',perm_type='user',role='writer') #replace with your G-mail account 

#alphabet_mapping = {chr(i): i - 64 for i in range(65,91)}
print("Done!")
'''

gc = gspread.service_account(filename= 'service_account.json')
nameofspreadsheet = 'DruidHillsVolunteerEvents-9/3/2024'
Dates = ['9/6/2024','9/13/2024','9/20/24','9/27/2024']
GoogleEmail = 'jamoffatt.411@gmail.com'
CreateDatabaseSpreadsheet(nameofspreadsheet,Dates,gc,GoogleEmail)

# After the volunteer event is over, move the data to the corresponding sheet



