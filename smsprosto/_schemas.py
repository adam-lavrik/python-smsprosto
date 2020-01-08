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

from datetime import datetime
from decimal import Decimal


_int_to_is_flash = lambda integer: integer == 0
_int_or_str_to_int = lambda value: value if type(value) == int else int(value)
_str = lambda string: string
_str_to_datetime = lambda string: string and datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
_str_to_decimal = lambda string: Decimal(string)
_str_to_int = lambda string: int(string)

_PUSH_MESSAGE = {
    'id': _str_to_int,
    'sender_name': _str,
    'n_raw_sms': _str_to_int,
    'credits': _str_to_decimal
}

_MESSAGE_REPORT = {
    'id': _str_to_int,
    'sender_name': _str,
    'text': _str,
    'phone': _str,
    'is_flash': _int_to_is_flash,
    'start_time': _str_to_datetime,
    'last_update': _str_to_datetime,
    'n_raw_sms': _str_to_int,
    'credits': _str_to_decimal,
    'state': _int_or_str_to_int,
    'state_text': _str
}

_ACCOUNT_PROFILE = {
    'id': _str_to_int,
    'sender_name': _str,
    'first_name': _str,
    'last_name': _str,
    'email': _str,
    'credits': _str_to_decimal,
    'credits_used': _str_to_decimal,
    'credits_name': _str,
    'currency': _str,
    'referral_id': _str_to_int
}
