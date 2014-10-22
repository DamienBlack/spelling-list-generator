Spelling List Generator
=======================

This is a very simple webapp to generate randomly-chosen word lists for spelling
bees. The number of contestants, number of rounds, and number of words can all
be customized. 

Currently the word lists are hard-coded and packaged with the application, in
the [spelling/data](spelling/data) directory.

When you hit the "Generate" button, the word list is randomly generated and
saved to a database table, so if you save the URL you can retrieve it later.

Deployment
----------

This is a standard [Flask](http://flask.pocoo.org/) webapp. To run it in
development mode:

    pip install -r requirements.txt
    python runserver.py

The app fits comfortably within Heroku's free tier, so you can run your own
instance by clicking the button below.

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)
