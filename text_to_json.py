import firebase_admin, json, random, uuid
from firebase_admin import firestore, credentials
from argparse import ArgumentParser

args = ArgumentParser()
args.add_argument("--infile", help="The text file to be read in", required=True)
args.add_argument("--outfile", help="The json file to be written to", required=True)
args = args.parse_args()

my_dict = {}
json_file = open(args.outfile, 'w')
count = 0

cred = credentials.Certificate("service-key.json")
firebase_admin.initialize_app(cred)
client = firestore.client()
categories = [doc.to_dict()['category'] for doc in client.collection("categories").get()]
next_id = {}

for category in categories:
    count = 1
    for doc in client.collection(category).get():
        count += 1
    next_id[category] = count

with open(args.infile) as f:
    line_count = 0
    for line in f:
        line_count += 1
        line = line.rstrip('\n').rstrip('\r')

        # Move on if the line is empty
        if not line or not line.strip():
            continue

        # if this is not in the line and it's not empty, it must be a category
        if '${playerOne}' not in line:
            category = line.rstrip(':')
            if category not in next_id:
                print("%s is not a valid category.  Please create a collection in firestore." % category)
                exit(0)
            my_dict[category] = {}
            curr_category = category
            count = next_id[category]
            continue
        document_id = random.getrandbits(128)
        my_dict[curr_category][document_id] = {'question': line, 'question_id': count}
        count += 1

json.dump(my_dict, json_file, indent=4)