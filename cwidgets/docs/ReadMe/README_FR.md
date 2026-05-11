# Guide de l'utilisateur - Bibliothèque CWidgets V0.1.0 :

## Introduction
CWidgets : Votre puissance de programmation illimitée
Transformer les obstacles Qt en opportunités créatives
CWidgets est une bibliothèque Python spécialisée qui donne aux développeurs aveugles un contrôle total sur les interfaces PyQt6 et PySide6.
L'ère des limitations avec QTextEdit est révolue - désormais, vous pouvez concevoir des interfaces contenant des zones d'édition multi-lignes avec une liberté et une compatibilité totales.
La bibliothèque offre une compatibilité absolue pour les développeurs aveugles, car tous les éléments sont conçus pour fonctionner parfaitement avec le lecteur d'écran NVDA.
Continuité de la créativité : Pas besoin d'apprendre de nouveaux outils - continuez à écrire votre code familier tout en conservant les mêmes fonctions et caractéristiques.
Ingénierie intelligente : Chaque élément de CWidgets hérite des propriétés des éléments Qt originaux, garantissant des performances standard avec des solutions radicales aux problèmes de compatibilité.
Qu'est-ce qui changera lorsque vous écrirez votre code d'application basée sur des fenêtres PyQt6 et PySide6 ?
Tout ce que vous avez à faire est de remplacer simplement la première lettre (C au lieu de Q) :
CTextEdit au lieu de QTextEdit.
CButton au lieu de QPushButton.
Où C signifie Custom
Flexibilité totale dans le travail, car la bibliothèque supporte votre environnement de travail préféré avec la même efficacité :
Avec PySide6 :
from cwidgets.pyside6 import CButton, CLabel, CLineEdit


Avec PyQt6 :

from cwidgets.pyqt6 import CButton, CLabel, CLineEdit

CWidgets : Codez avec confiance, concevez sans limites.

## Composants disponibles :
7 éléments personnalisés entièrement compatibles fournis par cette bibliothèque sont :
1-CTextEdit
2-CButton
3-CLabel
4-CLineEdit
5-CComboBox
6-CListWidget
7-CMessageBox

## Installation

pip install cwidgets


## Accéder à l'aide

Après l'installation, commencez à explorer la bibliothèque, ses composants, propriétés et utilisation grâce à ces fonctions :

import cwidgets

# Liste de tous les composants disponibles
cwidgets.widgets()

# Liste de toutes les sections disponibles
cwidgets.sections()

# Ouvrir le guide complet dans le navigateur
cwidgets.show_help()
cwidgets.show_help(lang="ar")

# Ouvrir un composant spécifique directement
cwidgets.show_help(lang="ar", goto="CButton")
cwidgets.show_help(lang="ar", goto="CTextEdit")

# Ouvrir une section spécifique directement
cwidgets.show_help(lang="ar", goto="introduction")
cwidgets.show_help(lang="ar", goto="installation")


## Problèmes courants résolus

#CTextEdit :
Zone d'édition multi-lignes : CTextEdit résout le problème fondamental de QTextEdit, qui est incompatible avec NVDA.
#CComboBox & CListWidget :
Séparation navigation-activation : Séparer les actions de navigation (flèches) des actions d'activation (Entrée/Espace) pour éviter les activations involontaires.
Disponibilité : Maintenir l'annonce NVDA même lorsque le composant est désactivé.
#CButton :
Activation avec entrée, retour, espace et clic de souris.
Compatibilité même lorsque désactivé.
#CLabel
Compatibilité améliorée pour les titres et étiquettes
#CLineEdit :
Permet de récupérer le texte à l'intérieur de l'élément en appuyant sur entrée sans aucun code supplémentaire.
#CMessageBox :
Boîtes de dialogue de message à fermeture automatique.
Vous pouvez spécifier un temps après lequel la boîte de dialogue disparaît automatiquement.
#À l'exception de CTextEdit, tous les autres composants héritent de QT et conservent donc toutes leurs propriétés et fonctions de base.

## Détails des composants :
Définition, Création, Propriétés, Utilisation.

## CTextEdit

### Définition
CTextEdit est une zone d'édition multi-lignes entièrement compatible avec NVDA.

### Pourquoi — Le problème fondamental
- Le QTextEdit original dans Qt est incompatible avec NVDA.
- Les développeurs aveugles ne peuvent pas lire ou écrire dans cet élément.
C'est la barrière qui empêche les aveugles de concevoir des interfaces QT contenant des zones d'édition multi-lignes.
Jusqu'à l'apparition de cette bibliothèque, aucune solution connue n'était utilisée par les aveugles pour ce problème.

