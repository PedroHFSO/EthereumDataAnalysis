import requests
with open('config.txt') as f:
    api_key = f.readline()

first_block = int(input('Input # of first block collected'))
last_block = int(input('Input # of last block collected'))
url_start = 'https://api.etherscan.io/api?module=proxy&action=eth_getBlockByNumber&tag='
#block number goes in the middle
url_end = '&boolean=true&apikey='+api_key

def collectBlock(block_num, f):
    block_num = hex(block_num) #needed conversion for the etherscan api
    url = url_start+str(block_num)+url_end
    re = requests.get(url)
    base_fee = re['result']['baseFeePerGas']
    for tx in re['result']['transactions']:
        hash_ = tx['hash']
        gas_price = tx['gasPrice']
        type_ = tx['type']
        value = tx['value']
        to = tx['to']
        from_ = tx['from']
        f.write(hash_+','+str(block_num)+','+base_fee+','+gas_price+','+type_+','+value+','+to+','+from_) #don't remember if i need to break the line here, needs testing


print('Starting block collection...')
for i in range(first_block, last_block + 1):
    #necessary header for dataset.csv as it follows:
    #hash,block_num,base_fee,gas_price,type,value,to,from
    with open('dataset.csv', 'a') as f: 
        collectBlock(i, f)
print('All blocks were collected!')
