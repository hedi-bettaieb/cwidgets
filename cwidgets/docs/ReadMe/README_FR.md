# Guide de l'utilisateur - Bibliothèque CWidgets V0.1.3.post1

## Introduction

CWidgets est une bibliothèque Python spécialisée qui donne aux développeurs aveugles
un contrôle total sur les interfaces PyQt6 et PySide6.

L'ère des limitations avec QTextEdit est révolue — vous pouvez désormais concevoir
des interfaces contenant des zones d'édition multi-lignes avec une liberté et une
compatibilité totales avec NVDA.

Tout ce que vous avez à faire est de remplacer la première lettre (C au lieu de Q) :
- CTextEdit au lieu de QTextEdit
- CButton au lieu de QPushButton
- Où C signifie Custom

La bibliothèque supporte les deux environnements Qt :

# PySide6
from cwidgets.pyside6 import CButton, CLabel, CLineEdit

# PyQt6
from cwidgets.pyqt6 import CButton, CLabel, CLineEdit

CWidgets : Codez avec confiance, concevez sans limites.


## Composants disponibles

7 composants personnalisés entièrement compatibles NVDA :

1. CTextEdit
2. CButton
3. CLabel
4. CLineEdit
5. CComboBox
6. CListWidget
7. CMessageBox


## Installation

pip install cwidgets


## Accéder à l'aide

import cwidgets

# Liste de tous les composants disponibles
cwidgets.widgets()

# Liste de toutes les sections disponibles
cwidgets.sections()

# Ouvrir le guide complet dans le navigateur
cwidgets.show_help()
cwidgets.show_help(lang="fr")
cwidgets.show_help(lang="ar")

# Ouvrir un composant spécifique directement
cwidgets.show_help(lang="fr", goto="CButton")
cwidgets.show_help(lang="fr", goto="CTextEdit")

# Ouvrir une section spécifique directement
cwidgets.show_help(lang="fr", goto="introduction")
cwidgets.show_help(lang="fr", goto="installation")

# API de CTextEdit:  
cwidgets.ctextedit.show()          # noms seuls
cwidgets.ctextedit.show_details()  # noms + descriptions


## Problèmes courants résolus

**CTextEdit** — Zone d'édition multi-lignes : résout l'incompatibilité de QTextEdit avec NVDA.

**CComboBox & CListWidget** — Séparation navigation/activation : évite les activations
involontaires lors de la navigation avec les flèches. Accessibilité NVDA maintenue
même en mode désactivé.

**CButton** — Activation via Entrée, Retour, Espace et clic. Compatibilité NVDA
même lorsque désactivé.

**CLabel** — Compatibilité améliorée pour les titres et étiquettes.

**CLineEdit** — Récupération du texte via Entrée sans code supplémentaire.

**CMessageBox** — Boîtes de dialogue à fermeture automatique avec délai configurable.

À l'exception de CTextEdit, tous les composants héritent de Qt et conservent
toutes leurs propriétés et fonctions d'origine.


## Détails des composants


## CTextEdit

### Définition
CTextEdit est une zone d'édition multi-lignes entièrement accessible avec NVDA,
basée sur le moteur natif Win32 RichEdit.

### Pourquoi — Le problème fondamental
- QTextEdit natif de Qt est incompatible avec NVDA.
- Les développeurs aveugles ne peuvent pas lire ou écrire dans cet élément.
- Jusqu'à l'apparition de cette bibliothèque, aucune solution connue n'existait.

### Solution — RichEdit Win32 intégré dans Qt
La solution intègre directement un contrôle RichEdit Win32 dans la fenêtre Qt.
RichEdit Win32 est nativement compatible avec NVDA.

Structure interne :
- CTextEdit — Interface Qt publique
- EditorStyle — Styles, police, couleur, alignement
- RichEdit Win32 — Moteur natif compatible NVDA

### Fonctionnalités
- Accessibilité NVDA complète : lecture, écriture, navigation, sélection.
- API étendue : 25 méthodes publiques disponibles.
- Texte formaté : police, taille, gras, italique, couleur, alignement.
- Signaux : textChanged, selectionChanged, cursorPositionChanged.
- Gestion asynchrone : styles et texte mis en file d'attente avant initialisation.
- Focus intelligent : restauré automatiquement après Alt+Tab.

### Import

# PySide6
from cwidgets.pyside6 import CTextEdit
# PyQt6
from cwidgets.pyqt6 import CTextEdit

### Création

self.editor = CTextEdit(self, accessible_name="Nom de la zone")
layout.addWidget(self.editor)

### API disponible

