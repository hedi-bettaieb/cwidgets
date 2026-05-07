# CWidgets — Composants Qt Accessibles pour NVDA

## Introduction

cwidgets est une librairie Python fournissant une collection de widgets Qt accessibles pour NVDA,
conçus pour résoudre les limitations natives de Qt en matière d'accessibilité.
Chaque composant étend un widget Qt standard en ajoutant les fonctionnalités essentielles pour les
utilisateurs de lecteurs d'écran, tout en conservant une API familière pour les développeurs.

Compatible avec PySide6 et PyQt6 :

    # PySide6
    from cwidgets.pyside6 import CButton, CLabel, CLineEdit, ...
    # PyQt6
    from cwidgets.pyqt6 import CButton, CLabel, CLineEdit, ...

## Installation

    pip install cwidgets

## Accéder à l'aide

Après installation, deux fonctions sont disponibles directement depuis le module :

    import cwidgets

    # lister tous les widgets disponibles
    cwidgets.widgets()

    # ouvrir le guide dans le navigateur (français par défaut)
    cwidgets.show_help()
    cwidgets.show_help(lang="fr")
    cwidgets.show_help(lang="en")
    cwidgets.show_help(lang="ar")

    # ouvrir directement la section d'un widget
    cwidgets.show_help(lang="fr", widget="CButton")
    cwidgets.show_help(lang="fr", widget="CTextEdit")
    cwidgets.show_help(lang="fr", widget="CLabel")
    cwidgets.show_help(lang="fr", widget="CLineEdit")
    cwidgets.show_help(lang="fr", widget="CComboBox")
    cwidgets.show_help(lang="fr", widget="CListWidget")
    cwidgets.show_help(lang="fr", widget="CMessageBox")

## Problématiques communes résolues

- Zone de texte multiligne : CTextEdit résout le problème fondamental de QTextEdit, totalement inaccessible pour NVDA.
- Navigation vs validation : séparation des actions de navigation (flèches) et de validation (Enter/Space) pour éviter les déclenchements involontaires.
- Désactivation accessible : maintien de l'annonce NVDA même lorsque le widget est désactivé (setEnabled(False)).
- Titres et labels : intégration avec CLabel pour éviter les conflits avec setAccessibleName.

## Détails des widgets

---

## CTextEdit

### Définition
CTextEdit est une zone d'édition multiligne accessible, remplaçant QTextEdit.

### Pourquoi — Le problème fondamental
QTextEdit natif Qt est totalement inaccessible pour NVDA — un développeur non-voyant ne peut ni lire
ni écrire dans une zone de texte multiligne. C'est le problème le plus bloquant de Qt pour
l'accessibilité, sans aucune solution native.
Ce problème a conduit à l'abandon des zones d'édition multiligne dans de nombreuses applications Qt
développées par des personnes non-voyantes.

### Solution — RichEdit Win32 intégré dans Qt
La solution adoptée consiste à intégrer le contrôle Win32 RichEdit directement dans un QWidget Qt.
Win32 RichEdit est nativement accessible — la complexité réside dans son intégration dans une fenêtre
Qt tout en conservant cette accessibilité et en harmonisant le comportement avec Qt.

Architecture :

    CTextEdit (QWidget)
        └── EditorStyle        — styles, police, couleur, alignement
                └── RichEdit Win32  — moteur natif accessible

### Fonctionnalités
- Accessibilité NVDA totale : lecture, écriture, navigation, sélection.
- API compatible QTextEdit : setText, toPlainText, append, clear, setReadOnly.
- Texte enrichi : police, taille, gras, italique, couleur, alignement.
- Gestion asynchrone : styles et texte en attente si le handle Win32 n'est pas encore disponible.
- Focus intelligent : restauration du focus au retour de l'application.

