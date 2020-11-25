# Kicards
Webbasierte Karteikarten App <br>

Um das kollektive Lernen zu unterstützen, ist diese App nach Anforderungen der Open Education Richtlinien erstellt worden.<br>
ALMS-Framework <br>
  * «A» (Access to editing tools), <br>
  (a) Betriebssystemunabhängigkeit <br>
			(b) Freiheit  der  Bearbeitungssoftware <br>
	• «L» (Level of expertise required to revise or remix), <br>
		○ benötigte Expertise zur Software-Nutzung <br>
			(a) sollte möglichst  gering  sein <br>
	• «M» (Meaningfully editable) <br>
		  (a) Editierbarkeit  der erstellten Materialien <br>
	• «S» (Source-file access) zur Präzisierung technischer Offenheit vorgestellt. <br>
      (a) Verfügbarkeit der Quellmaterialien. <br>


## Gewünschte Funktionen



## Features
You can 
* Register an User Account
* Each User could create their own Flashcard Collections
* Create Flashcards in that Collections
* Learn the Collection
* Mark the Flashcard as Wrong or Right answered
* Only learn the Wrong Answered Flashcards
* Question and Answer of the Flashcards allow Markdown Text


## Installation
1. Install the Requirements

```pip3 install -r requriements/common.txt```

2. Setup the Database

```
python3 manage.py db init

python3 manage.py db migrate

python3 manage.py db upgrade
```

3. Run the Application

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
