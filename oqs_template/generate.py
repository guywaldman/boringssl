#!/usr/bin/env python3

import copy
import glob
import jinja2
import jinja2.ext
import os
import shutil
import subprocess
import yaml

# For list.append in Jinja templates
Jinja2 = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="."),extensions=['jinja2.ext.do'])

def file_get_contents(filename, encoding=None):
    with open(filename, mode='r', encoding=encoding) as fh:
        return fh.read()

def file_put_contents(filename, s, encoding=None):
    with open(filename, mode='w', encoding=encoding) as fh:
        fh.write(s)

def populate(filename, config, delimiter, overwrite=False):
    fragments = glob.glob(os.path.join('oqs_template', filename, '*.fragment'))
    if overwrite == True:
        source_file = os.path.join('oqs_template', filename, os.path.basename(filename)+ '.base')
        contents = file_get_contents(source_file)
    else:
        contents = file_get_contents(filename)
    for fragment in fragments:
        identifier = os.path.splitext(os.path.basename(fragment))[0]
        identifier_start = '{} OQS_TEMPLATE_FRAGMENT_{}_START'.format(delimiter, identifier.upper())
        identifier_end = '{} OQS_TEMPLATE_FRAGMENT_{}_END'.format(delimiter, identifier.upper())
        preamble = contents[:contents.find(identifier_start)]
        postamble = contents[contents.find(identifier_end):]
        if overwrite == True:
            contents = preamble + Jinja2.get_template(fragment).render({'config': config}) + postamble.replace(identifier_end + '\n', '')
        else:
            contents = preamble + identifier_start + Jinja2.get_template(fragment).render({'config': config}) + postamble
    file_put_contents(filename, contents)

def load_config():
    config = file_get_contents(os.path.join('oqs_template', 'generate.yml'), encoding='utf-8')
    config = yaml.safe_load(config)
    return config

config = load_config()

# kems
populate('include/openssl/ssl.h', config, '/////')
populate('ssl/s3_both.cc', config, '/////')
populate('ssl/ssl_key_share.cc', config, '/////')
populate('ssl/ssl_test.cc', config, '/////')
populate('ssl/t1_lib.cc', config, '/////')
populate('ssl/test/fuzzer.h', config, '/////')
populate('ssl/test/test_config.cc', config, '/////')
populate('crypto/obj/objects.txt', config, '#####')

# tests
populate('oqs_test/test_kems.py', config, '#####')
