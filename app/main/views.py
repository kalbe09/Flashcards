from flask import render_template, redirect, url_for, abort, flash, jsonify, make_response, request, current_app, session
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from ..models.users import User
from ..models.category import Category
from ..models.flashcard_collections import Collection
from ..models.flashcard import Flashcard
from ..models.learning import Learning
from ..models.phasen import Phasen
from . import main
from .. import db
from .forms import CollectionForm, FlashcardForm, EditFlashcardForm, FlashcardCategoryForm, ImportForm
from random import choice
import datetime
import random
import csv
import pandas as pd
import os

@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASHCARD_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n' %
                (query.statement, query.parameters, query.duration, query.context))
    return response






# INDEX.HTML ******************** 
@main.route('/')
def index():
    if current_user.is_authenticated:
        # shows collections ordered by priority
        collections = current_user.collections.order_by(Collection.prio.desc()).all()
        flashcards = Flashcard.query.all()

        # if phases are not initiated 
        if Phasen.query.first() == None:
            db.session.add(Phasen(waiting_days=0))
            db.session.add(Phasen(waiting_days=2))
            db.session.add(Phasen(waiting_days=4))
            db.session.add(Phasen(waiting_days=6))
            db.session.add(Phasen(waiting_days=7))
            db.session.add(Phasen(waiting_days=8))
            db.session.add(Phasen(waiting_days=9))
            db.session.commit()
    else:
        collections = []
    return render_template('index.html', collections=collections, flashcards=flashcards)



# USER.HTML ********************  
@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    collections = current_user.collections.order_by(Collection.prio.desc()).all()
    return render_template('user.html', user=user, collections=collections)




# *********************************************************************************************************************
# Add Collections, Categories, Flashcards
# *********************************************************************************************************************

# Collections***********************************************************************************************************
# ADD_Collection.HTML ******************** 
@main.route('/add-collection', methods=['GET', 'POST'])
@login_required
def add_collection():
    form = CollectionForm()
    
    # After pressing the submit button
    if form.validate_on_submit():
        
        # identify the current date
        now = datetime.datetime.now()
        now = datetime.date(now.year, now.month, now.day)

        # Validate entered duedate
        if form.duedate.data != None:
            if form.duedate.data < now:
                flash("Der Fälligkeitstermin liegt in der Vergangenheit")
                return render_template('add_collection.html', form=form)            
            
        # if the category does not exist, save all entered data in a new object category
# ACHTUNG: Schaut für alle Collections
        category = Category.query.filter_by(name=form.category.data).first()
        if category is None:
            category = Category(name=form.category.data, duedate=form.duedate.data)
            
        # Add attributes to the new collection
        collection = Collection(name=form.name.data, duedate=form.duedate.data, prio=form.prio.data)
        collection.categories.append(category)
        collection.user = current_user

        # update database
        db.session.add(collection)
        db.session.commit()

        # Short notice and redirection to home
        flash('Fach hinzugefügt')

        return redirect(url_for('.index'))
    # for the template add_collection.html
    return render_template('add_collection.html', form=form)




# Categories********************************************************************************************
# ADD_CATEGORY.HTML ******************** 
@main.route('/add-category/collection/<int:id>', methods=['GET', 'POST'])
@login_required
def add_category(id):
    form = FlashcardCategoryForm()
    
    # Determine the current collection
    flashcardcollection = Collection.query.get_or_404(id)
    
    # After pressing the button
    if form.validate_on_submit():
        now = datetime.datetime.now()
        now = datetime.date(now.year, now.month, now.day)
        
        # Validate entered duedate
        if form.duedate.data != None:
            if form.duedate.data < now:
                flash("Der Fälligkeitstermin liegt in der Vergangenheit")
                return render_template('add_category.html', form=form, name=flashcardcollection.name)
        
        # create new category and put it in the list of his collection
        category = Category(name=form.name.data, duedate=form.duedate.data, prio=form.prio.data)
        flashcardcollection.categories.append(category)
        
        # update database
        db.session.add(flashcardcollection)
        db.session.commit()
        
        # Short notice and redirection to home
        flash('Lektion hinzugefügt')
        return redirect(url_for('.flashcardcollection', id=flashcardcollection.id))
        # for the template add_category.html
    return render_template('add_category.html', form=form, name=flashcardcollection.name)
        
        
        
       
