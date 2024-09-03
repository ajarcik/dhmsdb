import collections
from collections import defaultdict


#counter = 1
'''
def my_function():
    global counter
    counter +=1
    print("Function has been called this many times: ",counter)

while True:
    user_input = input("Enter values separated by commas: ")
    input_list = user_input.split(',')

    input_list = [item.strip() for item in input_list]

    print(input_list)

    my_function()
'''


list_of_lists = [
    ['apple','banana','cherry'],
    ['apple','date','cherry'],
    ['banana','cherry','apple'],
    ['date','apple','banana']

]

element_counts = {}
#required_count = 4 #can change to three or two or one 

for sublist in list_of_lists:
    for element in sublist:
        if element in element_counts:
            element_counts[element] += 1
        else:
            element_counts[element] = 1

grouped_by_count = {}
        
for element,count in element_counts.items():
    if count in grouped_by_count:
        grouped_by_count[count].append(element)
    else:
        grouped_by_count[count] = [element]

for count,elements in sorted(grouped_by_count.items()):
    print(count,elements)

print("-----------------------")
print(grouped_by_count.items())
#item_counts = dict(item_counts)
#print(item_counts)
'''
key_counts = {}

for key in item_counts:
    if key in key_counts:
        key_counts[key] += 1
    else:
        key_counts[key] = 1

count_groups = {}


for key,count in key_counts.items():
    if count in count_groups:
        count_groups[count].append(key)
    else:
        count_groups[count] = [key]

print(count_groups.items())


    
if count == required_count:
    print("YEP")
    cell_list = worksheet.findall("Joseph Moffatt")
    worksheet.format(cell_list, {
        "backgroundColor": {
            "red": 0.0,
            "green":0.0,
            "blue": 0.0
        },
        "fontSize": 12,
        "bold": True
    })
else:
    print("NOPE")
'''