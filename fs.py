#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from stat import *
from datetime import datetime
import magic
import pwd
import grp


def human_size(num):
    for unit in ['B', 'K', 'M', 'G', 'T']:
        if abs(num) < 1024.0:
            if len(str(num).split('.')[0]) > 1 or unit == 'B':
                return "%3d%s" % (num, unit)
            else:
                return "%3.1f%s" % (num, unit)

        num /= 1024.0
    return "%.1f%s" % (num, 'P')


def get_path_content(path):
    list_dir = os.listdir(path)
    return [stat_to_dict(path, item, os.stat(os.path.join(path, item))) for item in list_dir]


def get_file_size(path):
    return os.path.getsize(path)


def join_path(root, path):
    if len(path) > 0 and path[0] == '/':
        return os.path.normpath(path)
    else:
        return os.path.normpath(os.path.join(root, path))


def check_path(path):
    return os.path.exists(path) and os.access(path, os.R_OK)


def get_file_type(path):
    return magic.from_file(path, mime=True).decode("utf-8")


def stat_to_dict(path, name, file_stat):
    result = {'name': name}
    if S_ISDIR(file_stat.st_mode):
        result['type'] = 'folder'
    elif S_ISREG(file_stat.st_mode):
        result['type'] = get_file_type(os.path.join(path, name))
    else:
        result['type'] = ''
    result['mode'] = filemode(file_stat.st_mode)
    result['size'] = human_size(file_stat.st_size)
    result['modify'] = datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M')
    result['create'] = datetime.fromtimestamp(file_stat.st_ctime).strftime('%Y-%m-%d %H:%M')
    result['owner'] = ':'.join([pwd.getpwuid(file_stat.st_uid).pw_name, grp.getgrgid(file_stat.st_gid).gr_name])
    return result


def is_subdir(root, path):
    root, path = os.path.normpath(root), os.path.normpath(path)
    return path.find(root) == 0