# Flashcards************************************************************************************************
# ADD_FLASHCARD.HTML ******************** 
@main.route('/add-flashcard/collection/<int:colid>', methods=['GET', 'POST'])
@login_required
def add_flashcard(colid):
    form = FlashcardForm()

    # Determine the current collection and category
    collection = Collection.query.get_or_404(colid)
    category_id = request.args.get('catid')

    
    # If a category was choosen, the flashcard can be saved
    if category_id != None:
        # to save the flashcard also in table category
        category = Collection.query.get_or_404(category_id)

        # After pressing the button
        if form.validate_on_submit():
            # Add attributes to the new collection
            card = Flashcard(
                 question=form.question.data, 
                 answer=form.answer.data,
                 category_id=category_id, 
                 collection_id = collection.id, 
                 phase=1)
            card.user = current_user
            #collection.flashcards.append(card)
            #category.flashcards.append(card)

            # # update database
            db.session.add(collection)
            db.session.commit()
        
        
            # Short notice and redirection to home
            flash('Karteikarte wurde zum Fach {0} hinzugefügt'.format(collection.name))        
            return redirect(url_for('.add_flashcard', colid=collection.id, catid=category_id))
    else:        
        if form.validate_on_submit():
            flash("Du musst eine Kategorie wählen")


    # for the template add_flashcard.html
    return render_template('add_flashcard.html', form=form, name=collection.name, col=collection)

# *********************************************************************************************************************
# Get Category
# *********************************************************************************************************************


# ????? Categories filtered by names ****************************************************************************************
@main.route('/get-category', methods=['GET', 'POST'])
@login_required
def get_category():
    return jsonify({
        'category': [category.name for category in Category.query.order_by(Category.name).all()]
    })



# Flashcards for collection id ***************************************************************************************
@main.route('/flashcardcollection/<int:id>/')
@login_required
def flashcardcollection(id):
    flashcardcollection = Collection.query.get_or_404(id)

    catid = request.args.get('catid')
    if catid != 'Null':
        flashcards = flashcardcollection.flashcards.filter_by(wrong_answered=False, right_answered=False).all()
    elif catid == 'wrong_ones':
        flashcards = flashcardcollection.flashcards.filter_by(wrong_answered=True, right_answered=False).all()
    else:
        abort(404)
    return render_template('single_collection.html', flashcardcollection=flashcardcollection)






# Flashcards for collection colid and category catid **************************************************************
@main.route('/category/<int:catid>')
@login_required
def getcards_catid(catid):
    category = Category.query.get_or_404(catid)
    flashcards = category.flashcards.filter_by(wrong_answered=False, right_answered=False).all()

    #catid = request.args.get('catid')
    if catid != 'Null':
        flashcards = flashcardcollection.flashcards.filter_by(wrong_answered=False, right_answered=False).all()
    elif catid == 'wrong_ones':
        flashcards = flashcardcollection.flashcards.filter_by(wrong_answered=True, right_answered=False).all()
    else:
        abort(404)
    return render_template('single_collection.html', flashcardcollection=flashcardcollection)


# Categories for collection id**********************************************************************************
@main.route('/flashcardcategory/<int:id>')
@login_required
def flashcardcategory(collId, catid):
    flashcardcollection = Collection.query.get_or_404(collId)
    category = flashcardcollection.categories.filter_by(id=catid).first()
    return render_template('flashcardcategory.html', flashcardcollection=flashcardcollection, Category=category)


# Single flashcard for collection id ****************************************************************************************
@main.route('/flashcardcollection/<int:collId>/flashcard/<int:cardId>')
@login_required
def flashcard(collId, cardId):
    flashcardcollection = Collection.query.get_or_404(collId)
    flashcard = flashcardcollection.flashcards.filter_by(id=cardId).first()
    if flashcard is None:
        abort(404)
    return render_template('flashcard.html', flashcardcollection=flashcardcollection, flashcard=flashcard)


# *********************************************************************************************************************
# Delete 
# *********************************************************************************************************************

@main.route('/flashcardcollection/<int:id>/delete')
@login_required
def delete_flashcardcollection(id):
    flashcardcollection = Collection.query.get_or_404(id)
    db.session.delete(flashcardcollection)
    db.session.commit()
    flash('Fach {0} wurde gelöscht'.format(flashcardcollection.name))
    return redirect(request.referrer)

@main.route('/flashcardcollection/<int:collId>/delete-flashcard/<int:cardId>')
@login_required
def delete_card(collId, cardId):
    flashcard = Flashcard.query.get_or_404(cardId)
    db.session.delete(flashcard)
    db.session.commit()
    return redirect(url_for('.flashcardcollection', id=collId))

# *********************************************************************************************************************
# Export & Import
# *********************************************************************************************************************

