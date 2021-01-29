from flask import render_template, redirect, url_for, abort, flash, jsonify, make_response, request, current_app, session
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from ..models.users import User
from ..models.category import Category
from ..models.flashcard_collections import Collection
from ..models.flashcard import Flashcard
from ..models.phasen import Phasen
from . import main
from .. import db
from .forms import CollectionForm, FlashcardForm, EditFlashcardForm, FlashcardCategoryForm, ImportForm, EditCourseForm, EditCategoryForm
from random import choice
import pandas as pd
import datetime
import random
import csv
import os
from PIL import Image



# Handling slow query time
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
        #flashcards = Flashcard.query.all()

        # if phases are not initiated 
        if Phasen.query.first() == None:
            db.session.add(Phasen(waiting_days=0))
            db.session.add(Phasen(waiting_days=1))
            db.session.add(Phasen(waiting_days=2))
            db.session.add(Phasen(waiting_days=8))
            db.session.add(Phasen(waiting_days=32))
            db.session.add(Phasen(waiting_days=64))
            db.session.add(Phasen(waiting_days=128))
            db.session.commit()
    
    else:
        collections = []
    
    return render_template('index.html', collections=collections)#, flashcards=flashcards)



# USER.HTML ********************  
@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    
    if user is None:
        abort(404)
    
    # Identifies all Collections for the user
    collections = current_user.collections.order_by(Collection.prio.desc()).all()

    return render_template('user.html', user=user, collections=collections)



# *********************************************************************************************************************
# *********************************************************************************************************************
# Adding Collections, Categories, Flashcards
# *********************************************************************************************************************
# *********************************************************************************************************************

# ADD_Collection.HTML ************************************************************************************************* 
@main.route('/add-collection', methods=['GET', 'POST'])
@login_required
def add_collection():
    # Shows the formular specified in main.forms
    form = CollectionForm()
    
    # POST: After pressing the submit button
    if form.validate_on_submit():
        
        # Identify the current date in yyyy.mm.dd
        date = datetime.datetime.now()
        formatted_date = datetime.date(date.year, date.month, date.day)

        # Validate duedate
        if form.duedate.data != None:
            if form.duedate.data < formatted_date:
                flash("Der Fälligkeitstermin liegt in der Vergangenheit")
                return render_template('add_collection.html', form=form)            
                    
            
        # Add attributes to the new collection
        collection = Collection(name=form.name.data, duedate=form.duedate.data, prio=form.prio.data)
        
        # Create and add Category
        category = Category(name=form.category.data, duedate=form.duedate.data)
        collection.categories.append(category)
        
        # Add user
        collection.user = current_user

        # update database
        db.session.add(collection)
        db.session.commit()

        # Short notice and redirection to home
        flash('Fach hinzugefügt')

        return redirect(url_for('.index'))

    return render_template('add_collection.html', form=form)





# ADD_CATEGORY.HTML ***************************************************************************** 
@main.route('/add-category/collection/<int:id>', methods=['GET', 'POST'])
@login_required
def add_category(id):
    # Shows the formular specified in main.forms
    form = FlashcardCategoryForm()
    
    # Select the collection
    flashcardcollection = Collection.query.get_or_404(id)
    
    # Post: Pressing button
    if form.validate_on_submit():

        date = datetime.datetime.now()
        formatted_date = datetime.date(date.year, date.month, date.day)
        
        # Validate entered duedate
        if form.duedate.data != None:
            if form.duedate.data < formatted_date:
                flash("Der Fälligkeitstermin liegt in der Vergangenheit")
                return render_template('add_category.html', form=form, name=flashcardcollection.name)
        
        # New category 
        category = Category(name=form.name.data, duedate=form.duedate.data, prio=form.prio.data)
        
        # Add to collection
        flashcardcollection.categories.append(category)
        
        # Update database
        db.session.add(flashcardcollection)
        db.session.commit()
        
        flash('Lektion hinzugefügt')
        
        return redirect(url_for('.flashcardcollection', id=flashcardcollection.id))
        
    return render_template('add_category.html', form=form, name=flashcardcollection.name)
        
        
        
       