### Utilisation

    # PySide6
    from cwidgets.pyside6 import CTextEdit
    # PyQt6
    from cwidgets.pyqt6 import CTextEdit

    # création
    self.editor = CTextEdit(self, accessible_name="Zone de saisie")
    layout.addWidget(self.editor)

    # texte
    self.editor.setText("Bonjour !")
    text = self.editor.text()
    text = self.editor.toPlainText()
    self.editor.append("Nouvelle ligne.")
    self.editor.clear()

    # lecture seule
    self.editor.setReadOnly(True)
    self.editor.setReadOnly(False)

    # police — QFont ou (str, int, bool, bool)
    self.editor.setFont("Arial", 12, True, False)  # nom, taille, gras, italique

    # couleurs — nom ou tuple RGB
    self.editor.setTextColor("red")
    self.editor.setTextColor((255, 0, 0))
    self.editor.setBackgroundColor("yellow")

    # alignement
    self.editor.setAlignment("left")
    self.editor.setAlignment("center")
    self.editor.setAlignment("right")

### Couleurs disponibles

    # noms supportés
    "black", "white", "red", "green", "blue", "yellow",
    "cyan", "magenta", "gray", "darkgray", "lightgray",
    "orange", "purple", "violet", "pink", "brown",
    "navy", "teal", "lime", "olive", "maroon",
    "coral", "salmon", "gold", "silver"

    # ou tuple RGB
    (255, 0, 0)    # rouge
    (0, 128, 255)  # bleu clair

### Titre visible optionnel
accessible_name est annoncé par NVDA mais invisible visuellement.
Pour un titre visible, ajouter un CLabel au layout avant l'éditeur :

    self.lbl    = CLabel("Zone de saisie :", self)
    self.editor = CTextEdit(self, accessible_name="Zone de saisie")
    layout.addWidget(self.lbl)
    layout.addWidget(self.editor)

---

## CLabel

### Définition
CLabel est un label accessible, remplaçant QLabel.

### Pourquoi ?
QLabel natif est invisible pour NVDA sauf s'il est lié à un buddy — et seulement quand ce buddy a le focus.

### Solution
Deux modes :
- Mode seul : StrongFocus + accessibleName — NVDA lit le label directement.
- Mode buddy : NoFocus sur le label, texte propagé comme accessibleName du buddy — NVDA annonce le label quand le buddy reçoit le focus.

### Fonctionnalités
- Nettoyage des raccourcis : &Nom → "Nom" pour NVDA, mnémonique visuel Qt conservé.
- Préfixe : contexte textuel ajouté à l'annonce NVDA ("Statut fichier enregistré").
- Synchronisation automatique : setText() et setPrefix() resynchronisent NVDA sans code supplémentaire.

### Utilisation

    # PySide6
    from cwidgets.pyside6 import CLabel, CLineEdit
    # PyQt6
    from cwidgets.pyqt6 import CLabel, CLineEdit

    # Mode seul — NVDA lit le texte directement
    self.lbl = CLabel("Fichier enregistré", self)

    # Avec préfixe — NVDA annonce : "Statut fichier enregistré"
    self.lbl = CLabel("Fichier enregistré", self, prefix="Statut")

    # Mode buddy — NVDA annonce le label quand le champ reçoit le focus
    # le label doit être ajouté au layout avant le widget
    self.edit = CLineEdit(self)
    self.lbl  = CLabel("Nom :", self, self.edit)
    layout.addWidget(self.lbl)
    layout.addWidget(self.edit)

    # Mise à jour dynamique
    self.lbl.setText("traitement en cours")
    self.lbl.setPrefix("Erreur")

---

## CButton

### Définition
CButton est un bouton accessible, remplaçant QPushButton.

### Pourquoi ?
- QPushButton natif n'accepte que Space pour l'activation — Enter et Return sont ignorés.
- setEnabled(False) rend le bouton invisible pour NVDA, même avec setAccessibleDescription.

### Solution
Activation étendue à Enter/Return et désactivation accessible via maintien du widget actif pour Qt
tout en bloquant les interactions manuellement.

### Fonctionnalités
- Activation étendue : Space, Enter, Return, clic souris.
- Désactivation accessible : non cliquable + NVDA annonce "non disponible".
- API identique à QPushButton.

