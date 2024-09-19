import gspread
import re
import time
import pandas as pd
import pandasql as ps
import numpy as np
import string
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

'''
Needs to:
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

counter = 1
def add_data_two(inputlist,gc,nameofspreadsheet,tabname):
  global counter
  counter +=1
  sh = gc.open(nameofspreadsheet)
  currentworksheet = sh.get_worksheet(tabname)

  currentworksheet.update('A1:C1',['FirstName','LastName','EmailAddress'])

  new_range = 'A'+str(counter)+':'+'C'+str(counter)
  print(counter)
  print(new_range)
  currentworksheet.update(new_range,[inputlist[0],inputlist[1],inputlist[2]])
  print("Done with adding data!!!")



def add_data(firstname, lastname, email, gc,nameofspreadsheet,tabname):
  global counter
  counter +=1
  sh = gc.open(nameofspreadsheet)
  currentworksheet = sh.get_worksheet(tabname)

  currentworksheet.update('A1:C1',['FirstName','LastName','EmailAddress'])

  new_range = 'A'+str(counter)+':'+'C'+str(counter)
  print(counter)
  print(new_range)
  currentworksheet.update(new_range,[firstname,lastname,email])
  print("Done with adding data!!!")



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
  
def get_key_by_value(dictionary, value):
  for key, val in dictionary.items():
      if val == value:
          return key

  return None  

def formatallcells(nameofspreadsheet,tabname,gc): #Concept
    alphabet_mapping = {chr(i): i - 64 for i in range(65,91)}
    sh = gc.open(nameofspreadsheet)
    currentworksheet = sh.worksheet(tabname)
    list_of_lists = currentworksheet.get_all_values()
    A = get_key_by_value(alphabet_mapping,1)
    O = get_key_by_value(alphabet_mapping,15)
    for i in list_of_lists:
        #print(i)
        count_y = i.count('y')
        #print(count_y)
        cell = currentworksheet.find(i[1])
    #print("Cell coordinates")

    #print(cell.row)
    #print(cell.col)
        #keyone_row = get_key_by_value(alphabet_mapping,cell.row)
        #keyone_column = get_key_by_value(alphabet_mapping,cell.col)
        rangeofcells = A+str(cell.row)+":"+O+str(cell.row)
        if count_y == 2:
            currentworksheet.format(rangeofcells,{
    "backgroundColor": {
        "red":1.0,
        "green":0.0,
        "blue":0.0
    }
}   
    
)
        if count_y == 3:
            currentworksheet.format(rangeofcells,{
    "backgroundColor": {
        "red":0.0,
        "green":0.0,
        "blue":1.0
    }
}   
    
)
        if count_y == 4:
            currentworksheet.format(rangeofcells,{
    "backgroundColor": {
        "red":0.0,
        "green":1.0,
        "blue":0.0
    }
}   
    
)
            
def switch(nameofspreadsheet,tabname,gc):
    nameofspreadsheet = "DHMS 2024-25"
    tabname = 'Attendance'
    sh = gc.open(nameofspreadsheet)
    currentworksheet = sh.worksheet(tabname)
    list_of_lists = currentworksheet.get_all_values()
    for i in list_of_lists:
        print(i)
    Email = input("Which email would you like to change??")
    cell = currentworksheet.find(Email)
    row = cell.row
    #print(row)
    column = cell.col
    #print(column)
    value = cell.value
    #print(value)
    #print(list_of_lists[row-1])
    currentworksheet.update_cell((row),(column),'1919')
    print("Done!!!")


def get_info(gc, dbname, tabname, name, email):
  sh = gc.open(dbname)
  worksheet = sh.worksheet(tabname)
  df = pd.DataFrame(worksheet.get_all_records())
  name = name.translate(str.maketrans('', '', string.punctuation))
  df["name"] = df["name"].apply(lambda x : x.translate(str.maketrans('', '', string.punctuation)))
  query = f"""SELECT * FROM df WHERE name='{name}' and email='{email}'"""
  return ps.sqldf(query, locals())

def get_check_in_dict(gc, dbname, tabname):
  sh = gc.open(dbname)
  worksheet = sh.worksheet(tabname)
  df = pd.DataFrame(worksheet.get_all_records())
  df["name"] = df["name"].apply(lambda x : x.translate(str.maketrans('', '', string.punctuation)))
  check_in_dict = {}
  for name in df["name"]:
    query = f"""SELECT name, checked_in FROM df WHERE name='{name}'"""
    vol = ps.sqldf(query, locals())
    check_in_dict[vol.at[0,"name"]] = vol.at[0,"checked_in"]
  return check_in_dict

def get_check_in_status(gc, dbname, tabname):
  sh = gc.open(dbname)
  teachers = sh.worksheet("Teachers")
  worksheet_vol = sh.worksheet(tabname)

  df_teach = pd.DataFrame(teachers.get_all_records())
  df_vol = pd.DataFrame(worksheet_vol.get_all_records())
  df_vol["name"] = df_vol["name"].apply(lambda x : x.translate(str.maketrans('', '', string.punctuation)))

  query = """SELECT df_teach.name, df_teach.room, count(df_vol.name) as vols_assigned, sum(checked_in) as vols_checked_in FROM df_teach INNER JOIN df_vol on df_teach.name = df_vol.teacher GROUP BY df_teach.name"""

  df = ps.sqldf(query, locals())

  volunteer_list = []
  vol_length = []

  for i in range(len(df)):
    q = f"""SELECT teacher, name FROM df_vol WHERE teacher='{df.iloc[i]["name"]}'"""

    vols = ps.sqldf(q, locals())

    vol_length.append(len(vols))

    volunteer_list.append(vols)

  for i in range(1, max(vol_length) + 1):
    a = np.empty((len(df),), dtype=object)
    a[:] = " "
    df[f"vol_{i}"] = a

  df.set_index(df['name'], inplace=True)
  df.drop(['name'], axis=1, inplace=True)

  for vol_set in volunteer_list:
    teach_name = vol_set.iloc[0]["teacher"]
    for i in range(1, len(vol_set) + 1):
      df.at[teach_name, f"vol_{i}"] = vol_set.iloc[i - 1]["name"]

  return df

def check_name_email_pair(gc, dbname, tabname, name, email):
   
  sh = gc.open(dbname)
  worksheet_vol = sh.worksheet(tabname)

  df_vol = pd.DataFrame(worksheet_vol.get_all_records())

  if len(df_vol.loc[(df_vol["name"] == name) & (df_vol["email"] == email)]) == 0:
     return True
  else:
     return False
  
def mark_checked_in(gc, dbname, tabname, name, email):
   
  sh = gc.open(dbname)
  worksheet_vol = sh.worksheet(tabname)

  email_cell = worksheet_vol.find(email)

  worksheet_vol.update_cell(email_cell.row, email_cell.col + 3, 1)

  return None

def reassign_vol(gc, dbname, tabname, name, new_teach):
   
  sh = gc.open(dbname)
  worksheet_vol = sh.worksheet(tabname)
  teachers = sh.worksheet("Teachers")

  name_cell = worksheet_vol.find(name)
  teach_cell = teachers.find(new_teach)

  worksheet_vol.update_cell(name_cell.row, name_cell.col + 2, new_teach)
  worksheet_vol.update_cell(name_cell.row, name_cell.col + 3, teachers.cell(teach_cell.row, teach_cell.col + 1).value)

  return None