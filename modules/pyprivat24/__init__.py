"""
Python module for working with transactions in PrivatBank
requirements: you need to create merchant in Privat24. After that set the following parameters in parent program
password: merchant password
merchant_id: merchant ID
card_number: bank card number
start_date: start date of transactions
end_date: end date of transactions
"""

from requests import post
from hashlib import sha1, md5
from string import Template
import datetime


class PrivatBank:

    def __init__(self):
        pass


class GetTX(PrivatBank):

    # default API endpoint
    url = "https://api.privatbank.ua/p24api/rest_fiz"
    # define XML for request
    xml = Template(
        '<?xml version="1.0" encoding="UTF-8"?>' +
        '<request version="1.0">' +
        '<merchant>' +
        '<id>$merchant_id</id>' +
        '<signature>$signature</signature>' +
        '</merchant>' +
        '<data>' +
        '$data' +
        '</data>' +
        '</request>'
    )
    # data part of XML used in signature generation
    data = Template(
        '<oper>cmt</oper>' +
        '<wait>0</wait>' +
        '<test>0</test>' +
        '<payment id="">' +
        '<prop name="sd" value="$start_date" />' +
        '<prop name="ed" value="$end_date" />' +
        '<prop name="card" value="$card_number" />' +
        '</payment>'
    )
    password = ''
    merchant_id = ''
    card_number = ''
    now = datetime.datetime.now()
    end_date = now.strftime('%d.%m.%Y')
    start_date = (now.date() - datetime.timedelta(1)).strftime('%d.%m.%Y')

    def gen_xml(self):
        """ generate signature """

        data = self.data.substitute(start_date=self.start_date, end_date=self.end_date, card_number=self.card_number)
        # generate signature
        signature = sha1(md5(data + self.password).hexdigest()).hexdigest()
        # update XML with signature
        xml_data = self.xml.substitute(merchant_id=self.merchant_id, signature=signature, data=data)

        return xml_data

    def get(self):
        """ get events """

        # prepare XML for request
        xml_data = str(self.gen_xml())

        # perform a request and get transactions list
        result = post(self.url, data=xml_data, headers={'Content-Type': 'application/xml; charset=UTF-8'}).text

        return result
