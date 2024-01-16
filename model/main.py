import json
from model.model import Model

FILENAME = r"C:/Users/delan/Documents/APAQ_files/Airports.json"
with open(FILENAME, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

FILENAME = r"C:\Users\delan\Desktop\APAQ\data\airports_augmented.json"
with open(FILENAME, "r", encoding="utf-8") as f:
    aq_data = json.load(f)

m = Model()

target, feature = m.preprocessing(raw_data, aq_data)

print(target)
print(feature)