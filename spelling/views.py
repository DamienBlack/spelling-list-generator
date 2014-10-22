from spelling import app, generator
from flask import render_template, request

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

    return render_template('list.html', title=title, pages=pages)
    

@app.route('/foo')
def foo():
    import os
    return str(sys.path) + " / " + os.getcwd()

