import json
import random
import uuid

my_dict = {}
json_file = open('data.json', 'w')
count = 0

with open('data.txt') as f:
    for line in f:
        line = line.rstrip('\n').rstrip('\r')
        if not line:
            continue
        if '${playerOne}' not in line:
            category = line.rstrip(':')
            my_dict[category] = {}
            curr_category = category
            count = 0
            continue
        document_id = random.getrandbits(128)
        my_dict[curr_category][document_id] = {'question': line, 'question_id': count}
        count += 1

json.dump(my_dict, json_file, indent=4)