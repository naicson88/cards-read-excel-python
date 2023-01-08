from pdb import line_prefix
import pandas
import requests
import re
import json
import time

class DTO(object):
    collectionId = ""
    deckName = ""
    isBasedDeck = ""
    cards = ""
    
    def __init__(self, collectionId, deckName, isBasedDeck, cards):
        self.collectionId = collectionId
        self.deckName = deckName
        self.isBasedDeck = isBasedDeck
        self.cards = cards
        
def do_login_and_get_token(url):
    full_path = url+'/auth/login'
    # print('Inset UserName')  
    # user_name = input()
    # print('Inset Password')  
    # password = input()
    login = {'username':'alannaicson','password':'91628319'}
    resp = requests.post(full_path, json=login)
    data = resp.json();
    token = data['accessToken']
    return 'Bearer '+token  

cards_admin = 'http://localhost:8081/v1/admin/deck/new-deck-collection-yugipedia'
yugi_api = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?name='
cards_main = 'http://localhost:8080/yugiohAPI'

excel_data = pandas.read_excel('C:/Users/USER/Documents/PROGRAMACAO/Python/Cards Excel Source Python/files/variant.xlsx')

data_json = excel_data.to_json(orient='records')

cards = json.loads(data_json)

for card in cards:
    api_data = requests.get(yugi_api+card['name'].strip())
    number = api_data.json()['data'][0]['id']
    time.sleep(1)
    card['cardNumber'] = number
    print(card)

dto = {
    "setId": 748,
    "nome": "Speed Duel GX: Midterm Paradox - Variant Cards",
    "isBasedDeck": True,
    "isSpeedDuel": True,
    "setType": "BOX", 
    "setCode": "SGX2",
    "relDeckCards": cards
}

token = do_login_and_get_token(cards_main)

resp = requests.post(cards_admin, headers={"Authorization": token}, json=dto)
# data = resp.json();
# print(data)



