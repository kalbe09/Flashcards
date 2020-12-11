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
* Import / Export 
  - eindeutige IDs um Konflikte zu vermeiden
  - id: timestamp+colname/ts+col+cat/username/ts+user(cards)
- Schleife für falsch beantwortete Karten
- Sicht einzelnes Fach: 
  - Farben reduzieren
  - Falsche lernen rausschmeißen wg. Schleife

- doppelte Fragen verhindern

- Offline-Zugriff
* Import / Export 

- Offline-Zugriff
  - Online-Repositories
  - Lokale Repositories

- Gui: nach Lektionen filtern
  - mehrere Kategorien: select-box

- Order by - Einstellungen Lektion
  - nach Fälligkeit 
  - nach Prio

- Editor 
  - Mathematische Formeln eingeben
  - Editorleiste für einfachere Erstellung von KK

- Votesystem, um schlechte Karten auszusortieren
  - 90% der User dann delete
  - User die das Fach folgen, nicht gesamte User
  - Nur 1x voten


## Usecases 
- X Karten nehmen und diese lernen
    - Karten nehmen: 
        - während des Lernens
        - aus Übersicht 
    - am Ende: Frage ob diese Karten nochmal wiederholt werden sollen
    - Speicherung der Kombination für später 
    - zurück zum normalen Lernmodus
    - Übersicht + Bearbeiten


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
- Order by - Einstellungen bei Fach
  - nach Prio
- Column: Anzahl der Abfragen
- Fälligkeitstermin 
  - greater than now
- Fehlerquote
  - Anzeige
  - Aktualisierung
- delete column: timestamp in collection 
- phasen-Handling and nextdate
- Lernmode: Heute
- lernen: Anzeige der Kategorie, phase (evtl nicht --> Beeinflussung)


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
