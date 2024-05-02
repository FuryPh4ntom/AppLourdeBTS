from multiprocessing import Pool, cpu_count
from pathlib import Path
import os
import pandas as pd
import pickle


# récupère les fichiers csv et leur chemin ex: path/fichier.csv
#@param path = le dossier ou se trouve les fichiers CSV
def csvfilenames(path):
# création de listes
    filenames = []
# parcours le système de la machine
    for root, dirs, files in os.walk(path):
# parcourt les fichiers trouvés dans le chemin
        for file in files:
# en fonction de l'extension du fichier, ici csv, ajoute les fichiers à la liste
            if file.endswith(".CSV"):
                filenames.append(os.path.join(root, file))
# suppression des variables après dernière utilisation
    del path
    return filenames

# optimise les données de type object que l'on peut voir avec la commande df.info(memory_usage='deep'), ici df représente un dataframe
#@param data_obj = un dataframe construit
def opti_object(data_obj):
    df_obj = data_obj.select_dtypes(include=['object']).copy()
    converted_obj = pd.DataFrame()
    for col in df_obj.columns:
        if len(df_obj[col].unique()) / len(df_obj[col]) < 0.5:
            converted_obj.loc[:, col] = df_obj[col].astype('category')
        else:
            converted_obj.loc[:, col] = df_obj[col]
# suppression des variables après dernière utilisation
    del df_obj
    del data_obj
    return converted_obj

# optimise les données de type flottant que l'on peut voir avec la commande df.info(memory_usage='deep'), ici df représente un dataframe
#@param data_float = un dataframe contenant des valeurs numériques
def opti_float(data_float):
# sélectionne les types float et les copies
    df_float = data_float.select_dtypes(include=['float']).copy()
# crée un dataframe vide
    converted_float = pd.DataFrame()
# parcourt les colonnes de la copie du df
    for col in df_float.columns:
# en fonction de la taille des colonnes (uniques ou non)
        if len(df_float[col].unique()) / len(df_float[col]) < 0.5:
# change le type de la colonne, ajoute la copie au dataframe vide
            converted_float.loc[:, col] = df_float[col].astype('f')
        else:
# si ce n'est pas un float, laisse la colonne telle quelle 
            converted_float.loc[:, col] = df_float[col]
    return converted_float

# affiche sous forme de dataframe le chemin et nom du fichier
#@param route = csvfilenames(path) = chemin/fichier.csv
def df_path(route):
# crée une variable en tant que dataframe avec en entrée le paramètre et instancie le nom de la première colonne
    dataframe_path = pd.DataFrame(route, columns=["Path"])
# sans changer le chemin/nomfichier, crée une colonne pour le nom de fichier
    dataframe_path["Filename"] = [Path(x).name for x in dataframe_path.Path]
# suppression des variables après dernière utilisation
    del route
    return dataframe_path

# crée une liste avec les noms de fichiers spécifiques
#@param dataframe_path = df_path(route) = chemin/fichier.csv ||| fichier.csv
def liste_values(dataframe_path):
# création de liste
    df_list = []
    df_list_cycle = []
# parcours les noms du dataframe dataframe 
    for k in dataframe_path["Path"]:
# lit le fichier csv
        file = pd.read_csv(k, sep=';', skiprows=1, usecols=[0, 1])
        #file = opti_object(file)
# renomme les colonnes du fichier
        file.columns = ["Date", "Value"]
# en fonction des premiers caractères et renomme la colonne avant de l'ajouter dans les listes
        if "_I" in k:
            file.columns = ["Date", "I"]
            df_list.append(file)
        elif "_F" in k:
            file.columns = ["Date", "F"]
            df_list.append(file)
        else:
# quand k n'est pas une intensité ou une fréquence, sort le nom du fichier du chemin 
# k = chemin/fichier.extension
            k = Path(k).stem
# k = fichier
            file.columns = ["Date", "Mouvement"]
# crée une 3e colonne dans le tableau et ajoute le tout dans une liste
            file["type"] = k
            df_list_cycle.append(file)
# suppression des variables après dernière utilisation
    del dataframe_path
    return df_list, df_list_cycle