# ADD_FLASHCARD.HTML ******************** 
@main.route('/add-flashcard/collection/<int:colid>', methods=['GET', 'POST'])
@login_required
def add_flashcard(colid):
    # Shows the formular specified in main.forms
    form = FlashcardForm()

    # Determine the current collection and category_id
    collection = Collection.query.get_or_404(colid)
    catid = request.args.get('catid')

    
    # If category was choosen, the flashcard can be saved
    if catid:
        category = Category.query.get_or_404(catid)

        # After pressing the button
        if form.validate_on_submit():
            
            # Add attributes to the new collection
            card = Flashcard(
                 question=form.question.data, 
                 answer=form.answer.data,
                 category_id=catid, 
                 collection_id = collection.id, 
                 phase=1)
             
            card.user = current_user

            # # update database
            db.session.add(collection)
            db.session.commit()
        
            # Image saving
            # Extract the file extension
            filename, file_extension = os.path.splitext(form.photo.data.filename)

# url_for
            form.photo.data.save("app/static/flashcard_img/" + str(card.id) + file_extension)
            
            flash('Karteikarte wurde zum Fach {0} hinzugefügt'.format(collection.name))        
            return redirect(url_for('.add_flashcard', colid=collection.id, catid=catid))
    
    # If Category was not choosen
    else: 
        category = None      
        if form.validate_on_submit():
            flash("Du musst eine Kategorie wählen")


    return render_template('add_flashcard.html', form=form, name=collection.name, collection=collection, category=category)






# *********************************************************************************************************************
# Get 
# *********************************************************************************************************************

# single_collection.html ****************************************************************************************************
# Cards for collection and/or category***************************************************************************************
@main.route('/flashcardcollection/<int:id>/')
@login_required
def flashcardcollection(id):
    flashcardcollection = Collection.query.get_or_404(id)
    catid = request.args.get('catid')
    
    # cards for a category
    if(catid):
        category = Category.query.get_or_404(catid)
        flashcards = flashcardcollection.flashcards.filter_by(category_id=catid).all()
        
        return render_template('single_collection.html', flashcardcollection=flashcardcollection, cards=flashcards, category=category)
    
    # all cards in collection
    else:
        flashcards = flashcardcollection.flashcards.all()    
        
        return render_template('single_collection.html', flashcardcollection=flashcardcollection, cards=flashcards)



# flashcardcategory.html ***************************************************************************************
# Categories for collection id**********************************************************************************
@main.route('/flashcardcategory/<int:id>')
@login_required
def flashcardcategory(collId, catid):
    flashcardcollection = Collection.query.get_or_404(collId)
    category = flashcardcollection.categories.filter_by(id=catid).first()

    return render_template('flashcardcategory.html', flashcardcollection=flashcardcollection, Category=category)




# flashcard.html ***************************************************************************************
# Cards  ***********************************************************************************************
@main.route('/flashcardcollection/<int:collId>/flashcard/<int:cardId>')
@login_required
def flashcard(collId, cardId):

    # Collect cards for collection and category
    flashcardcollection = Collection.query.get_or_404(collId)
    flashcard = flashcardcollection.flashcards.filter_by(id=cardId).first()

    if flashcard is None:
        abort(404)

    # Load image
    if os.path.exists("app/static/flashcard_img/" +str(cardId) + ".jpg"):
        
        img = Image.open("app/static/flashcard_img/" +str(cardId) + ".jpg")
        img_name = str(cardId) + ".jpg"
        
        return render_template('flashcard.html', flashcardcollection=flashcardcollection, flashcard=flashcard, img=img, img_name=img_name)
    
    # Without image
    else:
        return render_template('flashcard.html', flashcardcollection=flashcardcollection, flashcard=flashcard)


