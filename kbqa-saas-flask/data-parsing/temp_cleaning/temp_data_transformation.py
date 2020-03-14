import json

with open('result_spy.json', 'r') as spy_file:
    spy = json.load(spy_file)

with open('fields_renamed.json', 'r') as fields_file:
    field_mapping = json.load(fields_file)

field_renamed_spy = {}
for ticker, info in spy.items():
    ticker_info = {}

    for field, value in info.items():

        predicate = '/' + field.lower().replace(" ", "_")
        print(predicate)

        if predicate in field_mapping:

            new_predicate = field_mapping[predicate]
            new_field = new_predicate[1:].replace("_", " ")
            ticker_info[new_field] = value


    field_renamed_spy[ticker] = ticker_info


with open('new_result_spy.json', 'w') as fields_file:

    json.dump(field_renamed_spy, fields_file)