# Export***************************************************************************************************************
@main.route('/flashcardcollection/<int:colId>/export_collection')
@login_required
def export_collection(colId):
    flashcardcollection = Collection.query.get_or_404(colId)
    flashcards = flashcardcollection.flashcards.all()
    # Export will be saved under the name of collection
    fieldnames = [
        "id", 
        "collection_id", 
        "category_id", 
        "phase", 
        "user_id",
        "question",
        "question_html",
        "answer",
        "answer_html", 
        "right_answered", 
        "wrong_answered", 
        "sum_right_answered", 
        "sum_wrong_answered",
        "sum_answered", 
        "quote",
        "vote_bad", 
        "vote_good",
        "nextdate", 
        "lastdate",
        ]
    file_path = os.path.join(current_app.config['DOWNLOAD_FOLDER'], flashcardcollection.name + '.csv')
    with open(file_path, mode='w') as csvfile:

        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(fieldnames)
        for element in flashcards:
            csv_writer.writerow([
                element.id, 
                element.collection_id,
                element.category_id,
                element.phase,
                element.user_id,
                element.question,
                element.question_html,
                element.answer,
                element.answer_html,
                element.right_answered,
                element.wrong_answered,
                element.sum_right_answered,
                element.sum_wrong_answered,
                element.sum_answered,
                element.quote,
                element.vote_bad,
                element.vote_good,
                element.nextdate,
                element.lastdate,
                ])

    flash("Export erfolgreich")
    return redirect(url_for('main.index'))



# Import***************************************************************************************************************


# Funktionen vereinen
@main.route('/import_collection', methods=['GET', 'POST'])
@login_required
def import_collection():
    #form = ImportForm()
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(current_app.config['DOWNLOAD_FOLDER'], uploaded_file.filename)
            # set the file path
            uploaded_file.save(file_path)
            #flash(file_path)
            csvData = pd.read_csv(file_path, encoding = "ISO-8859-1")
            print(csvData)
            csvData.to_sql("flashcard", con=db.engine, if_exists="append", index=False)


            # save the file



        flash("Import erfolgreich")
        return redirect(url_for('main.index'))
    return render_template('import.html')
    flash("Import erfolgreich")
    return render_template('import.html')


# *********************************************************************************************************************
# Edit 
# *********************************************************************************************************************

@main.route('/flashcardcollection/<int:collId>/flashcard/<int:cardId>/edit', methods=['GET', 'POST'])
@login_required
def edit_flashcard(collId, cardId):
    form = EditFlashcardForm()
    flashcardcollection = Collection.query.get_or_404(collId)
    flashcard = flashcardcollection.flashcards.filter_by(id=cardId).first()
    if flashcard is None:
        abort(404)
    if form.validate_on_submit():
        flashcard.question = form.question.data
        flashcard.answer = form.answer.data
        db.session.add(flashcard)
        db.session.commit()
        flash('Flashcard was updated.')
        return redirect(url_for('.flashcard', collId=collId, cardId=cardId))
    form.question.data = flashcard.question
    form.answer.data = flashcard.answer
    return render_template('edit_flashcard.html', form=form, flashcard=flashcard)

@main.route('/flashcardcollection/<int:collId>/edit', methods=['GET', 'POST'])
@login_required
def edit_course(collId):
    form = EditCourseForm()
    flashcardcollection = Collection.query.get_or_404(collId)


    if form.validate_on_submit():
        flashcardcollection.name = form.name.data
        #flashcardcollection.category = form.category.data
        flashcardcollection.duedate = form.duedate.data
        flashcardcollection.prio = form.prio.data

        db.session.add(flashcardcollection)
        db.session.commit()
        flash('Course was updated.')
        return redirect(url_for('.index'))

    form.name.data = flashcardcollection.name
    #form.category.data = flashcardcollection.category
    form.duedate.data = flashcardcollection.duedate
    form.prio.data = flashcardcollection.prio

    return render_template('edit_course.html', form=form, flashcard=flashcard)

# *********************************************************************************************************************
# Learning 
# *********************************************************************************************************************

@main.route('/flashcardcollection/<int:id>/learn')
@login_required
def learn(id, flashcards=None):
    # Identifies the object flashcardcollection
    flashcardcollection = Collection.query.get_or_404(id)
    # Identifies the object category
    category = Category.query.get_or_404(id)
 
    mode = request.args.get('mode')
    now = datetime.datetime.now()
    # At the beginning of a learning session flashcards == None 
    

    if(mode not in session):
        # Selecting new flashcards
        if mode == 'all':
            flashcards = flashcardcollection.flashcards.filter_by().all()
        elif mode == 'bad_ones':
            flashcards = flashcardcollection.flashcards.order_by(Flashcard.quote.asc()).limit(50).all()
        elif mode == 'today':
            flashcards = flashcardcollection.flashcards.filter_by(nextdate=datetime.datetime.now().date()).all()   
        elif mode == 'session':
            if "cards" in session:
                flashcards = flashcardcollection.flashcards.filter(Flashcard.id.in_(session["cards"])).all()
                if not flashcards:
                    flash('Keine Kicards in dieser Session vorhanden.')
                    return redirect(url_for('.question_learn_again'))
        else:
            abort(404)

        # No flashcards available anymore
        if not flashcards:
            flash('Keine Kicards in dieser Sektion vorhanden.')
            return redirect(url_for('.flashcardcollection', id=id))
        else:
            session[mode + "len"] = len(flashcards)
            session[mode] = []    
            for element in flashcards:
                session[mode].append(element.id)

    progress= round((session[mode + "len"] - len(session[mode])) / session[mode + "len"] * 100, 2)
    flashcard = Flashcard.query.get_or_404(random.choice(session[mode]))
    
    return render_template('learn.html', 
        flashcard=flashcard, 
        flashcards=flashcards, 
        collection=flashcardcollection, 
        category=category,
        progress=progress,
        remain=len(session[mode]),
        sum=session[mode + "len"])