# *********************************************************************************************************************
# Delete 
# *********************************************************************************************************************

# Delete User ********************************************************************************************************
@main.route('/user/<int:id>/delete')
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    
    db.session.delete(user)
    db.session.commit()
    flash('User {0} wurde gelöscht'.format(user.username))
    
    return redirect(url_for('auth.logout'))




# Delete Collection ********************************************************************************************************
@main.route('/flashcardcollection/<int:id>/delete')
@login_required
def delete_flashcardcollection(id):

    # Select collecttion and all flashcards
    flashcardcollection = Collection.query.get_or_404(id)
    flashcards = flashcardcollection.flashcards.all()
    categories = flashcardcollection.categories.all()

    # Delete cards
    for element in flashcards:
        db.session.delete(Flashcard.query.get_or_404(element.id))
    
    # Delete Categories
    for element in categories:
        db.session.delete(Category.query.get_or_404(element.id))

    # Delete Collection
    db.session.delete(flashcardcollection)
    
    db.session.commit()
    
    flash('Fach {0} wurde gelöscht'.format(flashcardcollection.name))
    
    return redirect(request.referrer)






# Delete Category ********************************************************************************************************
@main.route('/flashcardcollection/<int:collId>/category/<int:catid>/delete')
@login_required
def delete_category(collId, catid):
    flashcardcollection = Collection.query.get_or_404(collId)
    category = Category.query.get_or_404(catid)
    flashcards = flashcardcollection.flashcards.filter_by(category_id=catid).all()

    # Delete cards
    for element in flashcards:
        db.session.delete(Flashcard.query.get_or_404(element.id))
    
    # Delete category
    db.session.delete(category)
    
    db.session.commit()
    flash('Category {0} wurde gelöscht'.format(category.name))
    
    return redirect(url_for('.flashcardcollection', id=collId))





# Delete Card ********************************************************************************************************
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

    # Export will be saved under the name of the collection
    columns = [m.key for m in Flashcard.__table__.columns]
    
    # Exclude the first id's
    del columns[:1]
    
    # Select the download-path
    file_path = os.path.join(current_app.config['DOWNLOAD_FOLDER'], flashcardcollection.name + '.csv')
    
    with open(file_path, mode='w') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # Writes the fieldnames first
        csv_writer.writerow(columns)
        
        for element in flashcards:
            csv_writer.writerow([
                #element.id, 
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
                element.nextdateLeitner,
                element.nextdateSpaced,
                element.lastdate,
                ])

    flash("Erfolgreich! Speicherung unter: " + current_app.config['DOWNLOAD_FOLDER'])
    return redirect(url_for('main.index'))



# Import***************************************************************************************************************


# Funktionen vereinen
@main.route('/import_collection', methods=['GET', 'POST'])
@login_required
def import_collection():
    #form = ImportForm()
    
    if request.method == 'POST':
        
        # Select the inserted file
        uploaded_file = request.files['file']
    
        # if uploaded_file
        if uploaded_file: #.filename != '':

            # Save Collection 

            # Save Category
            
            # Save flashcard            
            csvData = pd.read_csv(uploaded_file, encoding = "UTF-8") # ISO-8859-1        
            csvData.to_sql("flashcard", con=db.engine, if_exists="append", index=False)

            flash("Import erfolgreich")
            return redirect(url_for('main.index'))
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


