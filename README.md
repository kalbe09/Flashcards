# Kicards
Webbasierte Karteikarten App <br>

Um das kollektive Lernen zu unterstützen, ist diese App nach Anforderungen der Open Education Richtlinien erstellt worden.<br>

<br>

### <u>**ALMS-Framework**</u> <br>
* **«A» (Access to editing tools)**, <br>
  * Betriebssystemunabhängigkeit <br>
  * Freiheit  der  Bearbeitungssoftware <br>
* **«L» (Level of expertise required to revise or remix)**, <br>
  * benötigte Expertise zur Software-Nutzung sollte möglichst  gering  sein <br>
* **«M» (Meaningfully editable)** <br>
	* Editierbarkeit  der erstellten Materialien <br>
* **«S» (Source-file access) zur Präzisierung technischer Offenheit vorgestellt.** <br>
  * Verfügbarkeit der Quellmaterialien. <br>



## <u>**Lernfokus</u>**
- Webapp mit Flask
- Sicherheitsaspekte
- Lernmethoden für Karteikarten


<hr>

## Installation
1. **Anforderungen installieren** <br>
  ```pip install -r requirements/common.txt```

2. **Datenbank erstellen**<br>
  ```python3 manage.py db init```<br>
    ```python3 manage.py db migrate```<br>
  ```python3 manage.py db upgrade```

3. **Webapplikation / Server starten** <br>
    ```python3 manage.py runserver```



  **Tests starten** <br>
  ```python3 manage.py test```

  **Shell öffnen** <br>
  ```python3 manage.py shell```
<hr>



## Todos
- Offline-Zugriff
* Import / Export 
* Online-Repository, um Änderungen in Echtzeit zu verfolgen

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

- delete column: timestamp in collection 
- id: timestamp+colname/ts+col+cat/username/ts+user(cards)
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


## Funkionen
- Registrierung eines User Accounts
- Erstellung eigener Themengebiete  
- Erstellung verschiedener Lektionen
- Erstellung von Karteikarten in den Themengebieten
- Abfrage der Karteikarten
- Angabe von Richtig oder Falsch
- Nur die falschen Karteikarten lernen
- Markdown Text für die Erstellung und Bearbeitung

## Fragen
- Quellen zu flask tutorial etc.? 




<hr>

## Datenbankmodell
![Datenbankmodell](/img/Datenbankmodell.png)

## Klassendiagramm
![Klassendiagramm](/img/Klassendiagramm.png)