# mets tous les fichiers csv dans un seul et même fichier, puis réécrit pour I et F en format numérique, sinon pour tout les fichiers, passe la date en format date jj-mm-aaaa
#@param df_list = une liste contenant une date et des valeurs numérique, df_list_cycle = une liste contenant une date et des valeurs de mouvements
def formate_df(df_list, df_list_cycle):
# mets toutes les données des listes dans une seule variable pour faciliter le traitement et le passe en dataframe
    df = pd.concat(df_list).map(lambda x: str(str(x).replace(',', '.')))
    del df_list
    df = opti_object(df)
# convertit les valeurs en numérique / date
    df["I"] = pd.to_numeric(df["I"], errors='coerce')
    df["F"] = pd.to_numeric(df["F"], errors='coerce')
    df["Date"] = pd.to_datetime(df["Date"], format='%d/%m/%Y %H:%M:%S.%f', errors='coerce')
    df[["I", "F"]] = opti_float(df)
    df.columns = ["Date", "I", "F"]
# convertit les valeurs de date
    df_cycle = pd.concat(df_list_cycle).map(lambda x: str(str(x).replace(',', '.')))
    df_cycle["Date"] = pd.to_datetime(df_cycle["Date"], format='%d/%m/%Y %H:%M:%S.%f', errors='coerce')
    return df, df_cycle

# sauvegarde les dataframe dans un fichier pickle
#@param df = un dataframe contenant une col date, et 2 col numérique, df_cycle = 
def sauvegarde(df, df_cycle, selected_refs, chemin_sauvegarde, nom_fichier):
# équivaut à chemin/fichier.pkl
    path = chemin_sauvegarde + "\\" + nom_fichier + ".pkl"
    try:
# crée et ecrit dans le fichier pkl
        with open(path, 'wb') as fichier_pickle:
            pickle.dump((df, df_cycle, selected_refs), fichier_pickle)
        print("Sauvegarde réussie.")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")

# lance toute les fonctions précédentes
#@param le chemin sélcetionné par l'utilisateur via l'interface graphique
def run_data(path_data):
    filenames = csvfilenames(path_data)
    dataframe_path = df_path(filenames)
    del filenames
    df_list, df_list_cycle = liste_values(dataframe_path)
    df, df_cycle = formate_df(df_list, df_list_cycle)
    return df, df_cycle

#### mettre les 3 valeurs en fichiers pkl pour l'application




# possibilité d'afficher le graphe de toute les données
"""
#crée un graphe, trace des lignes et l'affiche viz une interface web 127.0.0.1:xxxxx
#@param reprends les données df df_cac et df_cda de formate_df()
def graphe(df, df_CAC, df_CDA):
    fig = make_subplots(specs=[[{"secondary_y": True}]]) # permet de crée un 2e axe Y
    # creation des tracés et suppression des variables après dernière utilisation
    fig.add_trace(go.Scatter(x=df["Date"], y=df["I"], name='I', line=dict(color='blue')), secondary_y=False)
    fig.add_trace(go.Scatter(x=df["Date"], y=df["F"], name='F', line=dict(color='red')), secondary_y=True)
    del df
    fig.add_trace(go.Scatter(x=df_CAC["Date"], y=df_CAC["Montée"], mode='lines', name='Montée'))
    del df_CAC
    fig.add_trace(go.Scatter(x=df_CDA["Date"], y=df_CDA["Descente"], mode='lines', name='Descente'))
    del df_CDA
    # mets des noms sur les axes
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Intensité',
        yaxis2_title='Fréquence'
    )
    # mets en place des boutons pour se déplacer par périodes
    fig.update_xaxes(rangeslider_visible=True, rangeselector=dict(buttons=list([
        dict(count=7, label="1w", step="day", stepmode="backward"),
        dict(count=1, label="1m", step="month", stepmode="backward"),
        dict(count=6, label="6m", step="month", stepmode="backward"),
        dict(count=1, label="1y", step="year", stepmode="backward"),
        dict(step="all")
    ])))
    # affichage de la figure 
    figure = fig.show()
    print(figure)"""