@main.route('/flashcardcollection/<int:collId>/category/<int:catid>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(collId, catid):
    form = EditCategoryForm()
    category = Category.query.get_or_404(catid)
    #flashcardcollection = Collection.query.get_or_404(collId)


    if form.validate_on_submit():
        category.name = form.name.data
        #flashcardcollection.category = form.category.data
        category.duedate = form.duedate.data
        category.prio = form.prio.data

        db.session.add(category)
        db.session.commit()
        flash('Category was updated.')
        return redirect(url_for('.flashcardcollection', id=collId))
        

    form.name.data = category.name
    #form.category.data = flashcardcollection.category
    form.duedate.data = category.duedate
    form.prio.data = category.prio

    return render_template('edit_category.html', form=form)



















# *********************************************************************************************************************
# Learning 
# *********************************************************************************************************************

@main.route('/flashcardcollection/<int:id>/learn')
@login_required
def learn(id, flashcards=None):
    flashcardcollection = Collection.query.get_or_404(id)
    category = Category.query.get_or_404(id)
    catid = request.args.get('catid')
    mode = request.args.get('mode')
    now = datetime.datetime.now()
    #session.pop(mode)
    


    # ****************************************************
    # Break handeling for spaced-method
    if mode == 'spaced' and "break" in session:
        if session["break"] > now:
            flash("Die Pause ist noch nicht vorbei: %s:%s:%s" % (session["break"].hour, session["break"].minute, session["break"].second))
            #return redirect(url_for('.index'))
            return redirect(url_for('.flashcardcollection', id=id))



    # ****************************************************
    # Get new flashcards 
    if(mode not in session):
        # Selecting new flashcards
        if mode == 'all':
            if catid:
                flashcards = flashcardcollection.flashcards.filter_by(category_id=catid).all()
            else: 
                flashcards = flashcardcollection.flashcards.filter_by().all()
        
        elif mode == 'bad_ones':
            if catid:
                flashcards = flashcardcollection.flashcards.filter_by(category_id=catid).order_by(Flashcard.quote.asc()).limit(50).all()
            else:
                flashcards = flashcardcollection.flashcards.order_by(Flashcard.quote.asc()).limit(10).all()

        elif mode == 'leitner':
            if catid:
                temp_flashcards = flashcardcollection.flashcards.filter_by(category_id=catid).all() 
                flashcards = temp_flashcards.filter(Flashcard.nextdateLeitner <= datetime.datetime.now())  
            else:
                flashcards  = flashcardcollection.flashcards.filter(Flashcard.nextdateLeitner <= datetime.datetime.now())
        
        elif mode == 'spaced':
            session[mode + "begin"] = now
            flash(session[mode + "begin"])
            if catid:
                temp_flashcards = flashcardcollection.flashcards.filter_by(category_id=catid).all() 
                flashcards = temp_flashcards.filter(Flashcard.nextdateSpaced <= datetime.datetime.now())
                
            else:
                flashcards  = flashcardcollection.flashcards.filter(Flashcard.nextdateSpaced <= datetime.datetime.now())

        elif mode == 'session':
            session['onetimefalse'] = False
            if "cards" in session:
                flashcards = flashcardcollection.flashcards.filter(Flashcard.id.in_(session["cards"])).all()
                #if not flashcards:
                    #flash('Keine Kicards in dieser Session vorhanden.')
                    # return to diffent page
                    #return redirect(url_for('.flashcardcollection', id=id))
                    #return redirect(url_for('.question_learn_again'))
            elif flashcards == None:
                flash('Keine Kicards in dieser Session vorhanden.')
                return redirect(url_for('.flashcardcollection', id=id))

        session[mode] = []
        for element in flashcards:
            session[mode].append(element.id)

        session[mode + "len"] = len(session[mode])


    # ****************************************************************************
    # No cards available
    if session[mode] == [] :
        session.pop(mode + "len")
        session.pop(mode)
        flash('Keine Kicards in dieser Sektion vorhanden.')
        return redirect(url_for('.flashcardcollection', id=id))


    # ****************************************************************************
    # Progessbar
    progress= round((session[mode + "len"] - len(session[mode])) / session[mode + "len"] * 100, 2)

    # ****************************************************************************
    # Choice of the flashcard
    flashcard = Flashcard.query.get_or_404(random.choice(session[mode]))




    # Check if a image exist and handle returns
    if os.path.exists("app/static/flashcard_img/" +str(flashcard.id) + ".jpg"):
        img = Image.open("app/static/flashcard_img/" +str(flashcard.id) + ".jpg")
        img_name = str(flashcard.id) + ".jpg"
        
        return render_template('learn.html', 
            flashcard=flashcard, 
            flashcards=flashcards, 
            collection=flashcardcollection, 
            category=category,
            mode=mode,
            progress=progress,
            remain=len(session[mode]),
            sum=session[mode + "len"],
            # with image
            img=img, img_name=img_name)
    else:

        return render_template('learn.html', 
            flashcard=flashcard, 
            flashcards=flashcards, 
            collection=flashcardcollection, 
            category=category,
            mode=mode,
            progress=progress,
            remain=len(session[mode]),
            sum=session[mode + "len"])




# Wrong / Right Buttons***********************************************************************************************
@main.route('/flashcardcollection/<int:collId>/learn/<int:cardId>/right')
@login_required
def answer(collId, cardId):
    flashcard = Flashcard.query.get_or_404(cardId)
    lencards = request.args.get('lencards')
    mode = request.args.get('mode')
    answer = request.args.get('answer')

    if answer =='right':
        flashcard.sum_right_answered += 1
        session[mode].remove(cardId)
    elif answer =='wrong':
        flashcard.sum_wrong_answered += 1
        if mode == 'session':
            session['onetimefalse'] = True


    flashcard.sum_answered +=1
    flashcard.quote = round(flashcard.sum_wrong_answered/flashcard.sum_answered, 3)

    # **** Leitner

    if mode == 'leitner':
        if answer =='right':
            if flashcard.phase < 7:
                flashcard.phase += 1
                waitingdays = Phasen.query.filter_by(id=flashcard.phase).first().waiting_days
            else:
                waitingdays = 365
            
        if answer == 'false':
            flashcard.phase = 1
            waitingdays = Phasen.query.filter_by(id=flashcard.phase).first().waiting_days

        flashcard.nextdateLeitner = (datetime.datetime.now() + datetime.timedelta(days=waitingdays)).date()
    flashcard.lastdate = datetime.datetime.now().date()

    if mode == 'session' and 'onetimefalse' in session and session['onetimefalse'] == True:
        return redirect(url_for('.learn', id=collId, flashcards=request.args.get('flashcards'), lencards=lencards, mode=request.args.get('mode')))


    # database update
    db.session.add(flashcard)
    db.session.commit()
    
    # When no cards are in the current session, this session will be delete
    if(session[mode] == []):
        if mode == 'session':
            session['onetimefalse'] = False
            session.pop('cards')
        session.pop(mode)
        return redirect(url_for('.flashcardcollection', id=collId))
    flash(session[mode])

    # next card
    return redirect(url_for('.learn', id=collId, flashcards=request.args.get('flashcards'), lencards=lencards, mode=request.args.get('mode')))


@main.route('/flashcardcollection/<int:id>/learn/spaced')
@login_required
def spaced(id, flashcards=None):
    flashcardcollection = Collection.query.get_or_404(id)
    category = Category.query.get_or_404(id)
    catid = request.args.get('catid')
    mode = request.args.get('mode')
    flashcards = session[mode]
    
    now = datetime.datetime.now()
    breaktime = current_user.spaced_duration
    session_duration = current_user.spaced_duration

    finish_break = session[mode + "begin"] + datetime.timedelta(minutes=session_duration)
    flash(now - finish_break)

    progress= round((session[mode + "len"] - len(session[mode])) / session[mode + "len"] * 100, 2)

    # Choice of the flashcard
    flashcard = Flashcard.query.get_or_404(random.choice(session[mode]))

    # Check if breaktime is passed
    if finish_break < now :
        session.pop(mode)
        session.pop(mode + "len")
        session["break"] = datetime.datetime.now() + datetime.timedelta(minutes=breaktime)
        flash(str(breaktime) + " Minuten Pause")
        return redirect(url_for('.flashcardcollection', id=id))

    #zeroSecondDate = finish_break.AddSeconds(-finish_break.Second);    
    #flash(zeroSecondDate)

    # Check if a image exist and handle returns
    if os.path.exists("app/static/flashcard_img/" +str(flashcard.id) + ".jpg"):
        img = Image.open("app/static/flashcard_img/" +str(flashcard.id) + ".jpg")
        img_name = str(flashcard.id) + ".jpg"
        
        return render_template('learn.html', 
            flashcard=flashcard, 
            flashcards=flashcards, 
            collection=flashcardcollection, 
            category=category,
            mode=mode,
            progress=progress,
            remain=len(session[mode]),
            sum=session[mode + "len"],
            # with image
            img=img, img_name=img_name,
            finish_break = finish_break.time())
    else:

        return render_template('learn.html', 
            flashcard=flashcard, 
            flashcards=flashcards, 
            collection=flashcardcollection, 
            category=category,
            mode=mode,
            progress=progress,
            remain=len(session[mode]),
            sum=session[mode + "len"], 
            finish_break = finish_break.time())





@main.route('/flashcardcollection/<int:collId>/learn/<int:cardId>/hard')
@login_required
def spacedanswer(collId, cardId):
    flashcard = Flashcard.query.get_or_404(cardId)
    mode = request.args.get('mode')
    #flashcards = session[mode] 
    lencards = request.args.get('lencards')
    answer =request.args.get('answer')

    flash(session[mode] )
    if answer == 'again':
        flashcard.sum_wrong_answered += 1
        flashcard.nextdateSpaced = (datetime.datetime.now() + datetime.timedelta(seconds=0))
    elif answer == 'hard':
        flashcard.sum_wrong_answered += 1
        flashcard.nextdateSpaced = (datetime.datetime.now() + datetime.timedelta(minutes=10))
    elif answer == 'middle':
        flashcard.nextdateSpaced = (datetime.datetime.now() + datetime.timedelta(minutes=60))
    elif answer == 'easy':
        session[mode].remove(cardId)
        flashcard.sum_right_answered += 1
        flashcard.nextdateSpaced = (datetime.datetime.now() + datetime.timedelta(days=6))
    elif answer == 'veryeasy':
        session[mode].remove(cardId)
        flashcard.sum_right_answered += 1
        flashcard.nextdateSpaced = (datetime.datetime.now() + datetime.timedelta(days=30))

    flashcard.sum_answered +=1
    flashcard.quote = round(flashcard.sum_wrong_answered/flashcard.sum_answered, 3)

    flashcard.lastdate = datetime.datetime.now().date()

    # Einstellungsmöglichkeiten, was passiert mit phase wenn falsche Antwort

    # database update    
    db.session.add(flashcard)
    db.session.commit()
    if session[mode]  == []: 
        session.pop(request.args.get('mode'))
        return redirect(url_for('.flashcardcollection', id=collId))
    # next card
    return redirect(url_for('.spaced', id=collId, flashcards=session[mode], lencards=lencards, mode=request.args.get('mode')))





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




# *********************************************************************************************************************
# Statistics 
# *********************************************************************************************************************

@main.route('/flashcardcollection/<int:collId>/stats/')
@login_required
def stats(collId):
    flashcardcollection = Collection.query.get_or_404(collId)
    
    # Flashcards in each phases
    cards_in_phases =	{
        "phase1": flashcardcollection.flashcards.filter_by(phase=1).all(),
        "phase2": flashcardcollection.flashcards.filter_by(phase=2).all(),
        "phase3": flashcardcollection.flashcards.filter_by(phase=3).all(),
        "phase4": flashcardcollection.flashcards.filter_by(phase=4).all(),
        "phase5": flashcardcollection.flashcards.filter_by(phase=5).all(),
        "phase6": flashcardcollection.flashcards.filter_by(phase=6).all(),
        "phase7": flashcardcollection.flashcards.filter_by(phase=7).all()
    }



    return render_template('statistic.html', 
        flashcardcollection=flashcardcollection, 
        cards_in_phases=cards_in_phases)














