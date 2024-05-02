import os
import pandas as pd
from pathlib import Path

def excelfilenames(path):
    excelfile = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".xlsx"):
                excelfile.append(os.path.join(root, file))
    return excelfile

def df_path(route):
    dataframe_path = pd.DataFrame(route, columns=["Path"])
    dataframe_path["Filename"] = [Path(x).name for x in dataframe_path.Path]
    return dataframe_path

def liste_values(dataframe_path):
    selected_refs = []
    for k in dataframe_path["Path"]:
        try:
            file = pd.read_excel(k, skiprows=3, engine='openpyxl')
            file.columns = ['Vide', 'Nom Machine', 'type evt', 'num pcmf', 'ref evt', 'descri evt', 'Vide', 'debut evt', 'vide']
            if 'ref evt' in file.columns and 'debut evt' in file.columns:
                for index, row in file.iterrows():
                    ref_evt = row['ref evt']
                    debut_evt = row['debut evt']
                    if 'EVT' in ref_evt and 'AL' in ref_evt:
                        selected_refs.append((ref_evt, debut_evt))
        except Exception as e:
            print(f"Error reading {k}: {e}")

    selected_refs = pd.DataFrame(selected_refs, columns=['ref', 'date'])
    selected_refs['date'] = pd.to_datetime(selected_refs["date"], format='%d/%m/%Y %H:%M:%S.%f', errors='coerce')
    return selected_refs

def run_xlsx(path):
    excelfile = excelfilenames(path)
    dataframe_path = df_path(excelfile)
    selected_refs = liste_values(dataframe_path)
    return selected_refs
