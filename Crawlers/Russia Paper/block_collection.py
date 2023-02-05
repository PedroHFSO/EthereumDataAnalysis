import pandas as pd 
import requests

api_key = 'DH1IHX1N6XZD5STWKPM9SFV5WJCF9PXMGD'
url = ('https://api.etherscan.io/api'
    '?module=proxy'
    '&action=eth_getBlockByNumber'
    '&tag=BLOCK'
    '&boolean=true'
    '&apikey='+api_key)

initial_block = 14310658 #Primeiro bloco do dia 24/02/2022
#initial_block = 14175350 #Meio do dia 10/02/2022, onde parei
last_block = 14355747 #Último bloco do dia 02/03/2022 

f = open('blocks_war_4.csv', 'a')
f_2 = open('war_txs_4.csv', 'a')

for i in range(initial_block, last_block + 1):
    try:
        block_hex = hex(i)
        r = requests.get(url.replace('BLOCK', block_hex))
        result = base_fee = r.json()['result']
        base_fee = result['baseFeePerGas']
        gas_lim = result['gasLimit']
        gas_used = result['gasUsed']
        miner = result['miner']
        tx_list = result['transactions']
        timestamp = result['timestamp']

        f.write('\n'+str(block_hex)+','+str(base_fee)+','+str(gas_lim)+','+str(gas_used)+','
                +miner+','+str(len(tx_list))+','+str(timestamp))
        for tx in tx_list:
            maxFee = -1
            maxPriorityFee = -1
            if 'maxFeePerGas' in tx:
                maxFee = tx['maxFeePerGas']
            if 'maxPriorityFeePerGas' in tx:
                maxPriorityFee = tx['maxPriorityFeePerGas']
            f_2.write('\n'+str(tx['hash'])+','+str(tx['blockNumber'])+','+str(timestamp)+','+str(tx['from'])+','+str(tx['to'])+','+
            str(tx['type'])+','+str(maxFee)+','+str(maxPriorityFee)+','+str(base_fee))
    except Exception as err:
        print(err)
        pass
    finally:
        if i % 50 == 0:
            f.flush()
            f_2.flush()