### Solution — RichEdit Win32 intégré dans Qt
La solution fournie par cette bibliothèque est d'intégrer directement un contrôle RichEdit Win32 dans la fenêtre QT.
RichEdit Win32 est nativement entièrement compatible avec NVDA.
La partie complexe de la conception de la solution a été de l'intégrer dans la fenêtre Qt tout en maintenant cette accessibilité.
La bibliothèque a également assuré l'utilisation par défaut des commandes QT.
Structure de l'élément QTextEdit :
-QTextEdit
-EditorStyle — Styles, police, couleur, alignement
-RichEdit Win32 — Le moteur compatible original

### Fonctionnalités
- Accessibilité NVDA complète : lecture, écriture, navigation, sélection.
- API compatible avec QTextEdit : setText, toPlainText, append, clear, setReadOnly.
- Texte formaté : police, taille, gras, italique, couleur, alignement.
- Gestion asynchrone : les styles et le texte sont mis en file d'attente si le handle Win32 n'est pas encore disponible.
- Focus intelligent : restaure le focus lors du retour à l'application.

### Utilisation


# PySide6
from cwidgets.pyside6 import CTextEdit
# PyQt6
from cwidgets.pyqt6 import CTextEdit

# Création
self.editor = CTextEdit(self, accessible_name="Nom de la boîte")
layout.addWidget(self.editor)

# Insérer du texte dans la boîte
self.editor.setText("Bonjour !")
# Récupérer le texte de la boîte :
text = self.editor.text()
text = self.editor.toPlainText()
# Ajouter du texte au texte original
self.editor.append("Nouvelle ligne.")
# Effacer le texte pour vider la boîte
self.editor.clear()

# Rendre la boîte en lecture seule
self.editor.setReadOnly(True)
# Désactiver la lecture seule pour rendre la boîte modifiable
self.editor.setReadOnly(False)

# Police — QFont ou (str, int, bool, bool)
self.editor.setFont("Arial", 12, True, False)  # Nom, taille, gras, italique

# Couleurs — nom ou ensemble RGB
self.editor.setTextColor("red")
self.editor.setTextColor((255, 0, 0))
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

# Ou ensemble RGB
(255, 0, 0)    # rouge
(0, 128, 255)  # bleu clair


### Titre visuel optionnel
accessible_name est lu par NVDA mais n'est pas visuellement visible.
Pour ajouter un titre visuel, ajoutez un CLabel au layout avant l'éditeur :

self.editor = CTextEdit(self)
self.lbl    = CLabel("Zone d'édition :", self, self.editor)

Il est important de noter que l'ajout de CLabel au layout doit précéder l'ajout de l'éditeur afin que le nom de la boîte apparaisse au-dessus de la boîte, et non en dessous.

layout.addWidget(self.lbl)
layout.addWidget(self.editor)


## CLabel

### Définition
CLabel est une étiquette compatible NVDA qui remplace QLabel.

### Pourquoi ?
Le QLabel original est invisible pour NVDA sauf s'il est lié à un buddy - et seulement lorsque ce buddy a le focus.

### Solution
Deux modes :
- Mode simple : compatible NVDA et reconnu même avec la navigation par tabulation.
- Mode buddy : lorsque CLabel est lié à un autre élément.

### Fonctionnalités
- Nettoyage des raccourcis : &Nom → "Nom" pour NVDA, raccourci visuel pour Qt préservé.
- prefix : Texte supplémentaire exemple lors de l'expression d'un statut.

- Synchronisation par défaut :
Changement du contenu de l'étiquette.
setText()
Changement du texte supplémentaire :
setPrefix()
Ils se resynchronisent sans code supplémentaire.

### Utilisation


# PySide6
from cwidgets.pyside6 import CLabel, CLineEdit
# PyQt6
from cwidgets.pyqt6 import CLabel, CLineEdit

# Mode simple — NVDA lit le texte et est accessible via tab :
self.lbl = CLabel("Fichier enregistré", self)

# Avec préfixe — NVDA annonce : "statut fichier enregistré"
self.lbl = CLabel("Fichier enregistré", self, prefix="statut")

# Mode buddy — NVDA annonce l'étiquette lorsque le champ obtient le focus
# L'étiquette doit être ajoutée au layout avant le champ d'édition pour apparaître visuellement au-dessus
self.edit = CLineEdit(self)
self.lbl  = CLabel("Nom :", self, self.edit)
layout.addWidget(self.lbl)
layout.addWidget(self.edit)

# Mise à jour dynamique
self.lbl.setText("Traitement en cours")
self.lbl.setPrefix("erreur")


## CButton

### Définition
CButton est un bouton avec des fonctionnalités supplémentaires qui le rendent utilisable sans avoir besoin des lignes de code du bouton original pour activer ces fonctionnalités.

