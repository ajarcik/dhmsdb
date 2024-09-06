import collections
from collections import defaultdict
import gspread
gc = gspread.service_account(filename= 'service_account.json')
nameofspreadsheet = "DHMS 2024-25"
tabname = 'Attendance'
sh = gc.open(nameofspreadsheet)
currentworksheet = sh.worksheet("2/23/2024 - Volunteers")
list_of_lists = currentworksheet.get_all_values()
