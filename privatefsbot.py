#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
from telegram import Updater
from commands import history, cat, cd, get, ls, pwd, save
from settings import ACCESS_LIST, BOT_TOCKEN
from utils import on_error_decorator


@on_error_decorator
def on_ls(bot, update):
    path = update.message.text[3:].strip()
    user = update.message.from_user['username']
    bot.sendMessage(update.message.chat_id, text='<pre>%s</pre>' % ls(user, path), parse_mode='HTML')


@on_error_decorator
def on_start(bot, update):
    if update.message.from_user['username'] not in ACCESS_LIST:
        bot.sendMessage(update.message.chat_id, text='<b>Я не твоя мамочка!</b>', parse_mode='HTML')
    else:
        bot.sendMessage(update.message.chat_id, text=pwd(user))


def on_error(_, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


@on_error_decorator
def on_cd(bot, update):
    path = update.message.text[3:].strip()
    user = update.message.from_user['username']
    bot.sendMessage(update.message.chat_id, text='<pre>%s</pre>' % cd(user, path), parse_mode='HTML')


@on_error_decorator
def on_get(bot, update):
    path = update.message.text[4:].strip()
    user = update.message.from_user['username']
    f, f_type = get(user, path)
    {'video': bot.sendVideo,
     'audio': bot.sendAudio,
     'image': bot.sendPhoto}.get(f_type,
                                 bot.sendDocument(update.message.chat_id,
                                                  f,
                                                  filename=path)
                                 )(update.message.chat_id, f)


@on_error_decorator
def on_pwd(bot, update):
    user = update.message.from_user['username']
    bot.sendMessage(update.message.chat_id, text=pwd(user))


@on_error_decorator
def on_history(bot, update):
    user = update.message.from_user['username']
    bot.sendMessage(update.message.chat_id, text=history(user))


@on_error_decorator
def on_message(bot, update):
    if hasattr(update.message, 'document'):
        bot.sendMessage(update.message.chat_id,
                        text=save(update.message.from_user['username'],
                                  bot.getFile(update.message.document.file_id),
                                  update.message.document.file_name))


@on_error_decorator
def on_cat(bot, update):
    path = update.message.text[4:].strip()
    user = update.message.from_user['username']
    bot.sendMessage(update.message.chat_id, text='<pre>%s</pre>' % cat(user, path), parse_mode='HTML')


def run_bot():
    updater = Updater(BOT_TOCKEN)
    updater.dispatcher.addErrorHandler(on_error)
    updater.dispatcher.addTelegramCommandHandler("start", on_start)
    updater.dispatcher.addTelegramCommandHandler("ls", on_ls)
    updater.dispatcher.addTelegramCommandHandler("cd", on_cd)
    updater.dispatcher.addTelegramCommandHandler("get", on_get)
    updater.dispatcher.addTelegramCommandHandler("cat", on_cat)
    updater.dispatcher.addTelegramCommandHandler("pwd", on_pwd)
    updater.dispatcher.addTelegramCommandHandler("history", on_history)
    updater.dispatcher.addTelegramMessageHandler(on_message)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    run_bot()