### Utilisation

    # PySide6
    from cwidgets.pyside6 import CButton
    # PyQt6
    from cwidgets.pyqt6 import CButton

    self.btn = CButton("Valider", self)
    self.btn.clicked.connect(self.on_click)

    # désactiver — NVDA annonce "non disponible", bouton non cliquable
    self.btn.setEnabled(False)
    self.btn.setEnabled(True)

    # modifier le titre — natif Qt
    self.btn.setText("Nouveau titre")

    # vérifier l'état
    if self.btn.isEnabled():
        ...

---

## CLineEdit

### Définition
CLineEdit est un champ de saisie accessible, remplaçant QLineEdit.

### Pourquoi ?
QLineEdit natif nécessite une connexion manuelle à returnPressed pour récupérer le texte validé.
CLineEdit rend cette validation automatique via le signal validated.

### Fonctionnalités
- Signal validated émis avec le texte courant à chaque Enter/Return.
- placeholderText en paramètre — annoncé par NVDA quand le champ est vide.
- Titre via CLabel avec buddy.

### Utilisation

    # PySide6
    from cwidgets.pyside6 import CLineEdit, CLabel
    # PyQt6
    from cwidgets.pyqt6 import CLineEdit, CLabel

    # champ créé en premier pour le buddy
    self.edit = CLineEdit(self)
    self.lbl  = CLabel("Nom :", self, self.edit)
    layout.addWidget(self.lbl)
    layout.addWidget(self.edit)

    # avec texte initial
    self.edit = CLineEdit(self, "Paris")

    # avec placeholder
    self.edit = CLineEdit(self, placeholderText="Saisissez votre nom...")

    # signal validated
    self.edit.validated.connect(self.on_validated)

    def on_validated(self, text: str) -> None:
        text = self.edit.text()  # récupération natif Qt

    # show / hide — natif Qt
    self.edit.hide()
    self.edit.show()

---

## CComboBox

### Définition
CComboBox est une liste déroulante accessible, remplaçant QComboBox.

### Pourquoi ?
- QComboBox natif valide immédiatement la sélection lors de la navigation avec les flèches — un non-voyant ne peut pas naviguer sans déclencher une action.
- setEnabled(False) rend le widget muet pour NVDA.

### Solution
Séparation explicite entre navigation et validation, avec maintien de l'accessibilité en mode désactivé.

### Fonctionnalités
- Navigation libre : ↑ ↓ naviguent sans valider.
- Validation explicite : Enter, Return, Space → signal validated.
- Signal cleared : émis quand l'utilisateur valide sur un combo vide.
- Désactivation accessible : NVDA annonce "non disponible".
- Titre via CLabel avec buddy — setAccessibleName non recommandé car il écrase le label.

### Utilisation

    # PySide6
    from cwidgets.pyside6 import CComboBox, CLabel, CMessageBox, CButton
    # PyQt6
    from cwidgets.pyqt6 import CComboBox, CLabel, CMessageBox, CButton

    # combo créé en premier pour le buddy
    self.combo = CComboBox(self)
    self.combo.addItems(["France", "Belgique", "Suisse"])
    self.lbl = CLabel("Liste des pays :", self, self.combo)
    layout.addWidget(self.lbl)
    layout.addWidget(self.combo)

    self.combo.validated.connect(self.on_selection)
    self.combo.cleared.connect(self.on_cleared)

    # bouton qui vide le combo
    self.btn_vider = CButton("Vider", self)
    self.btn_vider.clicked.connect(self.combo.clear)

    def on_selection(self) -> None:
        text  = self.combo.currentText()
        index = self.combo.currentIndex()
        CMessageBox.information(self, "Sélection", f"Pays : {text}")

    def on_cleared(self) -> None:
        CMessageBox.warning(self, "Attention", "Aucun item disponible dans la liste.")

    # désactiver / réactiver
    self.combo.setEnabled(False)
    self.combo.setEnabled(True)

---

## CListWidget

### Définition
CListWidget est une liste accessible, remplaçant QListWidget.

### Pourquoi ?
QListWidget natif valide immédiatement la sélection lors de la navigation avec les flèches — un non-voyant ne peut pas naviguer librement.

### Solution
Séparation entre navigation et validation, avec maintien de l'accessibilité en mode désactivé.

