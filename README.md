# Kicards
Webbasierte Karteikarten App <br>

Um das kollektive Lernen zu unterstützen, ist diese App nach Anforderungen der Open Education Richtlinien erstellt worden.<br>

ALMS-Framework <br>
* «A» (Access to editing tools), <br>
  * Betriebssystemunabhängigkeit <br>
  * Freiheit  der  Bearbeitungssoftware <br>
* «L» (Level of expertise required to revise or remix), <br>
  * benötigte Expertise zur Software-Nutzung sollte möglichst  gering  sein <br>
* «M» (Meaningfully editable) <br>
	* Editierbarkeit  der erstellten Materialien <br>
* «S» (Source-file access) zur Präzisierung technischer Offenheit vorgestellt. <br>
  * Verfügbarkeit der Quellmaterialien. <br>




## Gewünschte Funktionen

* Import / Export 
* Online-Repository, um Änderungen in Echtzeit zu verfolgen



## Lernfokus 
- Webapp mit Flask
- Sicherheitsaspekte
- Lernmethoden für Karteikarten


## Todos
- Offline-Zugriff

- Gui: Lektion anklicken und danach filtern
  - mehrere Kategorien: select-box

- Order by - Einstellungen bei Fach und Lektion
  - nach Fälligkeit 
  - nach Prio
  - nach Name

- Fehlerquote
  - Anzeige
  - Column: Anzahl der Abfragen
  - Aktualisierung

- Editor 
  - Mathematische Formeln eingeben
  - Editorleiste für einfachere Erstellung von KK

- Votesystem, um schlechte Karten auszusortieren
  - 90% der User dann delete
  - User die das Fach folgen, nicht gesamte User
  - Nur 1x voten

- Import/export
  - eindeutige IDs um Konflikte zu vermeiden

- Fälligkeitstermin 
  - greater than now



## Erledigt
- Wahr/Falsch Button anders platzieren
- Neue Lektion erstellen
- doppelte Lektionen möglich
- direkte Eingabe einer nächsten Karte
- Löschen der Auswahlbox nächste Karte
- Votebuttons
- Fach hinzufügen: Fälligkeit
- Datenbankmodell erweitert
- Fälligkeit und Prio in db eintragen
- Fach hinzufügen: Fälligkeit (optional)
* Seit dem 25th November 2020 ein registrierter Benutzer
  * Datum auf Deutsch ändern

## Fragen
- Quellen zu flask tutorial etc.? 


## Funkionen
- Registrierung eines User Accounts
- Erstellung eigener Themengebiete  
- Erstellung verschiedener Lektionen
- Erstellung von Karteikarten in den Themengebieten
- Abfrage der Karteikarten
- Angabe von Richtig oder Falsch
- Nur die falschen Karteikarten lernen
- Markdown Text für die Erstellung und Bearbeitung


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
... 
