# groupme-sentence-maker

Predictive Text bot for GroupMe!

This bot is designed to run constantly on a server to read and write messages on GroupMe

Follow this tutorial to get your access token.
https://dev.groupme.com/tutorials/bots

Put your access token in the TOKEN variable on line 8

This code runs predictive text through all bots linked to your account

To trigger it, type "predictive text" into the chat to see what you would say.
Type "predictive text" and tag someone to run a prediction on what they would say.
Type "Predictive Text", capitalized, to run a prediction based on everyone in the chat.

This bot requires external modules. On the command line, run the command:
pip install GroupyAPI
to install the necessary module.

In addition, this bot is designed to work with Heroku.
Create a new private repo with your access code set up.
Link that to a new application on Heroku
Turn on the new "worker" dyno once the app deploys to Heroku
This makes the bot run even when your computer is not running it