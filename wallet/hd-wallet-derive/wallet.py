# FUNCTION TO RUN HD_DERIVE ON GITBASH
import subprocess, pathlib, tempfile
import json
GIT_BASH = r"C:\Program Files\Git\git-bash.exe"
def run_git_bash_cmd(cmd):
    with tempfile.TemporaryDirectory() as tmpdir:
        target = pathlib.Path(tmpdir) / "output_file"
        dirname, fname = target.parts[-2:]
        sh_target = f"/tmp/{dirname}/{fname}"
        git_bash_cmd = [GIT_BASH, "--hide", "--no-needs-console", "-lc", f"{cmd} > {sh_target}"]
        #print(git_bash_cmd)
        cmd_result = subprocess.run(git_bash_cmd)
        #print(cmd_result)
        #keys = json.loads(cmd_result)
        cmd_result.check_returncode()
        with target:
            result = target.open().read()
        return result

 CODE TO GENERATE WALLET WITH 3 SETS OF KEYS
import subprocess
import json
from constants import *
import os

mnemonic = os.getenv('mnemonic')

#coinlist=[constants.BTC,constants.BTCTEST,constants.ETH]
coinlist=['btc','btc-test','eth']
print(coinlist)
coins={}

for coin in coinlist:
    wallet=run_git_bash_cmd('./hd-wallet-derive.php -g --coin='+str(coin)+' --mnemonic='+str(mnemonic)+' --numderive=3 --cols=index,address,path,privkey,pubkey,pubkeyhash,xprv,xpub --format=jsonpretty')
    coins.update({coin:json.loads(wallet)})
print(json.dumps(coins,indent=1))

# FUNCTION TO EXTRACT SPECIFIC PRIVATE KEY BY INDEX AND COIN TYPE
def get_priv_key(coin_name,coin_index):
    for k1,v1 in coins.items():
        for elements in v1:
            if coin_name==k1 and coin_index==elements['index']:
                return(elements['privkey'])

def get_address(coin_name,coin_index):
    for k1,v1 in coins.items():
        for elements in v1:
            if coin_name==k1 and coin_index==elements['index']:
                return(elements['address'])            

# TEST FUNCTION ON BTC 0 Keys
get_priv_key('btc',0)
get_address('btc',0)

# FUNCTION TO CONVERT PRIVATE KEY TO ACCOUNT
from web3 import Web3
from bit import *
from eth_account import Account
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

def priv_key_to_account(coin_name,coin_priv_key):
    if coin_name=='eth':
        return(Account.privateKeyToAccount(coin_priv_key))
    if coin_name=='btc_test':
        return(PrivateKeyTestnet(priv_key))

# TEST FUNCTION ON ETH 0 and BTC-TEST 1 Keys
priv_key_to_account('eth',get_priv_key('eth',0))
priv_key_to_account('btc-test',get_priv_key('btc-test',1))

# FUNCTION TO CREATE TRANSACTION
def create_tx(coin_name,account,recipient,amount):
    if coin_name=='eth':
        gasEstimate = w3.eth.estimateGas({"from": account.address, "to": recipient, "value": amount})
    return {
        "from": account.address,
        "to": recipient,
        "value": amount,
        "gasPrice": w3.eth.gasPrice,
        "gas": gasEstimate,
        "nonce": w3.eth.getTransactionCount(account.address),
    }
    if coin_name=='btc_test':
        return(PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, coin_name)]))
# TEST FUNCTION ON ETH 0 and BTC-TEST 1 Keys
create_tx('eth',priv_key_to_account('eth',get_priv_key('eth',0)),get_address('eth',1),1)
create_tx('btc-test',priv_key_to_account('btc-test',get_priv_key('btc-test',0)),get_address('btc-test',1),1)

# FUNCTION TO SEND TRANSACTION
def send_tx(coin_name, account,receipent,amount):
    if coin_name='eth':
        tx = create_raw_tx(account, recipient, amount)
        signed_tx = account.sign_transaction(tx)
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(result.hex())
        return result.hex()
    if coin_name='btc_test':
        tx = create_raw_tx(account, recipient, amount,'btc')
        key=wif_to_key(get_priv_key('btc',0))
        tx_hex = key.sign_transaction(tx_data)

## TEST PRE_FUNDING OF ACCOUNT

from web3 import Web3
from eth_account import Account
from web3.middleware import geth_poa_middleware
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.eth.getBalance("0x2222C2EF61816F5D61c74f429E20c4dFF6a474b3")

from constants import *
print(constants.)