# Afficher toutes les méthodes depuis le terminal
import cwidgets
cwidgets.ctextedit.show()          # noms seuls
cwidgets.ctextedit.show_details()  # noms + descriptions

# Depuis le code
CTextEdit.api()

### Contenu

# Définir le contenu
self.editor.setText("Bonjour !")

# Récupérer le contenu
text = self.editor.toPlainText()
text = self.editor.text()          # alias de toPlainText()

# Ajouter du texte à la fin
self.editor.append("Nouvelle ligne.")

# Insérer à la position du curseur
self.editor.insertPlainText("Texte inséré\n")

# Insérer du HTML à la position du curseur
# Les balises sont supprimées, <br> et <p> deviennent des sauts de ligne
self.editor.insertHtml("<p>Bonjour <b>monde</b></p>")  # insère : "Bonjour monde"
self.editor.insertHtml("<p>Ligne 1</p><br/>Ligne 2")   # insère : "Ligne 1\nLigne 2"

# Vider le contenu
self.editor.clear()

### Sélection

# Sélectionner tout
self.editor.selectAll()

# Récupérer le texte sélectionné (retourne "" si aucune sélection)
text = self.editor.selectedText()

# Exemple combiné — récupérer tout le texte
self.editor.selectAll()
text = self.editor.selectedText()

### Propriétés

# Nombre de lignes
count = self.editor.lineCount()

# Lecture seule
self.editor.setReadOnly(True)    # activer
self.editor.setReadOnly(False)   # désactiver
state = self.editor.isReadOnly() # vérifier

### Mise en forme

# Police — QFont ou (nom, taille, gras, italique)
self.editor.setFont("Arial", 12, True, False)

# Couleur du texte — nom ou (R, G, B)
self.editor.setTextColor("red")
self.editor.setTextColor((255, 0, 0))

# Couleur de fond
self.editor.setBackgroundColor("yellow")

# Alignement
self.editor.setAlignment("left")
self.editor.setAlignment("center")
self.editor.setAlignment("right")

### Couleurs disponibles

# Noms supportés
"black", "white", "red", "green", "blue", "yellow",
"cyan", "magenta", "gray", "darkgray", "lightgray",
"orange", "purple", "violet", "pink", "brown",
"navy", "teal", "lime", "olive", "maroon",
"coral", "salmon", "gold", "silver"

# Ou RGB
(255, 0, 0)    # rouge
(0, 128, 255)  # bleu clair

### Presse-papiers

# Les raccourcis Ctrl+C/X/V/Z/Y fonctionnent nativement via le clavier.
# Ces méthodes permettent un usage programmatique (ex: via un bouton).

self.editor.copy()   # copier la sélection
self.editor.cut()    # couper la sélection
self.editor.paste()  # coller
self.editor.undo()   # annuler
self.editor.redo()   # rétablir

### Signaux

# Réagir aux modifications en temps réel
self.editor.textChanged.connect(self.on_text_changed)
self.editor.cursorPositionChanged.connect(self.on_cursor_changed)
self.editor.selectionChanged.connect(self.on_selection_changed)

def on_text_changed(self):
    print(self.editor.toPlainText())

def on_cursor_changed(self):
    print("Curseur déplacé")

def on_selection_changed(self):
    print(self.editor.selectedText())

### Comportement dans les layouts

CTextEdit a une taille minimale de 50x50 pixels pour garantir sa visibilité.

**Cas 1 — QVBoxLayout (éditeur seul sur sa ligne)**
layout.addWidget(self.editor)

**Cas 2 — QHBoxLayout partagé avec QListWidget ou QComboBox**
Sans `stretch=1`, les autres widgets prennent tout l'espace.
layout = QHBoxLayout()
layout.addWidget(self.list_widget, 1)
layout.addWidget(self.editor, 1)

**Cas 3 — Dimensions fixes**
self.editor = CTextEdit(self, width=400, height=200)

**Cas 4 — Masquer / Afficher**
self.editor.hide()  # cache sans détruire le contenu
self.editor.show()  # réaffiche avec le contenu intact

### Titre visuel optionnel

accessible_name est lu par NVDA mais n'est pas visuellement visible.
Pour ajouter un titre visuel, utiliser CLabel avant l'éditeur dans le layout :

self.editor = CTextEdit(self)
self.lbl    = CLabel("Zone d'édition :", self, self.editor)
layout.addWidget(self.lbl)
layout.addWidget(self.editor)


### CLabel

#### Définition
CLabel est une étiquette compatible NVDA qui remplace `QLabel`.

#### Pourquoi ?

