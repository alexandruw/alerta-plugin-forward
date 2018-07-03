
import json
import logging
import os
import requests
from alerta.plugins import PluginBase
from alertaclient.api import Client

try:
    from alerta.plugins import app  # alerta >= 5.0
except ImportError:
    from alerta.app import app  # alerta < 5.0

LOG = logging.getLogger('alerta.plugins.forward')

SMS_URL = os.environ.get(
    'SMS_URL') or app.config.get('SMS_URL')

class ForwardAlert(PluginBase):
    
    def _sms_prepare_payload(self, alert, status=None, text=None):
        summary = "*[%s] %s %s - _%s on %s_* " % (
            (status if status else alert.status).capitalize(), alert.environment, alert.severity.capitalize(
            ), alert.event, alert.resource)
        )

        payload = {
            "text": summary
        }

        return payload

    def pre_receive(self, alert):
        return alert

    def post_receive(self, alert):
        payload = self._sms_prepare_payload(alert)

        LOG.info('sms payload: %s', payload)

        try:
            r = requests.post(SMS_URL,data=json.dumps(payload), timeout=2)
        except Exception as e:
            raise RuntimeError("sms connection error: %s", e)

        LOG.info('sms response: %s', r.status_code)

    def status_change(self, alert, status, text):
        return
