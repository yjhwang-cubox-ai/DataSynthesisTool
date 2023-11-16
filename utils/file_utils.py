import os
import json
import csv

def load_config(path):
    with open(path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

def read_csv(path):
    with open(path, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        rows = [row for row in csvreader]
    return rows