QLabel est invisible pour NVDA sauf s'il est lié à un buddy, et seulement lorsque ce buddy a le focus.

#### Solution

**Mode simple (individuel)** :  
Compatible NVDA, reconnu directement via la navigation par tabulation (Focus fort).

**Mode buddy** :  
Lié à un autre composant, invisible à la tabulation (pas de focus) pour éviter d'encombrer la lecture.  
Son texte nettoyé est lu automatiquement quand le composant lié prend le focus.

#### Fonctionnalités

- **Nettoyage des raccourcis** : `&Nom` devient `"Nom"` pour NVDA. Le raccourci visuel reste préservé pour le système.
- **prefix** : Texte supplémentaire pour exprimer un statut (ex : "erreur", "statut").
- **Synchronisation automatique** via `setText()` et `setPrefix()`.

#### Utilisation

# PySide6
from cwidgets.pyside6 import CLabel, CLineEdit
# PyQt6
from cwidgets.pyqt6 import CLabel, CLineEdit

# Mode simple (individuel)
self.lbl = CLabel("Fichier enregistré", self, prefix="statut")
# NVDA annonce : "statut fichier enregistré"
layout.addWidget(self.lbl)

# Mode buddy — ajouter le label AU DESSUS du buddy dans le layout
self.edit = CLineEdit(self)
self.lbl  = CLabel("&Nom :", self, self.edit)
layout.addWidget(self.lbl)   # label en premier → apparaît au-dessus
layout.addWidget(self.edit)

# Mise à jour dynamique
self.lbl.setText("Traitement en cours")
self.lbl.setPrefix("erreur")


## CButton

### Définition
CButton est un bouton accessible qui remplace QPushButton.

### Pourquoi ?
- QPushButton n'accepte que la barre d'espace — Entrée et Retour sont ignorés.
- setEnabled(False) rend le bouton invisible pour NVDA.

### Solution
- Activation via Entrée, Retour, Espace et clic souris.
- Mode désactivé : non cliquable mais visible pour NVDA ("indisponible").

### Fonctionnalités
- Activation étendue : Espace, Entrée, Retour, clic souris.
- Désactivation accessible : NVDA annonce "indisponible".
- API identique à QPushButton.

### Utilisation

# PySide6
from cwidgets.pyside6 import CButton
# PyQt6
from cwidgets.pyqt6 import CButton

self.btn = CButton("Enregistrer", self)
self.btn.clicked.connect(self.on_click)

# Désactiver / réactiver
self.btn.setEnabled(False)
self.btn.setEnabled(True)

# Vérifier l'état
if self.btn.isEnabled():
    ...


## CLineEdit

### Définition
CLineEdit est un champ de saisie compatible qui remplace QLineEdit.

### Pourquoi ?
QLineEdit nécessite du code supplémentaire pour récupérer le texte à la validation.
CLineEdit automatise cela via le signal `validated`.

### Fonctionnalités
- Signal `validated` : émet le texte à chaque Entrée/Retour.
- `placeholderText` en paramètre, annoncé par NVDA quand le champ est vide.
- Titre via CLabel avec buddy.

### Utilisation

# PySide6
from cwidgets.pyside6 import CLineEdit, CLabel
# PyQt6
from cwidgets.pyqt6 import CLineEdit, CLabel

self.edit = CLineEdit(self)
self.lbl  = CLabel("Nom :", self, self.edit)
layout.addWidget(self.lbl)
layout.addWidget(self.edit)

# Avec texte initial
self.edit = CLineEdit(self, "Le Caire")

# Avec placeholder
self.edit = CLineEdit(self, placeholderText="Entrez votre nom...")

# Signal validated
self.edit.validated.connect(self.on_validated)

def on_validated(self, text: str) -> None:
    print(text)


## CComboBox

### Définition
CComboBox est une liste déroulante accessible qui remplace QComboBox.

### Pourquoi ?
QComboBox active l'élément lors de la navigation avec les flèches —
problématique pour les utilisateurs aveugles.

### Solution
Séparation explicite entre navigation (flèches) et activation (Entrée/Espace).
Accessibilité NVDA maintenue en mode désactivé.

### Fonctionnalités
- Navigation libre : ↑↓ sans activation.
- Activation explicite : Entrée, Retour, Espace → signal `validated`.
- Signal `cleared` : émis si l'utilisateur interagit avec une liste vide.
- Désactivation accessible : NVDA annonce "indisponible".

### Utilisation

# PySide6
from cwidgets.pyside6 import CComboBox, CLabel, CMessageBox
# PyQt6
from cwidgets.pyqt6 import CComboBox, CLabel, CMessageBox

