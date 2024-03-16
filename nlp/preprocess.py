import spacy 
from spacy.tokens import doc
import openpyxl

nlp = spacy.load('en_core_web_md')
print("Loaded model")

workbook = openpyxl.load_workbook('data/preliminary_march_data/data.xlsx')
ws = workbook.active
print("opened workbook 1")

workbook2 = openpyxl.load_workbook('nlp/preprocessed-missions.xlsx')
ws2 = workbook2.active
print("opened workbook 2")

count = 0
for i in range(2, ws.max_row + 1):
    print(i)
    if count == 3000:
        break
    mission = str(ws[f'P{i}'].value)
    ein = ws[f'A{i}'].value
    name = ws[f'B{i}'].value
    ntee = ws[f'I{i}'].value
    asset = ws[f'K{i}'].value
    revenue = ws[f'O{i}'].value
    doc = nlp(mission)
    lemmatized_text = " ".join([token.lemma_ for token in doc])
    ws2.append([ein, name, "", lemmatized_text, revenue, asset, ntee])
    count += 1

workbook2.save('nlp/preprocessed-missions.xlsx')