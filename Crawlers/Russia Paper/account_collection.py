import pandas as pd 
import requests

api_key = 'DH1IHX1N6XZD5STWKPM9SFV5WJCF9PXMGD'
url = ('https://api.etherscan.io/api'
    '?module=proxy'
    '&action=eth_getBlockByNumber'
    '&tag=BLOCK'
    '&boolean=true'
    '&apikey='+api_key)


#initial_block = 13974427 #Primeiro bloco do dia 10/01/2022
#last_block = 14019699 #Último bloco do dia 17/01/2022 

#initial_block = 14019700 #Primeiro bloco do dia 10/01/2022
#last_block = 14064996 #Último bloco do dia 17/01/2022 

initial_block = 14064997 #Primeiro bloco do dia 10/01/2022
last_block = 14110299 #Último bloco do dia 17/01/2022 

f = open('accs_3.csv', 'a')

for i in range(initial_block, last_block + 1):
    try:

        block_hex = hex(i)
        r = requests.get(url.replace('BLOCK', block_hex))
        result = base_fee = r.json()['result']
        tx_list = result['transactions']
        for tx in tx_list:
            f.write('\n'+str(tx['from']+','+str(tx['to'])))
    except Exception as err:
        print(err)
        pass
    finally:
        if i % 50 == 0:
            f.flush()