### Fonctionnalités
- Navigation libre : ↑ ↓ naviguent sans valider.
- Validation explicite : Enter, Return, Space → émet itemActivated natif Qt.
- Désactivation accessible : NVDA annonce "non disponible".
- Titre via CLabel avec buddy — setAccessibleName non recommandé car il écrase le label.

### Utilisation

    # PySide6
    from cwidgets.pyside6 import CListWidget, CLabel
    # PyQt6
    from cwidgets.pyqt6 import CListWidget, CLabel

    # liste créée en premier pour le buddy
    self.liste = CListWidget(self)
    self.liste.addItems(["France", "Belgique", "Suisse"])
    self.lbl = CLabel("Liste des pays :", self, self.liste)
    layout.addWidget(self.lbl)
    layout.addWidget(self.liste)

    # signal natif Qt — identique à QListWidget
    self.liste.itemActivated.connect(self.on_item)

    def on_item(self, item) -> None:
        text = item.text()
        row  = self.liste.currentRow()
        print(row, text)

    # désactiver / réactiver
    self.liste.setEnabled(False)
    self.liste.setEnabled(True)

    # vider — natif Qt
    self.liste.clear()

---

## CMessageBox

### Définition
CMessageBox est une boîte de dialogue accessible, remplaçant QMessageBox.

### Pourquoi ?
QMessageBox natif ne propose pas de fermeture automatique temporisée — utile pour les messages
d'information ou de succès qui ne nécessitent pas d'action.

### Solution
Ajout d'un mode temporisé optionnel pour les messages non critiques.

### Fonctionnalités
- information : modal ou temporisé — sans beep.
- warning : modal ou temporisé — sans beep.
- critical : toujours modal + beep système — fermeture manuelle obligatoire.
- Fermeture manuelle toujours possible avant le timeout.

### Utilisation

    # PySide6
    from cwidgets.pyside6 import CMessageBox
    # PyQt6
    from cwidgets.pyqt6 import CMessageBox

    # information modale
    CMessageBox.information(self, "Succès", "Fichier enregistré.")

    # information temporisée — fermeture auto après 3 secondes
    CMessageBox.information(self, "Succès", "Fichier enregistré.", timeout=3000)

    # avertissement modal
    CMessageBox.warning(self, "Attention", "Espace disque insuffisant.")

    # avertissement temporisé
    CMessageBox.warning(self, "Attention", "Connexion instable.", timeout=4000)

    # erreur critique — modal + beep — fermeture manuelle obligatoire
    CMessageBox.critical(self, "Erreur", "Fichier introuvable.")

    # timeout recommandé uniquement pour information et warning
    # timeout non disponible pour critical

---

## Bonnes pratiques

1 — Titres : toujours utiliser CLabel avec buddy pour les widgets interactifs.

    # non recommandé — écrase le buddy
    self.combo.setAccessibleName("...")

    # correct
    self.lbl = CLabel("Liste des pays :", self, self.combo)

2 — Désactivation : setEnabled(False) est accessible par défaut sur tous les widgets C*.

3 — Validation :
- CLineEdit et CComboBox → signal validated
- CListWidget → signal natif Qt itemActivated

4 — Ordre de création avec buddy : toujours créer le widget avant son CLabel.

    # correct — widget créé avant le label
    self.combo = CComboBox(self)
    self.lbl   = CLabel("Pays :", self, self.combo)

---

## Dépendances

- PySide6 ou PyQt6
- pywin32 — uniquement pour CTextEdit (intégration Win32 RichEdit)

Fournies par la librairie :
- validate_parent — vérification systématique du parent QWidget
- logger — journalisation des erreurs (module "cwidgets")

## Limites

- CTextEdit dépend de Win32 RichEdit — compatible Windows uniquement.
- setAccessibleName non recommandé avec CComboBox et CListWidget car il écrase le buddy CLabel.
- CButton : visuel grisé via stylesheet — Windows ne grise pas automatiquement un bouton maintenu actif pour NVDA.

## Conclusion

Ce projet vise à rendre les applications Qt 100% accessibles pour les développeurs et utilisateurs
non-voyants, sans sacrifier la productivité ni les habitudes des développeurs Qt.
