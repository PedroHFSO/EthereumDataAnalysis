const Web3 = require("web3")
const http = require('http');

var options = {
  timeout: 30000,
  clientConfig: {
    maxReceivedFrameSize: 100000000,
    maxReceivedMessageSize: 100000000,
  },
  reconnect: {
    auto: true,
    delay: 5000,
    maxAttempts: 15,
    onTimeout: false,
  },
};

var fs = require('fs')
var logger = fs.createWriteStream('dataset.txt', {
  flags: 'a' // 'a' means appending (old data will be preserved)
})


const web3 = new Web3(new Web3.providers.WebsocketProvider("wss://mainnet.infura.io/ws/v3/0e2d1b8de01f4274b69eb1a54caf3518"), options = options)

const subscription = web3.eth.subscribe("pendingTransactions", (err, res) => {
  if (err) console.error(err);
});

const block_subscription = web3.eth.subscribe("newBlockHeaders", (err, res) => {
  if (err) console.error(err);
});

transaction_pool = {};
transactions = [];

const pendingTransactions = function(){
    subscription.on("data", (txHash) => {
      setTimeout(async () => {
        if(txHash != null){
            transaction_pool[txHash] = new Date().getTime();
        }
      });
    });
}

var checkBlock = function(block){
    let current = new Date().getTime();
    let timestamp = block['timestamp'];
    for(tx of block['transactions']){
        if(tx['hash'] in transaction_pool){
            tx_new = {
                'hash': tx['hash'],
                'block_number': block['number'],
                'from': tx['from'],
                'to': tx['to'],
                'value': tx['value'],
                'gas_price': tx['gasPrice'],
                'gas': tx['gas'],
                'joined_pool': transaction_pool[tx['hash']],
                'joined_chain' : current,
                'confirmed' : '-1' //we don't know if the transaction was confirmed yet
            }
            delete tx['hash'];
            logger.write('\n'+tx_new['hash']+','
                +tx_new['block_number']+','
                +tx_new['from']+','
                +tx_new['to']+','
                +tx_new['value']+','
                +tx_new['gas_price']+','
                +tx_new['gas']+','
                +tx_new['joined_pool']+','
                +tx_new['joined_chain']+','
                +tx_new['confirmed']);
            //transactions.push(tx_new);
        }
    }
}

const newBlocks = function(){
    block_subscription.on("data", (block) =>{
        setTimeout(async() => {
            let block_number = block["number"];
            console.log(block_number);
            try{
                let full_block = await web3.eth.getBlock(block_number, true);
                await checkBlock(full_block);
            }catch(err){
                console.log(err);
            }
        });
    });
}

pendingTransactions();
newBlocks();

const hours = 3;
const min = 60*hours;
const timeout = false;

if(timeout){
    setTimeout(function() {
            //console.log(transactions);
            logger.end();
            process.exit();
        }
    , min*60000);
}
