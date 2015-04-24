import json

records = []
with open("test.json", "r") as log_file:
    for raw_log_record in log_file:
        records.append(json.loads(raw_log_record))

for record in records:
    if int(record["loop_num"]) > 2:
        print("{0}, {1}".format(record["message"], record["loop_num"]))
