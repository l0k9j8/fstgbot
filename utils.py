#!/usr/bin/env python
# -*- coding: utf-8 -*-

from settings import ACCESS_LIST, CURRENT_STATE


class BotException(Exception):
    pass


def check_access_decorator(func):
    def check_access_func(*args, **kwargs):
        user = args[0]
        if user not in ACCESS_LIST:
            raise BotException('Я не твоя мамочка!')
        if user not in CURRENT_STATE:
            CURRENT_STATE[user] = {'path': ACCESS_LIST[user], 'history': []}
        return func(*args, **kwargs)

    return check_access_func


def on_error_decorator(func):
    def on_error_func(*args, **kwargs):
        bot = args[0]
        update = args[1]
        try:
            return func(*args, **kwargs)
        except BotException as exc:
            bot.sendMessage(update.message.chat_id, text='<b>%s</b>' % repr(exc), parse_mode='HTML')

    return on_error_func
