#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardHide)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
from globals import *

import logging,json, urllib2

gameList = []

def search_game_on_api(query):
    cont = 1
    output = ""
    del gameList [:]
	
    archivoDescargar = "http://www.giantbomb.com/api/search/?api_key=" + GIANTBOMBKEY + "&format=json&query=%22"+ query.replace(" ","%20") +"%22&resources=game&limit=50"

    descarga = urllib2.urlopen(archivoDescargar)
    response_json = descarga.read()
    info = json.loads(response_json)

    for r in info['results']:
        output = output + str(cont) + ": " + r['name'] + "\n"
        temp = []
        temp.append(r['name'])
        gameList.append(temp)
        cont = cont + 1

    return output

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

CREATEGAMEREPLY, SELECTGAME = range(2)

def searchGame(bot, update):
    update.message.reply_text(text = 'Which game do you want to add to your Wishlist ? ', reply_markup=ReplyKeyboardHide())
    return CREATEGAMEREPLY

def createGameReply(bot, update):
    final_list = []
    logger.info('GAME Function '+ update.message.text)
    output_text = "Select a Game please from this list \n" + search_game_on_api(update.message.text)

    final_list = gameList
    reply_markup = ReplyKeyboardMarkup(final_list)

    logger.info('' + str(len(final_list)))

    update.message.reply_text(text = output_text, reply_markup=reply_markup)
    return SELECTGAME

def selectGame(bot, update):
    selectedGame = update.message.text
    logger.info("Selected Game: " + selectedGame)
    update.message.reply_text(selectedGame + ' added to Wishlist :) ', reply_markup=ReplyKeyboardHide())
    return ConversationHandler.END

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',reply_markup=ReplyKeyboardHide())

    return ConversationHandler.END

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TELEGRAMTOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('searchgame', searchGame)],

        states={
            CREATEGAMEREPLY: [MessageHandler(Filters.text, createGameReply)],
            SELECTGAME: [MessageHandler(Filters.text, selectGame)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()