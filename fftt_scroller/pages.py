#-*- coding: utf-8 -*-

def format_get_data(**kwargs):

    final = []

    for key, value in kwargs.items():  
        final.append('{}={}'.format(key, value))


    return '?{}'.format('&'.join(final))
