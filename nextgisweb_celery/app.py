# BASED ON: https://github.com/sontek/pyramid_celery
# Author: John Anderson
from ConfigParser import ConfigParser

import codecs
from celery import Celery, signals
from nextgisweb import Env
from nextgisweb import setenv
from pyramid.settings import asbool

from .util import SETTINGS_CONF_NAME
from .loaders import INILoader, boolify


def add_preload_arguments(parser):
    parser.add_argument(
        '-i', '--ngw-config', default=None,
        help='NextGIS WEB configuration file'
    )

celery_app = Celery()
celery_app.user_options['preload'].add(add_preload_arguments)


def setup_app(ini_location):
    loader = INILoader(celery_app, ini_file=ini_location)
    celery_config = loader.read_configuration()

    #: TODO: There might be other variables requiring special handling
    boolify(
        celery_config, 'CELERY_ALWAYS_EAGER', 'CELERY_ENABLE_UTC', 'CELERY_RESULT_PERSISTENT'
    )

    if asbool(celery_config.get('USE_CELERYCONFIG', False)):
        config_path = 'celeryconfig'
        celery_app.config_from_object(config_path)
    else:
        # TODO: Couldn't find a way with celery to do this
        hijack_logger = asbool(
            celery_config.get('CELERYD_HIJACK_ROOT_LOGGER', False)
        )
        celery_config['CELERYD_HIJACK_ROOT_LOGGER'] = hijack_logger

        celery_app.config_from_object(celery_config)


def init_ngw(ngw_conf_path):
    cfg = ConfigParser()
    cfg.readfp(codecs.open(ngw_conf_path, 'r', 'utf-8'))

    #TODO: setup logging

    env = Env(cfg=cfg)
    env.initialize()

    setenv(env)

    return env



@signals.user_preload_options.connect
def on_preload_parsed(options, **kwargs):
    ngw_config = options['ngw_config']

    if ngw_config is None:
        print('You must provide --ngw-config argument')
        exit(-1)

    env = init_ngw(ngw_config)
    setup_app(env.celery.settings[SETTINGS_CONF_NAME])
