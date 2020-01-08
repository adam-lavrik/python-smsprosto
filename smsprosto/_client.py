# Copyright 2020 Adam Lavrik <lavrik.adam@gmail.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#  http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import json, requests
from sys import version_info

from . import _schemas


_API_URL_0 = "http://api.sms-prosto.ru"
_API_URL_1 = "http://ssl.bs00.ru"

class ApiException(Exception):
    """
    Represents error returned by service API.
    Fields:
    * code (integer) - error code;
    * type (string) - error type: 'message' (on success), 'notice', 'error';
    * text (string) - error description (in Russian).
    """
    def __init__(self, code, type, text):
        self.code = code
        self.type = type
        self.text = text

    def __str__(self):
        return self.text if version_info.major > 2 else self.text.encode('utf-8')

class Client:
    """
    Implements SMS sending via API of Prosto SMS service (https://sms-prosto.ru).
    Fields:
    * _url - currently used URL of API.
    * _spare_url - another usable URL of API.
    * _parameters - default parameters to pass to API.
    """
    def __init__(self, key, password=None):
        """
        Creates Client instance, initializes it by API URLs and sets JSON as response format.
        Single argument passed is considered as API key.
        Two arguments passed are considered as login (e-mail) and password pair.
        """
        self._url = _API_URL_0
        self._spare_url = _API_URL_1
        self._parameters = (
            {'key': key}
            if password is None else
            {'email': key, 'password': password}
        )
        self._parameters['format'] = 'json'

    def url(self):
        """
        Returns URL currently used for requests by this Client instance.
        """
        return self._url

    def switch_url(self):
        """
        Toggles `Client` instance between using main or spare URL.
        """
        self._url, self._spare_url = self._spare_url, self._url

    def _request(self, method, schema, parameters={}):
        """
        Performs POST request with given `parameters` (including `method`) and returns raw HTTP response.
        Raises ApiException if request fails.
        Returns dictionary with items validated according to given `schema`.
        """
        parameters['method'] = method
        parameters.update(self._parameters)
        response = requests.post(self._url, parameters)
        if response.status_code != 200:
            raise "HTTP error. Status code is " + str(response.status_code)
        request_result = json.loads(response.text)['response']
        # Check for API error
        error = request_result['msg']
        error_code = int(error['err_code'])
        if error_code != 0:
            raise ApiException(error_code, error['type'], error['text'])
        # No API error; extract, clean and return data
        return {key: schema[key](value) for key, value in request_result['data'].items() if key in schema}

    def push_message(self, phone, text, sender_name=None):
        """
        Performs request to API to push SMS. Raises ApiException if request fails.
        Arguments:
        * `text` (utf-8 str) - SMS text;
        * `phone` (utf-8 str) - SMS recipient phone number in format: '7XXXXXXXXXX' (Russia);
        * `sender_name` (str) - sender's signature (only Latin letters); if omitted, default sender name from account profile is used.
        Returns dictionary, holding the following items:
        * id (int) - SMS identifiers assigned by service;
        * sender_name (utf-8 str) - sender name, this SMS is signed with;
        * n_raw_sms (int) - count of single message parts the original message was splitted onto;
        * credits (Decimal) - price of the single message part.
        """
        extra_parameters = {'phone': phone, 'text': text}
        if sender_name is not None:
            extra_parameters['sender_name'] = sender_name
        return self._request('push_msg', _schemas._PUSH_MESSAGE, extra_parameters)

    def message_report(self, id):
        """
        Provides an information about SMS been previously sent.
        Arguments:
        `id` (int) - SMS identifier (previously returned in `push_message` output).
        Returns dictionary, holding the following items (or their subset for undelivered message):
        * id (int) - SMS identifier;
        * sender_name (utf-8 str) - sender name, this SMS is signed with;
        * text (utf-8 str) - SMS text;
        * phone (utf-8 str) - SMS recipient phone number in format: '7XXXXXXXXXX' (Russia);
        * is_flash (bool) - whether the message is standard (False) or flash (True);
        * start_time (datetime) - SMS sending date and time;
        * last_update (datetime) - SMS final status receiving date and time (None for undelivered message);
        * n_raw_sms (int) - count of single message parts the original message was splitted onto;
        * credits (Decimal) - price of the single message part;
        * state (int) - SMS status:
            0 - sent
            1 - delivered
            2 - not delivered
            4 - enqueued on SMSC
            8 - delivered to SMSC
            16 - not delivered to SMSC.
        * state_text (str) - textual description of SMS status (in Russian).
        """
        return self._request('get_msg_report', _schemas._MESSAGE_REPORT, {'id': id})

    def account_profile(self):
        """
        Provides an information about user account this `Client` instance is associated with.
        Returns dictionary, holding the following items:
        * id (int) - account identifier;
        * sender_name (utf-8 str) - default sender name to sign SMS;
        * first_name (utf-8 str) - user first name;
        * last_name (utf-8 str) - user last name;
        * email (utf-8 str) - user e-mail address;
        * credits (Decimal) - account balance;
        * credits_used (dec) - spent sum;
        * credits_name (utf-8 str) - currency name (Rubles);
        * currency (utf-8 str) - currency name (Rubles);
        * referral_id (int) - referral identifier.
        """
        return self._request('get_profile', _schemas._ACCOUNT_PROFILE)
