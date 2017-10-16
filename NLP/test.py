# coding=utf-8
import requests
from lxml import html

LOGIN_URL = 'https://github.com/login'
SESSION_URL = 'https://github.com/session'

s = requests.session()
r = s.get(LOGIN_URL)
tree = html.fromstring(r.text)
el = tree.xpath('//input[@name="authenticity_token"]')[0]
authenticity_token = el.attrib['value']

    