self.combo = CComboBox(self)
self.combo.addItems(["Égypte", "Tunisie", "Maroc"])
self.lbl = CLabel("Pays :", self, self.combo)
layout.addWidget(self.lbl)
layout.addWidget(self.combo)

self.combo.validated.connect(self.on_selection)
self.combo.cleared.connect(self.on_cleared)

def on_selection(self) -> None:
    text  = self.combo.currentText()
    index = self.combo.currentIndex()
    CMessageBox.information(self, "Sélection", f"Pays : {text}")

def on_cleared(self) -> None:
    CMessageBox.warning(self, "Avertissement", "Liste vide.")

# Désactiver / réactiver
self.combo.setEnabled(False)
self.combo.setEnabled(True)


## CListWidget

### Définition
CListWidget est une liste accessible qui remplace QListWidget.

### Pourquoi ?
QListWidget active l'élément immédiatement lors de la navigation —
obstacle pour les utilisateurs aveugles.

### Solution
Séparation entre navigation et activation. Accessibilité NVDA en mode désactivé.

### Fonctionnalités
- Navigation libre : ↑↓ sans activation.
- Activation explicite : Entrée, Retour, Espace.
- Désactivation accessible : NVDA annonce "indisponible".

### Utilisation

# PySide6
from cwidgets.pyside6 import CListWidget, CLabel
# PyQt6
from cwidgets.pyqt6 import CListWidget, CLabel

self.liste = CListWidget(self)
self.liste.addItems(["Irak", "Arabie Saoudite", "Koweït"])
self.lbl = CLabel("Pays :", self, self.liste)
layout.addWidget(self.lbl)
layout.addWidget(self.liste)

self.liste.itemActivated.connect(self.on_item)

def on_item(self, item) -> None:
    text = item.text()
    row  = self.liste.currentRow()
    print(row, text)

# Désactiver / réactiver
self.liste.setEnabled(False)
self.liste.setEnabled(True)

# Vider
self.liste.clear()


## CMessageBox

### Définition
CMessageBox est une boîte de dialogue accessible qui remplace QMessageBox.

### Pourquoi ?
QMessageBox ne propose pas de fermeture automatique.

### Solution
Ajout d'un mode chronométré avec fermeture automatique après un délai.

### Fonctionnalités
- `information` : chronométré ou non, sans son.
- `warning` : chronométré ou non, sans son.
- `critical` : toujours non chronométré + son système, fermeture manuelle requise.
- Fermeture manuelle toujours possible avant la fin du délai.

### Utilisation

# PySide6
from cwidgets.pyside6 import CMessageBox
# PyQt6
from cwidgets.pyqt6 import CMessageBox

# Information
CMessageBox.information(self, "Succès", "Fichier enregistré.")
CMessageBox.information(self, "Succès", "Fichier enregistré.", timeout=3000)

# Avertissement
CMessageBox.warning(self, "Avertissement", "Espace disque insuffisant.")
CMessageBox.warning(self, "Avertissement", "Connexion instable.", timeout=4000)

# Erreur — fermeture manuelle + son
CMessageBox.critical(self, "Erreur", "Fichier introuvable.")


## Bonnes pratiques

**1 — Titres : toujours utiliser CLabel avec buddy**
# Non recommandé
self.combo.setAccessibleName("...")

# Correct
self.lbl = CLabel("Pays :", self, self.combo)

**2 — Désactivation** : `setEnabled(False)` disponible sur tous les composants C*.

**3 — Activation**
- CLineEdit et CComboBox → signal `validated`
- CListWidget → signal `itemActivated`

**4 — Ordre de création avec buddy** : toujours créer l'élément avant son CLabel.
self.combo = CComboBox(self)
self.lbl   = CLabel("Pays :", self, self.combo)


## Configuration système requise

- PySide6 ou PyQt6
- pywin32 — uniquement pour CTextEdit (intégration Win32 RichEdit)
- Windows uniquement pour CTextEdit


## Limitations

- CTextEdit : Windows uniquement (dépend de Win32 RichEdit).
- CComboBox et CListWidget : `setAccessibleName` non recommandé — remplace le CLabel buddy.
- CButton : ombre grise via stylesheet — Windows n'ombre pas automatiquement
  le bouton maintenu actif pour NVDA.


## Développeur

Mohamed Hédi Bettaieb (Tunisie)
Email : hedidouz@gmail.com
Date de conception : mai 2026


## Conclusion

CWidgets vise à rendre les applications Qt 100 % accessibles aux développeurs
et utilisateurs aveugles, sans sacrifier la productivité ni les habitudes Qt.
