Prerequisites

Bitcoin Core installed and running in regtest mode

Basic understanding of SegWit and Legacy transactions

Familiarity with Bitcoin CLI

Steps to Execute:
2. Start Bitcoin Core in Regtest Mode

bitcoind -regtest -daemon

Check if it’s running:

bitcoin-cli -regtest getblockchaininfo

3. Create a SegWit Wallet

bitcoin-cli -regtest createwallet "segwit_wallet_7"

4. Retrieve Wallet Information

bitcoin-cli -regtest getwalletinfo

5. Obtain Code from Documents

Retrieve necessary transaction details from segwit_wallet_1 and segwit_wallet_2.

6. Create Transactions

1. Transaction A → B


2. Transaction B → C



After initiating transactions, obtain their Transaction IDs (TxIDs).

7. Get Transaction Details

Retrieve transaction details using TxID:

bitcoin-cli -regtest gettransaction "<Transaction_ID>"

This will return all details, including inputs, outputs, confirmations, and fees.

8. Check Unspent Transactions

List all unspent transactions:

bitcoin-cli -regtest listunspent

9. Decode Raw Transaction

Get raw transaction:

bitcoin-cli -regtest getrawtransaction "<Transaction_ID>"

Decode the raw transaction:

bitcoin-cli -regtest decoderawtransaction "<Raw_Transaction_Hex>"