### Pourquoi ?
- Le QPushButton original n'accepte que la barre d'espace pour l'activation — Entrée et Retour sont ignorés.
- setEnabled(False) rend le bouton invisible pour NVDA, même avec setAccessibleDescription.

### Solution
- Activation incluant Entrée/Retour.
- Désactivation du bouton tout en maintenant la compatibilité.
Le bouton reste visuellement "actif" mais ne fonctionne pas.
C'est la solution : offrir la possibilité de désactiver tout en maintenant la compatibilité, contrairement à QPushButton qui disparaît de NVDA lorsqu'il est désactivé.

### Fonctionnalités
- Activation étendue : Espace, Entrée, Retour, clic de souris.
- Désactivation disponible : Non cliquable + NVDA annonce "indisponible".
- API correspondant à QPushButton.

### Utilisation


# PySide6
from cwidgets.pyside6 import CButton
# PyQt6
from cwidgets.pyqt6 import CButton

self.btn = CButton("Enregistrer", self)
self.btn.clicked.connect(self.on_click)

# Désactiver — NVDA annonce "indisponible", bouton non cliquable
self.btn.setEnabled(False)
self.btn.setEnabled(True)

# Changer le titre — Qt original
self.btn.setText("Nouveau titre")

# Vérifier l'état
if self.btn.isEnabled():
    ...


## CLineEdit

### Définition
CLineEdit est un champ de saisie de texte compatible qui remplace QLineEdit.

### Pourquoi ?
QLineEdit nécessite une ligne de code supplémentaire pour récupérer le texte.
CLineEdit rend cette activation automatique via le signal validated.

### Fonctionnalités
- Le signal validated émet avec le texte actuel à chaque Entrée/Retour.
- placeholderText en paramètre — annoncé par NVDA lorsque le champ est vide.
- Titre via CLabel avec buddy.

### Utilisation


# PySide6
from cwidgets.pyside6 import CLineEdit, CLabel
# PyQt6
from cwidgets.pyqt6 import CLineEdit, CLabel

# Créer d'abord le champ pour le buddy
self.edit = CLineEdit(self)
self.lbl  = CLabel("Nom :", self, self.edit)
layout.addWidget(self.lbl)
layout.addWidget(self.edit)

# Avec texte initial
self.edit = CLineEdit(self, "Le Caire")

# Avec texte d'espace réservé
self.edit = CLineEdit(self, placeholderText="Entrez votre nom...")

# Signal validated
self.edit.validated.connect(self.on_validated)

def on_validated(self, text: str) -> None:
    text = self.edit.text()  # Récupération Qt originale
    print(text)

# Afficher/masquer — Qt original
self.edit.hide()
self.edit.show()


## CComboBox

### Définition
CComboBox est une liste déroulante compatible qui remplace QComboBox.

### Pourquoi ?
- L'activation de QComboBox original se produit en interne avec les flèches.
Cela pose problème aux utilisateurs aveugles qui naviguent avec les flèches.

### Solution
Séparation explicite entre la navigation et l'activation.
Maintien de la compatibilité même lorsque la liste est désactivée.

### Fonctionnalités
- Navigation libre : ↑ ↓ pour la navigation sans activation.
- Activation explicite : Entrée, Retour, Espace → via le signal validated.
- Signal cleared : Émis lorsque l'utilisateur consulte une liste vide.
- Désactivation disponible : NVDA annonce "indisponible".
- Titre via CLabel avec buddy — l'utilisation de setAccessibleName n'est pas recommandée car elle remplace l'étiquette.

### Utilisation


# PySide6
from cwidgets.pyside6 import CComboBox, CLabel, CMessageBox, CButton
# PyQt6
from cwidgets.pyqt6 import CComboBox, CLabel, CMessageBox, CButton

# Créer d'abord la liste pour le buddy
self.combo = CComboBox(self)
self.combo.addItems(["Égypte", "Tunisie", "Maroc"])
self.lbl = CLabel("Liste des pays :", self, self.combo)
layout.addWidget(self.lbl)
layout.addWidget(self.combo)

self.combo.validated.connect(self.on_selection)
self.combo.cleared.connect(self.on_cleared)

# Bouton pour vider la liste
self.btn_clear = CButton("Vider", self)
self.btn_clear.clicked.connect(self.combo.clear)

def on_selection(self) -> None:
    text  = self.combo.currentText()
    index = self.combo.currentIndex()
    CMessageBox.information(self, "Sélection", f"Pays : {text}")

def on_cleared(self) -> None:
    CMessageBox.warning(self, "Avertissement", "Aucun élément disponible dans la liste.")

# Désactiver/réactiver
self.combo.setEnabled(False)
self.combo.setEnabled(True)


## CListWidget

### Définition
CListWidget est une liste compatible qui remplace QListWidget.

