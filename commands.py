#!/usr/bin/env python
# -*- coding: utf-8 -*-

from settings import CURRENT_STATE, MAX_FILE_SIZE, ACCESS_LIST
from fs import *

from utils import check_access_decorator, BotException


def __set_path(user, path):
    path = join_path(CURRENT_STATE[user]['path'], path)
    if not is_subdir(ACCESS_LIST[user], path):
        raise BotException('Access to folder %s denied' % path)
    return path


def __save_history(user, command, arg=''):
    CURRENT_STATE[user]['history'].append(' '.join([command, arg]))


@check_access_decorator
def ls(user, path=''):
    __save_history(user, '/ls', path)
    path = __set_path(user, path)
    response = 'Path: ' + path + '\r\n'
    path_content = get_path_content(join_path(CURRENT_STATE[user]['path'], path))
    owner_size = max(map(lambda i: len(str(i['owner'])), path_content))
    for item in path_content:
        if item['type'] == 'folder':
            item['name'] += '/'
        item['owner'] = item['owner'].ljust(owner_size)
        response += '%(mode)s %(owner)s %(size)s %(modify)s %(name)s\r\n' % item
    return response


@check_access_decorator
def cd(user, path=''):
    __save_history(user, '/cd', path)
    if path == '':
        path = ACCESS_LIST[user]
    path = __set_path(user, path)
    if not check_path(CURRENT_STATE[user]['path']):
        raise BotException('Change path error')
    CURRENT_STATE[user]['path'] = path
    return 'Path: ' + CURRENT_STATE[user]['path']


@check_access_decorator
def cat(user, path=''):
    __save_history(user, '/cat', path)
    path = __set_path(user, path)
    if check_path(CURRENT_STATE[user]['path']):
        try:
            with open(path, 'rb') as f:
                return f.read().decode('utf-8', errors='ignore')
        except IOError:
            raise BotException('Read error')
    else:
        raise BotException('File not found')


@check_access_decorator
def get(user, path=''):
    __save_history(user, '/get', path)
    path = __set_path(user, path)
    if check_path(CURRENT_STATE[user]['path']):
        if get_file_size(path) > MAX_FILE_SIZE:
            raise BotException('File size > 50M')
        try:
            return open(path, 'rb'), get_file_type(path).split('/')[0]
        except IOError:
            raise BotException('Read error')
    else:
        raise BotException('File not found')


@check_access_decorator
def pwd(user):
    __save_history(user, '/pwd')
    return CURRENT_STATE[user]['path']


@check_access_decorator
def history(user):
    h_user = '\r\n'.join(CURRENT_STATE[user]['history'])
    __save_history(user, '/history')
    return h_user


@check_access_decorator
def save(user, tg_file, f_name):
    path = join_path(CURRENT_STATE[user]['path'], f_name)
    __save_history(user, ':UPLOAD_FILE:', path)
    try:
        tg_file.download(path)
    except IOError:
        raise BotException('Save error')
    return 'File %s saved' % path
