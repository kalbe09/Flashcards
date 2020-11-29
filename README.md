# Kicards
Webbasierte Karteikarten App <br>

Um das kollektive Lernen zu unterstützen, ist diese App nach Anforderungen der Open Education Richtlinien erstellt worden.<br>

ALMS-Framework <br>
* «A» (Access to editing tools), <br>
  * Betriebssystemunabhängigkeit <br>
  * Freiheit  der  Bearbeitungssoftware <br>
* «L» (Level of expertise required to revise or remix), <br>
  * benötigte Expertise zur Software-Nutzung <br>
  * sollte möglichst  gering  sein <br>
* «M» (Meaningfully editable) <br>
	* Editierbarkeit  der erstellten Materialien <br>
* «S» (Source-file access) zur Präzisierung technischer Offenheit vorgestellt. <br>
  * Verfügbarkeit der Quellmaterialien. <br>


## Gewünschte Funktionen
* Votesystem, um schlechte Karten auszusortieren
* Import / Export 
* Online-Repository, um Änderungen in Echtzeit zu verfolgen
* Editorleiste für einfachere Erstellung von KK
* Erstellung: nächste Karte (immer nächste Karte)
* Neue Lektion erstellen
* Seit dem 25th November 2020 ein registrierter Benutzer
  * Datum auf Deutsch ändern

## Todos
- Fehlermeldung bei doppelten Lektionen
- Gui: Lektion anklicken und danach filtern
- Fehlerquote
- Mathematische Formeln
- Votesystem (Anzahl User zählen * 90% dann delete)
- Import/export
- Einstellbare Frist (Klausurtermin)
- karten
  - letzte Abfrage
  - phase
  - nächste Abfrage


## Fragen
- Quellen zu flask tutorial etc.? 



## Erledigt 
- Wahr/Falsch Button anders platzieren


## Funkionen
You can 
* Registrierung eines User Accounts
* Erstellung eigener Themengebiete  
* Erstellung verschiedener Lektionen
* Erstellung von Karteikarten in den Themengebieten
* Abfrage der Karteikarten
* Angabe von Richtig oder Falsch
* Nur die falschen Karteikarten lernen
* Markdown Text für die Erstellung und Bearbeitung


## Installation
1. Anforderungen installieren

```pip install -r requirements/common.txt```

2. Datenbank erstellen

```python3 manage.py db init```
- Erstellt den Ordner migrations

```python3 manage.py db migrate```


```python3 manage.py db upgrade```

3. Webapplikation / Server starten

```python3 manage.py runserver```




The Application was created and tested with Python Version 3.5

To run the tests execute

```python3 manage.py test```

To open a shell within the App Context run

```python3 manage.py shell```

## Screenshots of the Application

Main Screen of the Application

![markdown-preview GitHub style](https://raw.githubusercontent.com/KevDi/Flashcards/screens/screens/Mainscreen.png)

List of Flashcards

![markdown-preview GitHub style](https://raw.githubusercontent.com/KevDi/Flashcards/screens/screens/Flashcardcollection.png)

Display of Flashcard without Markdown

![markdown-preview GitHub style](https://raw.githubusercontent.com/KevDi/Flashcards/screens/screens/flashcard.png)

Display of Flashcard with Markdown in the Answer

![markdown-preview GitHub style](https://raw.githubusercontent.com/KevDi/Flashcards/screens/screens/Flashcard_Markdown.png)

User Profile

![markdown-preview GitHub style](https://raw.githubusercontent.com/KevDi/Flashcards/screens/screens/User_profile.png)

Learn Page

![markdown-preview GitHub style](https://raw.githubusercontent.com/KevDi/Flashcards/screens/screens/Learn.png)

Learn Page with Answer

![markdown-preview GitHub style](https://raw.githubusercontent.com/KevDi/Flashcards/screens/screens/Learn_with_answer.png)

Creation of a new Flashcardcollection

![markdown-preview GitHub style](https://raw.githubusercontent.com/KevDi/Flashcards/screens/screens/New_FlashcardCollection.png)

Creation of a new Flashcard

![markdown-preview GitHub style](https://raw.githubusercontent.com/KevDi/Flashcards/screens/screens/New_Flashcard.png)
