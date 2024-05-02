from PyQt6.QtWidgets import QApplication, QFileDialog, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout, QStatusBar, QMainWindow
from PyQt6.QtCore import Qt, pyqtSignal
from pathlib import Path
from fonction.csv_data import run_data, sauvegarde
from fonction.excel_data import run_xlsx

class MainWindow(QWidget):
    selectedDirectoryChanged = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    # crée la fenêtre de l'app et définit une taille fix, définit aussi certaines variables
        self.setWindowTitle('MàJ DATA')
        self.setFixedSize(500, 150)
        self.selected_directory = ""
        self.selected_directory_save = ""

    # set the grid layout
        layout = QGridLayout()
        self.setLayout(layout)

    # directory
        dir_btn = QPushButton('Parcourir...')
        dir_btn.clicked.connect(self.open_dir_dialog)
        self.dir_name_edit = QLineEdit(placeholderText="Veuillez choisir le répertoire")
        layout.addWidget(QLabel('Répertoire :'), 1, 0)
        layout.addWidget(self.dir_name_edit, 1, 1)
        layout.addWidget(dir_btn, 1, 2)

    # save as
        save_btn = QPushButton('Parcourir...')
        save_btn.clicked.connect(self.open_save)
        self.save_name_edit = QLineEdit(placeholderText="Choisissez le lieu de sauvegarde.")
        layout.addWidget(QLabel('Sauvegarder : '), 2, 0)
        layout.addWidget(self.save_name_edit, 2, 1)
        layout.addWidget(save_btn, 2, 2)

    # name of file
        self.name_file = QLineEdit(
            self,
            # place un texte sur lequel on peut écrire, souvent utilisé pour indiquer ce que l'on attends dans une zone de texte
            placeholderText='Entrer un nom pour sauvegarder.',
            # ajoute une petite croix permettant de supprimer tout le contenu de la zone de texte
            clearButtonEnabled=True
        )
        layout.addWidget(QLabel('Nom du fichier : '), 3, 0)
        layout.addWidget(self.name_file, 3,1 )

    # crée un bouton pour quitter l'app
        leave = QPushButton('Quitter')
        leave.clicked.connect(self.quit)

    # crée un bouton permettant de mettre à jour les données
        maj = QPushButton('Mettre à jour')
        maj.clicked.connect(self.run)

    # add buttons to the layout
        layout.addWidget(maj, 4, 0, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(leave, 4, 2, alignment=Qt.AlignmentFlag.AlignRight)

    # showing a message when the data are ok 
        self.end_dl = QLabel('Ne pas fermer', self)
        layout.addWidget(self.end_dl, 5, 0)
    
    # create an empty label to show all end_dl

    # show the window
        self.show()

    # permet le parcours les dossiers de la machine et la sélection de l'un d'entre eux
    #@param permet d'appeler une autre variable de la maniere suivant ex : self.variable
    def open_save(self):
        save_name = QFileDialog.getExistingDirectory(self, "Select a Directory")
        if save_name:
            path = Path(save_name)
            self.save_name_edit.setText(str(path))
            self.selected_directory_save = str(path)
            self.selectedDirectoryChanged.emit(self.selected_directory_save)

    # permet le parcours les dossiers de la machine et la sélection de l'un d'entre eux
    #@param permet d'appeler une autre variable de la maniere suivant ex : self.variable
    def open_dir_dialog(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Select a Directory")
        if dir_name:
            path = Path(dir_name)
            self.dir_name_edit.setText(str(path))
            self.selected_directory = str(path)
            self.selectedDirectoryChanged.emit(self.selected_directory)

    # permet de fermer l'app a l'appuie d'un bouton
    #@param permet d'appeler une autre variable de la maniere suivant ex : self.variable
    def quit(self):
        self.destroy()
    
    # permet de lancer la fonction run_data qui se trouve dans le fichier library.py
    #@param permet d'appeler une autre variable de la maniere suivant ex : self.variable
    def run(self):
        #@param le chemin sélectionner par l'app
        df, df_cycle = run_data(self.selected_directory)
        selected_refs = run_xlsx(self.selected_directory)
        # Demander à l'utilisateur de choisir un emplacement de sauvegarde
        nom_fichier = self.name_file.text()
        chemin_sauvegarde = self.save_name_edit.text()
        print("Lieu de Sauvegarde : " + chemin_sauvegarde)
        print("Nom du fichier : " + nom_fichier)
        # S'assurer que l'utilisateur a sélectionné un emplacement
        if chemin_sauvegarde and nom_fichier:
            sauvegarde(df, df_cycle, selected_refs, chemin_sauvegarde, nom_fichier)
            self.end_dl.setText("Données à jour.")
        else:
            print("Sauvegarde annulée.")