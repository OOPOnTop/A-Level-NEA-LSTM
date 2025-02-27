import csv
import pandas as pd

raw_data = []

with open('/Users/charlie/PycharmProjects/A-Level-NEA-LSTM/AI_models/Data_Assets/train.csv', 'r', encoding='utf8') as f:
    spamreader = csv.reader(f, delimiter=',')
    line = 0
    if line == 0:
        line += 1
    for row in spamreader:
        raw_data.append(row)

f.close()
raw_data.pop(0)

with open('/Users/charlie/PycharmProjects/A-Level-NEA-LSTM/AI_models/Data_Assets/train_clean.csv', 'w', encoding='utf8', newline='') as f:
    spamwriter = csv.writer(f, delimiter=',')



    for row in raw_data:
        for i in row:
            if type(i) == float:
                i = round(i, 4)
            else:
                pass
        row[9] = str(float(row[9])/100000)



    """spamwriter.writerow(['Artist Name', 'Track Name', 'Danceability', 'Energy',
    'Loudness', 'Mode', 'Speechiness', 'Acousticness', 'Liveness',
    'Valence', 'Tempo', 'Duration', 'Time Signature'])"""
    for row in raw_data:
        for i, j in enumerate(["◊", "ì", "ï", "ú"]):
            if j in row[1] or None in row or "" in row or " " in row:
                pass
            else:
                if i % 4 == 0:
                    spamwriter.writerow(row)


f = pd.read_csv("/Users/charlie/PycharmProjects/A-Level-NEA-LSTM/AI_models/Data_Assets/train_clean.csv", header=None)
f.columns =['Artist Name', 'Track Name', 'Danceability', 'Energy',
    'Loudness', 'Mode', 'Speechiness', 'Acousticness', 'Liveness',
    'Valence', 'Tempo', 'Duration', 'Time Signature']
f.to_csv("/Users/charlie/PycharmProjects/A-Level-NEA-LSTM/AI_models/Data_Assets/train_clean.csv", index=False)
