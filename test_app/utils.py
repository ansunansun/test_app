__author__ = 'ansun'

import hmac
import time
import json
import base64
import hashlib

from social.utils import constant_time_compare
from test_app.settings import SOCIAL_AUTH_FACEBOOK_SECRET


def load_signed_request(signed_request):
    """ Copied from social.backend.facebook """
    def base64_url_decode(data):
        data = data.encode('ascii')
        data += '=' * (4 - (len(data) % 4))
        return base64.urlsafe_b64decode(data)

    try:
        sig, payload = signed_request.split('.', 1)
    except ValueError:
        pass  # ignore if can't split on dot
    else:
        sig = base64_url_decode(sig)
        data = json.loads(base64_url_decode(payload))
        expected_sig = hmac.new(SOCIAL_AUTH_FACEBOOK_SECRET, msg=payload,
                                digestmod=hashlib.sha256).digest()
        # allow the signed_request to function for upto 1 day
        if constant_time_compare(sig, expected_sig) and \
           data['issued_at'] > (time.time() - 86400):
            return data
