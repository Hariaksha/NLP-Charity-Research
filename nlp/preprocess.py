import spacy 
from spacy.tokens import doc
import openpyxl

nlp = spacy.load('en_core_web_lg')

workbook = openpyxl.load_workbook(f'data/preliminary_march_data/data.xlsx')
ws = workbook.active

workbook2 = openpyxl.load_workbook('nlp/preprocessed-missions.xlsx')
ws2 = workbook2.active

count = 0
for i in range(2, ws.max_row + 1):
    if count == 100:
        break
    mission = ws[f'P{i}']
    ein = ws[f'A{i}']
    name = ws[f'B{i}']
    ntee = ws['I{i}']
    asset = ws['K{i}']
    revenue = ws['O{i}']
    doc = nlp(mission)
    ws2.append([ein, name, mission, doc, revenue, asset, ntee])

workbook2.save()