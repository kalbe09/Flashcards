# Kicards
Webbasierte Karteikarten App <br>

Um das kollektive Lernen zu unterstützen, ist diese Anwendung nach den Software-Anforderung im Sinne von Open Education Richtlinien erstellt worden. Diese wurden im Rahmen eines Selbstversuchs von Dr. Jens Lechtenbörger aufgelistet [Hier gehts zum Paper](http://dx.doi.org/10.21240/mpaed/34/2019.03.02.X).

[Hier gehts zur dazugehörigen Seminararbeit](https://github.com/kalbe09/SeminararbeitOER)

<br>

### <u>**Anforderungen an Software-OER**</u> <br>
![Software-Anforderungen](/img/alms_framework.png)

## Funkionen
- Registrierung eines User Accounts
- Erstellung eigener Themengebiete  
- Erstellung verschiedener Lektionen
- Erstellung von Karteikarten in den Themengebieten
- Abfrage der Karteikarten
- Angabe von Richtig oder Falsch
- Nur die falschen Karteikarten lernen
- Markdown Text für die Erstellung und Bearbeitung

## Datenbankmodell
![Datenbankmodell](/img/Datenbankmodell.png)

<hr>

## Installation
1. **Anforderungen installieren** 
  ```pip install -r requirements/common.txt``` <br>

2. **Datenbank erstellen**
  ```python manage.py db init```
    ```python manage.py db migrate```<br>

3. **Webapplikation / Server starten**
    ```python manage.py runserver```


<br>

  **Tests starten** 
  ```python3 manage.py test```

  **Shell öffnen**
  ```python3 manage.py shell```
<hr>



## Todos
- Datenbank aktualisieren
- Lernen
  - Spaced Learning an Seminararbeit anpassen
  - Frage ob Session wiederholt werden soll
      - temp save in session['temp_learn']

- Import/Export
  - Speicherung im Download-Ordner des Browsers (nicht auf Server)
  - Nutzung der Forms
  - Validate Upload
  - Dropfield

- Delete 
  - Frage ob Fach/Karte wirklich gelöscht werden soll

	- Wenn eine Lernsession begonnen wurde und zurückgeht, dann eine Kategorie auswählt muss man erst die Session beenden
  
	- Images: 
		- Einschränkung auf jpg
		- Speicherung nicht in static
    - Bilder löschen, wenn Karte gelöscht wird

- Offline-Zugriff
  - Online-Repositories
  - Lokale Repositories

- Lektion/en wählen 
  - nach einzelne Lektion filtern
  - mehrere Kategorien: select-box

- Order by 
  - Einstellungen Lektion/Fach
    - nach Fälligkeit 
    - nach Prio

- Editor 
  - Mathematische Formeln eingeben
  - Editorleiste für einfachere Erstellung von KK

- Votesystem, um schlechte Karten auszusortieren
  - 90% der User dann delete
  - User die das Fach folgen, nicht gesamte User
  - Nur 1x voten



## Erledigt
- Lernen
  - Schleife für falsch beantwortete Karten
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
* Import / Export 
  - eindeutige IDs um Konflikte zu vermeiden
      - Erstellung nur auf dem Server möglich, daher immer eine eindeutige ID
- Sicht einzelnes Fach: 
  - Farben reduzieren
  - Falsche lernen rausschmeißen wg. Schleife
- Eingabe 
  - user_id
  - category


<hr>

