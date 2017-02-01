# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from nextgisweb.component import Component, require

from nextgisweb_celery.app import setup_app
from .model import Base
from .util import COMP_ID, SETTINGS_CONF_NAME


class CeleryComponent(Component):
    identity = COMP_ID
    metadata = Base.metadata

    def initialize(self):
        pass

    @require('resource')
    def setup_pyramid(self, config):
        from . import view, api
        view.setup_pyramid(self, config)
        api.setup_pyramid(self, config)

        # init celery
        celery_config_path = self.settings.get(SETTINGS_CONF_NAME)
        setup_app(celery_config_path)


    settings_info = (
        dict(key='celery_conf_file', desc=u"Путь до файла конфигурации celery"),
    )


def pkginfo():
    return dict(
        components=dict(celery='nextgisweb_celery')
    )
