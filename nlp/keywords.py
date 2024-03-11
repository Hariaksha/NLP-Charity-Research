import openpyxl
import csv
import spacy
from collections import defaultdict

def main():
    counts = defaultdict(int)
    state = "WY"
    workbook = openpyxl.load_workbook(f'data/finished_with_revenue/{state}_data.xlsx')
    ws = workbook.active
    nlp = spacy.load('en_core_web_md')
    for row in ws.iter_rows():
        mission = row[15].value
        doc = nlp(mission)
        for token in doc:
            counts[token] += 1
    filename = open('data/keywords.csv') 
    file = csv.DictReader(filename)
    for word, count in counts.items():
        file.append([word, count])

if __name__=="__main__":
    main()
