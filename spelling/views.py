from spelling import app, generator, storage
from flask import render_template, request, redirect, abort, url_for

import sys

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    title = request.form.get('title', 'Spelling List')

    pages = generator.generate(
            contestants = request.form.get('contestants', '0'),
            tiebreakers = request.form.get('tiebreakers', '0'),
            tiebreaker_list = request.form.get('tiebreakerList', ''),
            words_per_round = request.form.get('wordsPerRound', '0'),
            omitted_words = request.form.get('omitted', ''),
            word_lists = request.form.getlist('list'),
            word_counts = request.form.getlist('count'),
            shuffle = request.form.get('shuffle', 'yes')
            )
    
    identifier = storage.save(title, pages)
    return redirect(url_for('view_list', id=identifier))

@app.route('/list/<id>')
def view_list(id):
    word_list = storage.load(id)
    if word_list:
        return render_template('list.html', 
                title=word_list.title, 
                pages=word_list.pages)
    else:
        abort(404)
    

@app.route('/foo')
def foo():
    import os
    return str(sys.path) + " / " + os.getcwd()

