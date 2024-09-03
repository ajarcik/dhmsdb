import gspread
import re
import time
#from collection import Counter

#gc = gspread.oauth(credentials_filename='token.json')
#alphabet_mapping = {chr(i): i - 64 for i in range(65,91)}

'''
The purpose of this CreateDatabaseSpreadsheet function is create a Google spreadsheet using gspread library. 
@nameofspreadsheet - desired name of spreadsheet
@ArrayOfDates - an array of dates (as strings) For Example: Dates = ['9/6/2024','9/13/2024','9/20/24','9/27/2024']
@gc - auth component
@GoogleEmail - a Gmail account you have access to and the account the file will be shared with 
'''

def CreateDatabaseSpreadsheet(nameofspreadsheet,ArrayOfDates,gc,GoogleEmail):
  sh = gc.create(nameofspreadsheet)
  time.sleep(2)
  sh = gc.open(nameofspreadsheet)
  time.sleep(2)
  for i in ArrayOfDates:
    worksheet = sh.add_worksheet(title=i, rows=100, cols=20)
  sh.share(GoogleEmail,perm_type='user',role='writer') 
  print("Done!!!!")



def movedata(LengthOfHolderList,gc,nameofspreadsheet,tabname,targetname):
  sh = gc.open(nameofspreadsheet)
  worksheet = sh.worksheet(tabname)
  list_of_lists = worksheet.get_all_values()
  HolderList = []
  for i in list_of_lists:
    if i[3] == "9/6/2024":
        HolderList.append(i)

  worksheet = sh.worksheet(targetname)
  CellRange = 'A1:'+'D'+str(LengthOfHolderList)
  worksheet.update(HolderList,'A1:D2')
  print("Done!!")



#Once all the volunteers events are run (go in and get the rows where number of events  =1, 2, 3, etc, etc)
def formatcells(nameofspreadsheet,tabname,gc):
  sh = gc.open(nameofspreadsheet)
  worksheet = sh.worksheet(tabname)
  list_of_lists = worksheet.get_all_values()
  print(list_of_lists)
  #counts = Counter(list_of_lists)





  '''
  Where some code to edit the edit the cells will go
  '''



  print("All done!")

