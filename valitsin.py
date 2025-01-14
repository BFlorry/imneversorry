from telegram import Update
from telegram.ext import CallbackContext
import random
import re
import datetime
import json
import hashlib

class Valitsin:
    def __init__(self):
        self.commands = {}

    def getCommands(self):
        return self.commands

    def makeDecision(self, update: Update, context: CallbackContext, alternatives):
        now = datetime.datetime.now()
        data = [
            update.message.from_user.id,
            now.day,
            now.month,
            now.year,
            alternatives
        ]
        seed = hashlib.md5(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()
        rigged = random.Random(seed)
        if rigged.randint(0, 49) == 0:
            if (len(alternatives) > 2):
                answers = ['Kaikki :D', 'Ei mitään >:(']
            else:
                answers = ['Molemmat :D', 'Ei kumpaakaan >:(']
            context.bot.sendMessage(chat_id=update.message.chat_id, text=rigged.choice(answers))
        else:
            context.bot.sendMessage(chat_id=update.message.chat_id, text=rigged.choice(alternatives))

    def onkoPakko(self, update: Update, context: CallbackContext, groups):
        now = datetime.datetime.now()
        data = [
            update.message.from_user.id,
            now.day,
            now.month,
            now.year,
            groups.group(1)
        ]
        seed = hashlib.md5(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()
        rigged = random.Random(seed)
        if rigged.randint(0, 1) == 0:
            context.bot.sendMessage(chat_id=update.message.chat_id, text='ei ole pakko {}'.format(groups.group(1)))
        else:
            context.bot.sendMessage(chat_id=update.message.chat_id, text='on pakko {}'.format(groups.group(1)))

    def messageHandler(self, update: Update, context: CallbackContext):
        msg = update.message
        if msg.text is not None:
            vai = msg.text.lower().split(' vai ', 1)
            pakko = re.match(r"^onko pakko ([^?]+)(\??)$", msg.text.lower(), re.IGNORECASE)
            if vai > 1:
                self.makeDecision(update, context, vai)
            elif pakko:
                self.onkoPakko(update, context, pakko)
