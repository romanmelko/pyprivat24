"""
Python module for working with transactions in PrivatBank
requirements: you need to create merchant in Privat24.
After that set the following parameters in parent program
password: <merchant password>
merchant_id: <merchant ID>
card_number: <bank card number>
start_date: <start date of transactions>
end_date: <end date of transactions>
Example:
from pyprivat24 import pyprivat24
privat = pyprivat24.PrivatBank(merchant_id, merchant_password, card_number)
tx_list = privat.txget('24.11.2019', '25.11.2019')
"""

from hashlib import sha1, md5
from string import Template
from datetime import datetime, timedelta
from requests import post


class PrivatBank():
    """ get transactions via REST API """

    def __init__(self, merchant_id, password, card_number):
        self.url = 'https://api.privatbank.ua/p24api'
        now = datetime.now()
        self.end_date = now.strftime('%d.%m.%Y')
        self.start_date = (now.date() - timedelta(1)).strftime('%d.%m.%Y')
        self.xml = Template(
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
        self.merchant_id = merchant_id
        self.password = password
        self.card_number = card_number

    def _gen_xml(self, data, start_date, end_date):
        """ generate XML based on signature + data """
        data = data.substitute(
            start_date=start_date, end_date=end_date, card_number=self.card_number)
        signature = sha1(md5(data + self.password).hexdigest()).hexdigest()
        xml_data = self.xml.substitute(
            merchant_id=self.merchant_id, signature=signature, data=data)
        return xml_data

    def txget(self, start_date, end_date):
        """ get the list of transactions based on date range provided """
        url = self.url + '/rest_fiz'
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
        # prepare XML for request
        xml_data = self._gen_xml(data, start_date, end_date)
        # perform a request and get transactions list
        result = post(url, data=str(xml_data), headers={
            'Content-Type': 'application/xml; charset=UTF-8'}
                      ).text
        return result
