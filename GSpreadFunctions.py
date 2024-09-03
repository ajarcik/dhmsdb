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


'''
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
  '''


#Once all the volunteers events are run (go in and get the rows where number of events  =1, 2, 3, etc, etc)
def formatcellsperuser(nameofspreadsheet,tabname,gc,checkedname):
  sh = gc.open(nameofspreadsheet)
  currentworksheet = sh.get_worksheet(tabname)
  list_of_lists = currentworksheet.get_all_values()
  element_to_check = checkedname
  #required_count = 4
  count = sum(sublist.count(element_to_check) for sublist in list_of_lists)
  if count == 3:
    print("GREEN")
    cell_list = worksheet.findall("Joseph Moffatt")
    worksheet.format(cell_list, {
        "backgroundColor": {
            "red": 0.0,
            "green":1.0,
            "blue": 0.0
        },
        "fontSize": 12,
        "bold": True
    })
  elif count == 2:
    print("NO GREEN")
    cell_list = worksheet.findall("Joseph Moffatt")
    worksheet.format(cell_list, {
        "backgroundColor": {
            "red": 0.0,
            "green":0.0,
            "blue": 1.0
        },
        "fontSize": 12,
        "bold": True
    })
  elif count == 1:
    print("RED")
    cell_list = worksheet.findall("Joseph Moffatt")
    worksheet.format(cell_list, {
        "backgroundColor": {
            "red": 1.0,
            "green":0.0,
            "blue": 0.0
        },
        "fontSize": 12,
        "bold": True
    })
  else:
    print("NOPE")
 
  print("All done!")

def formatallcells(nameofspreadsheet,tabname,gc):
  sh = gc.open(nameofspreadsheet)
  currentworksheet = sh.get_worksheet(tabname)
  list_of_lists = currentworksheet.get_all_values()
  #element_to_check = checkedname
  #required_count = 4
  count = sum(sublist.count(element_to_check) for sublist in list_of_lists)
  if count == 3:
    print("GREEN")
    cell_list = worksheet.findall("Joseph Moffatt")
    worksheet.format(cell_list, {
        "backgroundColor": {
            "red": 0.0,
            "green":1.0,
            "blue": 0.0
        },
        "fontSize": 12,
        "bold": True
    })
  elif count == 2:
    print("NO GREEN")
    cell_list = worksheet.findall("Joseph Moffatt")
    worksheet.format(cell_list, {
        "backgroundColor": {
            "red": 0.0,
            "green":0.0,
            "blue": 1.0
        },
        "fontSize": 12,
        "bold": True
    })
  elif count == 1:
    print("RED")
    cell_list = worksheet.findall("Joseph Moffatt")
    worksheet.format(cell_list, {
        "backgroundColor": {
            "red": 1.0,
            "green":0.0,
            "blue": 0.0
        },
        "fontSize": 12,
        "bold": True
    })
  else:
    print("Not enough information")
 
  print("All done!")