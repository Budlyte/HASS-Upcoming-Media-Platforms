"""
Home Assistant component to feed the Upcoming Media Lovelace card with
Mylar upcoming releases.
https://github.com/Budlyte/HASS-Upcoming-Media-Platforms/tree/Local-Images
https://github.com/custom-cards/upcoming-media-card

"""
import logging
import json
import time
import requests
from datetime import date, datetime
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_API_KEY, CONF_HOST, CONF_PORT, CONF_SSL
from homeassistant.helpers.entity import Entity

__version__ = '0.1.1'

_LOGGER = logging.getLogger(__name__)

CONF_DAYS = 'days'
CONF_URLBASE = 'urlbase'

    
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_KEY): cv.string,
    vol.Optional(CONF_DAYS, default='7'): cv.string,
    vol.Optional(CONF_HOST, default='localhost'): cv.string,
    vol.Optional(CONF_PORT, default=8090): cv.port,
    vol.Optional(CONF_SSL, default=False): cv.boolean,
    vol.Optional(CONF_URLBASE, default=''): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    add_devices([MylarUpcomingMediaSensor(hass, config)], True)


class MylarUpcomingMediaSensor(Entity):

    def __init__(self, hass, conf):
        self.host = conf.get(CONF_HOST)
        self.port = conf.get(CONF_PORT)
        self.urlbase = conf.get(CONF_URLBASE)
        if self.urlbase:
            self.urlbase = "{}/".format(self.urlbase.strip('/'))
        self.apikey = conf.get(CONF_API_KEY)
        self.days = int(conf.get(CONF_DAYS))
        self.ssl = 's' if conf.get(CONF_SSL) else ''
        self._state = None
        self.data = []
        self.comicinfo = []

    @property
    def name(self):
        return 'Mylar_Upcoming_Media'

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        import re
        """Return JSON for the sensor."""
        attributes = {}
        default = {}
        card_json = []
        default['title_default'] = '$title'
        default['line1_default'] = '$episode'
        default['line2_default'] = 'Issue: $number'
        default['line3_default'] = ''
        default['line4_default'] = '$studio'
        default['icon'] = ''
        card_json.append(default)
        for comic in self.data:
            card_item = {}
            
            card_item['airdate'] = comic['IssueDate']
            
            title_string = comic['ComicName']
            if ':' in title_string:
                split_title = [part.strip() for part in title_string.split(':')]

                card_item['title'] = split_title[0]
                card_item['episode'] = split_title[1]
            else:
                card_item['title'] = comic['ComicName']
                card_item['episode'] = ''
            
            if 'IssueNumber' in comic:
                card_item['number'] = comic['IssueNumber']
            else:
                card_item['number'] = ''
            

            card_item['poster'] = ''
            card_item['fanart'] = ''
            
            card_json.append(card_item)
            attributes['data'] = card_json
            return attributes

    def update(self):
        try:
            api = requests.get('http{0}://{1}:{2}/{3}api?cmd=getUpcoming'
                               '&apikey={4}'.format(self.ssl, self.host,
                                                 self.port, self.urlbase,
                                                 self.apikey), timeout=10)
        except OSError:
            _LOGGER.warning("Host %s is not available", self.host)
            self._state = '%s cannot be reached' % self.host
            return

        if api.status_code == 200:
            self._state = 'Online'
            self.data = api.json()
        else:
            self._state = '%s cannot be reached' % self.host
