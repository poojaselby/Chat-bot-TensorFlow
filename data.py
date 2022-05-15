# Importing Libraries
import pandas as pd
import numpy as np
import json
import mysql.connector
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='chatbot_db_test')

mycursor = cnx.cursor()
mycursor.execute("SELECT * FROM chatbot_tb")

chatbot_tb = mycursor.fetchall()

chatbot_df = pd.DataFrame(chatbot_tb)
chatbot_df.columns = ["tag", "patterns", "responses"]

chatbot_df = chatbot_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

chatbot_df['tag'] = chatbot_df['tag'].str.replace(r'[^\w\s]+', '')
chatbot_df['patterns'] = chatbot_df['patterns'].str.replace(r'[^\w\s]+', '')
chatbot_df['responses'] = chatbot_df['responses'].str.replace(r'[^\w\s]+', '')

df = chatbot_df

g = df.groupby("tag")
g.groups.keys()

json_str = ""

innerdict = {}
outerdict = {}

for i in g.groups.keys():
    gk = g.get_group(i)
    gk_dict = gk.to_dict(orient='list')
    res_dict = {k: [elem for elem in v if elem is not ""] for k, v in gk_dict.items()}
    res_dict['tag'] = set(res_dict['tag'])

    res_dict_tpr = str(res_dict)
    del res_dict['tag']
    res_dict_pr = str(res_dict)

    res_dict_str_json = res_dict_tpr[:8] + "'" + str(i) + "' , " + res_dict_pr[1:]
    res_dict_json = eval(res_dict_str_json)

    res_dict_json = json.dumps(res_dict_json)
    res_json = json.loads(res_dict_json)

    json_str += res_dict_json

json_dict = "{" + "\"intents\":[ " + json_str + "]}"
json_dict = json_dict.replace("]}{", "]}, {")

json_string = eval(json_dict)
json_string = json.dumps(json_string)
jsonFile = open("chatbot_json.json", "w")
jsonFile.write(json_string)
jsonFile.close()