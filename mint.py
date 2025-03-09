from web3 import Web3
from eth_account import Account
import time

# Configure Monad Testnet RPC
MONAD_RPC_URL = "https://testnet-rpc.monad.io"
web3 = Web3(Web3.HTTPProvider(MONAD_RPC_URL))

# Wallet Private Key (Use a test wallet, never share real keys!)
PRIVATE_KEY = "your_private_key_here"
account = Account.from_key(PRIVATE_KEY)

# NFT Smart Contract Address & ABI (Replace with actual values)
NFT_CONTRACT_ADDRESS = "0xYourContractAddress"
NFT_ABI = [...]  # ABI of the NFT contract

# Connect to the contract
contract = web3.eth.contract(address=NFT_CONTRACT_ADDRESS, abi=NFT_ABI)

def countdown_timer(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = f"{mins:02d}:{secs:02d}"
        print(f"Minting starts in: {timer}", end="\r")
        time.sleep(1)
        seconds -= 1
    print("\nStarting minting process...")

def mint_nft():
    countdown_timer(7200)  # Set countdown time in seconds
    nonce = web3.eth.get_transaction_count(account.address)
    mint_txn = contract.functions.mint(1).build_transaction({
        'from': account.address,
        'gas': 250000,
        'gasPrice': web3.to_wei('52', 'gwei'),
        'nonce': nonce
    })
    
    # Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(mint_txn, PRIVATE_KEY)
    
    # Send the transaction
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"Transaction sent: {tx_hash.hex()}")
    
    # Wait for transaction receipt
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Transaction confirmed!", receipt)

if __name__ == "__main__":
    mint_nft()
