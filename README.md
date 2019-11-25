# pyprivat24
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