@main.route('/learning_again?')
@login_required
def question_learn_again(collId, cardId):
    if form.validate_on_submit():
        session["cards"] = session["cardstemp"]
        return redirect(url_for('.learn', id=id))
    return render_template('learnagain.html')





@main.route('/flashcardcollection/<int:id>/reset-cards')
@login_required
def reset_cards(id):
    coll = Collection.query.get_or_404(id)
    for card in coll.flashcards.all():
        card.wrong_answered = False
        card.right_answered = False
    db.session.add(coll)
    db.session.commit()
    return redirect(url_for('.flashcardcollection', id=id))



@main.route('/flashcardcollection/<int:collId>/learn/<int:cardId>/wrong')
@login_required
def wrong_answer(collId, cardId):
    flashcard = Flashcard.query.get_or_404(cardId)
    flashcards = request.args.get('flashcards')
    

    flashcard.wrong_answered = True
    flashcard.right_answered = False
    flashcard.sum_wrong_answered += 1
    flashcard.sum_answered +=1
    flashcard.quote = round(flashcard.sum_wrong_answered/flashcard.sum_answered, 3)


# Einstellungsmöglichkeiten, was passiert mit phase wenn falsche Antwort
    flashcard.phase = 1
    waitingdays = Phasen.query.filter_by(id=flashcard.phase).first().waiting_days

    flashcard.lastdate = datetime.datetime.now().date()#strftime("%d.%m.%Y")
    flashcard.nextdate = (datetime.datetime.now() + datetime.timedelta(
        days=waitingdays)).date()
    
    # database update    
    db.session.add(flashcard)
    db.session.commit()
    
    # next card
    return redirect(url_for('.learn', id=collId, flashcards=flashcards, lencards=lencards, mode=request.args.get('mode')))







@main.route('/flashcardcollection/<int:collId>/learn/<int:cardId>/right')
@login_required
def right_answer(collId, cardId):
    # Identifies the object flashcard
    flashcard = Flashcard.query.get_or_404(cardId)
    lencards = request.args.get('lencards')
    # Identifies the actual mode
    mode = request.args.get('mode')
    

    # removes the flashcard out of session 
    session[mode].remove(cardId)
    
    
    # When no cards are in the current session, this session will be delete
    if(session[mode] == []):
        session.pop(mode + "len")
        session.pop(mode)
        flash("Finish")
        return redirect(url_for('.flashcardcollection', id=collId))
    flash(session[mode])


    #flashcards = request.args.get('flashcards')

    # Changes attributes of the flashcard
    flashcard.wrong_answered = False
    flashcard.right_answered = True
    
    flashcard.sum_right_answered += 1
    flashcard.sum_answered +=1
    
    flashcard.quote = round(flashcard.sum_wrong_answered/flashcard.sum_answered, 3)

    waitingdays = Phasen.query.filter_by(id=flashcard.phase).first().waiting_days
    if waitingdays < 7:
        flashcard.phase += 1

    flashcard.lastdate = datetime.datetime.now().date()#.strftime("%d.%m.%Y")
    flashcard.nextdate = (datetime.datetime.now() + datetime.timedelta(
        days=waitingdays)).date()

    # database update
    db.session.add(flashcard)
    db.session.commit()
    
    # next card
    return redirect(url_for('.learn', id=collId, flashcards=request.args.get('flashcards'), lencards=lencards, mode=request.args.get('mode')))



@main.route('/flashcardcollection/<int:collId>/learn/<int:cardId>/add')
@login_required
def add_learningcards(collId, cardId):
    if "cards" not in session:
        session["cards"] = []
        session["cardstemp"] = []
    if cardId not in session["cards"]:
        session["cards"].append(cardId)
        session["cardstemp"].append(cardId)
        flash("Karte für die nächste Session hinzugefügt")
    else:
        flash("Karte schon in Session vorhanden")
    #flash(session["cards"])
    return redirect(url_for('.learn', id=collId, flashcards=request.args.get('flashcards'), mode=request.args.get('mode')))