### Pourquoi ?
L'activation de QListWidget original se produit immédiatement lors de la navigation avec les flèches.
C'est un obstacle pour les utilisateurs aveugles, et désactiver cette activation avec les flèches nécessite des lignes de code supplémentaires.

### Solution
- Séparation entre la navigation et l'activation.
- Maintien de l'accessibilité en mode désactivé.

### Fonctionnalités
- Navigation libre : ↑ ↓ pour la navigation sans activation.
- Activation explicite : Entrée, Retour, Espace.
- Lorsque désactivé : NVDA annonce "indisponible".
- Titre via CLabel avec buddy — l'utilisation de setAccessibleName n'est pas recommandée car elle remplace l'étiquette.

### Utilisation


# PySide6
from cwidgets.pyside6 import CListWidget, CLabel
# PyQt6
from cwidgets.pyqt6 import CListWidget, CLabel

# Créer la liste
self.list = CListWidget(self)
self.list.addItems(["Irak", "Arabie Saoudite", "Koweït"])
self.lbl = CLabel("Liste des pays :", self, self.list)
layout.addWidget(self.lbl)
layout.addWidget(self.list)

# Signal Qt original — correspond à QListWidget
self.liste.itemActivated.connect(self.on_item)

def on_item(self, item) -> None:
    text = item.text()
    row  = self.liste.currentRow()
    print(row, text)

# Désactiver/réactiver
self.liste.setEnabled(False)
self.liste.setEnabled(True)

# Vider — Qt original
self.liste.clear()


## CMessageBox

### Définition
CMessageBox est une boîte de dialogue de message compatible.

### Pourquoi ?
QMessageBox original ne fournit pas de fermeture automatique.
Nous en avons besoin pour les messages qui ne nécessitent pas d'intervention de l'utilisateur.

### Solution
Ajout d'un mode où le message se ferme après un temps spécifié.

### Fonctionnalités
- information : Chronométré ou non chronométré — pas de son.
- warning : Chronométré ou non chronométré — pas de son.
- critical : Toujours non chronométré + son système — fermeture manuelle requise.
- Fermeture manuelle toujours possible avant la fin du délai.

### Utilisation


# PySide6
from cwidgets.pyside6 import CMessageBox
# PyQt6
from cwidgets.pyqt6 import CMessageBox

# Information non chronométrée
CMessageBox.information(self, "Succès", "Fichier enregistré.")

# Information chronométrée — fermeture automatique après 3 secondes
CMessageBox.information(self, "Succès", "Fichier enregistré.", timeout=3000)

# Avertissement non chronométré
CMessageBox.warning(self, "Avertissement", "Espace disque insuffisant.")

# Avertissement chronométré
CMessageBox.warning(self, "Avertissement", "Connexion instable.", timeout=4000)

# Erreur — non chronométré + son — fermeture manuelle requise
CMessageBox.critical(self, "Erreur", "Fichier introuvable.")

# Le délai est recommandé uniquement pour information et warning
# Délai non disponible pour critical


## Bonnes pratiques

1 — Titres : Toujours utiliser CLabel avec buddy.


# Non recommandé — remplace l'étiquette
self.combo.setAccessibleName("...")

# Correct
self.lbl = CLabel("Liste des pays :", self, self.combo)


2 — Désactivation : setEnabled(False) est disponible par défaut sur tous les composants C*.

3 — Activation :
- CLineEdit et CComboBox → signal validated
- CListWidget → signal itemActivated original de Qt

4 — Ordre de création avec buddy : Toujours créer l'élément avant son CLabel.


# Correct — élément créé avant l'étiquette
self.combo = CComboBox(self)
self.lbl   = CLabel("Pays :", self, self.combo)


## Configuration système requise

- PySide6 ou PyQt6
- pywin32 — uniquement pour CTextEdit (intégration Win32 RichEdit)

Fourni par la bibliothèque :
- validate_parent — Vérification régulière de la fenêtre parente
- logger — Journalisation des erreurs (module "cwidgets")

## Limitations de la bibliothèque

- CTextEdit dépend de Win32 RichEdit — compatibilité Windows uniquement.
- L'utilisation de setAccessibleName avec CComboBox et CListWidget n'est pas recommandée car elle remplace le CLabel buddy.
- CButton : Ombre grise via stylesheet — Windows n'ombrage pas automatiquement le bouton lorsqu'on le maintient actif pour NVDA.

## Développeur :
Mohamed Hédi Bettaieb (Tunisie)
Contactez moi :
Email : hedidouz@gmail.com
Date de conception de la bibliothèque : mai 2026.

## Conclusion

Ce projet vise à rendre les applications Qt 100 % accessibles aux développeurs et utilisateurs aveugles, sans sacrifier la productivité ni les habitudes des développeurs Qt.