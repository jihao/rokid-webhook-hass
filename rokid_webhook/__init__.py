"""
Rokid (若琪) webhook home assistant component.

For more details about this component, please refer to:
https://github.com/jihao/rokid-webhook-hass 
"""
import requests
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
import logging

_LOGGER = logging.getLogger(__name__)

CONF_WEBHOOK_ID = 'webhook_id'
CONF_ROKID_SN = 'sn'
CONF_ROKID_ROOMNAME = 'roomName'
CONF_ROKID_TAG = 'tag'
CONF_ROKID_ISALL = 'isAll'

VERSION = '0.1.1'
DOMAIN = 'rokid_webhook'
ATTR_MESSAGE = 'message'

SERVICE_SCHEMA = vol.Schema({
    vol.Required(ATTR_MESSAGE): cv.string,
    vol.Optional(CONF_WEBHOOK_ID): cv.string,
    vol.Optional(CONF_ROKID_SN): cv.string,
    vol.Optional(CONF_ROKID_ROOMNAME): cv.string,
    vol.Optional(CONF_ROKID_TAG): cv.string,
    vol.Optional(CONF_ROKID_ISALL, default=False): cv.boolean,
})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_WEBHOOK_ID): cv.string,
        vol.Optional(CONF_ROKID_SN): cv.string,
        vol.Optional(CONF_ROKID_ROOMNAME): cv.string,
        vol.Optional(CONF_ROKID_TAG): cv.string,
        vol.Optional(CONF_ROKID_ISALL, default=False): cv.boolean,
    }),
}, extra=vol.ALLOW_EXTRA)

def setup(hass, config):
    conf = config.get(DOMAIN, {})
    hass.states.set('rokid_webhook.state', 'OK', conf)
    _LOGGER.info("The rokid_webhook component is ready!")

    def send(call, method):
        message = call.data.get(ATTR_MESSAGE) 
        webhook_id      = call.data.get(CONF_WEBHOOK_ID)     or conf.get(CONF_WEBHOOK_ID)
        rokid_sn        = call.data.get(CONF_ROKID_SN)       or conf.get(CONF_ROKID_SN)
        rokid_roomname  = call.data.get(CONF_ROKID_ROOMNAME) or conf.get(CONF_ROKID_ROOMNAME)
        rokid_tag       = call.data.get(CONF_ROKID_TAG)      or  conf.get(CONF_ROKID_TAG)
        rokid_isall     = call.data.get(CONF_ROKID_ISALL)    or conf.get(CONF_ROKID_ISALL) 
        client = rokid_webhook(webhook_id, rokid_sn, rokid_roomname, rokid_tag, rokid_isall)       
        try:
            message = getattr(client, method)(message)
        except Exception as e:
            _LOGGER.error(e)

    def send_tts_text(call):
        send(call, "tts")

    def send_audio_url(call):
        send(call, "audio")

    def send_asr_text(call):
        send(call, "asr")

    hass.services.register(DOMAIN, 'tts', send_tts_text, schema=SERVICE_SCHEMA)
    hass.services.register(DOMAIN, 'audio', send_audio_url, schema=SERVICE_SCHEMA)
    hass.services.register(DOMAIN, 'asr', send_asr_text, schema=SERVICE_SCHEMA)
    return True

class rokid_webhook:

    def __init__(self, webhook_id=None, rokid_sn=None, rokid_roomname=None, rokid_tag=None, rokid_isall=False):     
        self._rokid_sn = rokid_sn
        self._rokid_roomname = rokid_roomname
        self._rokid_tag = rokid_tag
        self._rokid_isall = rokid_isall
        self._headers = {"Content-Type": "application/json; charset=utf-8"}
        self._webhook_url = "https://homebase.rokid.com/trigger/with/{}".format(webhook_id)

    def _send_post(self, ttype, data_string):
        try:
            data = {"type": ttype,"devices": {
                "sn": self._rokid_sn, "roomName": self._rokid_roomname,
                "tag": self._rokid_tag, "isAll": self._rokid_isall },"data": {"text": data_string}}

            if ttype == "audio":
                data["data"].pop("text")
                data["data"]["url"] = data_string
            if self._rokid_sn is None: 
                data["devices"].pop("sn")
            if self._rokid_roomname is None: 
                data["devices"].pop("roomName")
            if self._rokid_tag is None: 
                data["devices"].pop("tag")

            r = requests.post(self._webhook_url, headers=self._headers, json=data)
            if r.status_code == 200:
                return
            else:
                _LOGGER.error('status: {}, content: {}'.format(r.status_code, r.content))
        except Exception as e:
            _LOGGER.error(e)
            return False

    def tts(self, text):
        if text:
            self._send_post("tts", text)
        else:
            _LOGGER.error('Please provide message to speak!')

    def audio(self, url):
        if url:
            self._send_post("audio", url)
        else:
            _LOGGER.error('Please provide audio url to play!')

    def asr(self, text):
        if text:
            self._send_post("asr", text)
        else:
            _LOGGER.error('Please provide message to execute!')