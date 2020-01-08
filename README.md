# python-smsprosto

This package provides a convenient Python wrapper over API of Russian SMS service [Prosto SMS](https://sms-prosto.ru).

It is licensed under [Apache 2.0 license](http://www.apache.org/licenses/LICENSE-2.0).

Usage:

## Import

```python
import smsprosto
# OR
from smsprosto import Client
# OR
from smsprosto import ApiException, Client
```

The second or third variant of import is implied below.

## Authorize

"Prosto SMS" user account must already exist.

```python
client = Client('<account e-mail address>', '<account password>') # Authorizing with e-mail as login and password (2 parameters)
# OR
client = Client('<API key>') # Authorizing with API key (1 parameter).
```

## Push message
```python
response = client.push_message('7XXXXXXXXXX', "Hello, there!") # Send message with a default sender signature.
# OR
response = client.push_message('7XXXXXXXXXX', "Here's Johny!", "Jack") # Send message with a different sender signature (only latin letters allowed).
```

If there is no exception, the following `dict` will be assigned to `response`:
* id (int) - SMS identifiers assigned by service;
* sender_name (utf-8 str) - sender name, this SMS is signed with;
* n_raw_sms (int) - count of single message parts the original message was splitted onto;
* credits (Decimal) - price of the single message part.

## Get message report
```python
report = client.message_report(<message id>) # <message id> has been previously returned in `push_message` output.
```

If there is no exception, the following `dict` will be assigned to `report` (note: for undelivered message some of items can be absent or None):
* id (int) - SMS identifier;
* sender_name (utf-8 str) - sender name, this SMS is signed with;
* text (utf-8 str) - SMS text;
* phone (utf-8 str) - SMS recipient phone number (in format: '7XXXXXXXXXX');
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
* state_text (utf-8 str) - textual description of SMS status (in Russian).

## Get information about your account
```python
profile = client.account_profile()
```

If there is no exception, the following `dict` will be assigned to `profile`:
* id (int) - account identifier;
* sender_name (utf-8 str) - default sender name to sign SMS;
* first_name (utf-8 str) - user first name;
* last_name (utf-8 str) - user last name;
* email (utf-8 str) - user e-mail address;
* credits (Decimal) - account balance;
* credits_used (Decimal) - spent sum;
* credits_name (utf-8 str) - currency name (Rubles);
* currency (utf-8 str) - currency name (Rubles);
* referral_id (int) - referral identifier.

## Catch API exceptions
```python
from smsprosto import ApiException, Client

try:
    client = Client(...)
    message_id = client.push_message(...)['id']
    report = client.message_report(message_id)
    profile = client.account_profile()
except ApiException as ae:
    # Processing API error
    print(ae.code)
    print(ae.type)
    print(ae.text)
except:
    # Processing other errors
    ...
```

(C) Adam Lavrik, 2020
