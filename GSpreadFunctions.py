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



def add_data(firstname, lastname, email,gc,nameofspreadsheet,tabname):
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
