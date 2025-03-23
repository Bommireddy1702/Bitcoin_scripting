from bitcoinrpc.authproxy import AuthServiceProxy
from decimal import Decimal
from pprint import pprint

# RPC Connection Setup
rpc_user = "bitcoinrpc"
rpc_password = "password"
wallet_name = "legacy_wallet1"

rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443/wallet/{wallet_name}")
print("\n✅ Connected to Bitcoin Core Wallet\n")

# Generate New Addresses
print("🎯 Generating new addresses:")
addr_A = rpc_connection.getnewaddress("Address_A", "legacy")
addr_B = rpc_connection.getnewaddress("Address_B", "legacy")
addr_C = rpc_connection.getnewaddress("Address_C", "legacy")

print(f"Address A: {addr_A}")
print(f"Address B: {addr_B}")
print(f"Address C: {addr_C}")

# Fund Address A
print("\n💰 Mining 101 blocks to fund wallet...")
mining_address = rpc_connection.getnewaddress()  # Get new address for mining
rpc_connection.generatetoaddress(101, mining_address)
print("⛏️ 101 blocks mined. Coinbase rewards matured.")

# Send 20 BTC to Address A
fund_txid = rpc_connection.sendtoaddress(addr_A, Decimal('20'))
print(f"🔄 Funding Address A with 20 BTC, TxID: {fund_txid}")

print("\n⛏️ Mine 1 block to confirm funding transaction...")
rpc_connection.generatetoaddress(1, mining_address)
print("✅ 1 block mined to confirm funding.")

# List UTXOs
print("\n🔍 Listing UTXOs:")
utxos = rpc_connection.listunspent()
pprint(utxos)

# Find UTXO for Address A
utxo_A = None
for utxo in utxos:
    if utxo['address'] == addr_A:
        utxo_A = utxo
        break

if utxo_A is None:
    print("\n❌ No UTXO found for Address A. Check if funding succeeded.")
    exit()

print("\n✅ Found UTXO for Address A")

# Create Raw Transaction: A → B
input_txid = utxo_A['txid']
vout = utxo_A['vout']
input_amount = utxo_A['amount']

amount_to_send = Decimal('10')
fee = Decimal('0.0001')
change_amount = input_amount - amount_to_send - fee

print(f"\nInput Amount: {input_amount} BTC")
print(f"Sending {amount_to_send} BTC to B")
print(f"Fee: {fee} BTC")
print(f"Change Back to A: {round(change_amount, 8)} BTC")

raw_tx = rpc_connection.createrawtransaction(
    [{"txid": input_txid, "vout": vout}],
    {
        addr_B: float(amount_to_send),
        addr_A: float(round(change_amount, 8))
    }
)
print("\n🔨 Raw Transaction Hex (A → B):")
print(raw_tx)

# Sign Transaction
signed_tx = rpc_connection.signrawtransactionwithwallet(raw_tx)
print("\n🖊️ Signed Transaction:")
pprint(signed_tx)

# Broadcast Transaction
txid_A_to_B = rpc_connection.sendrawtransaction(signed_tx['hex'])
print(f"\n✅ Broadcasted Transaction A → B TxID: {txid_A_to_B}")

# Mine 1 Block
print("\n⛏️ Mining 1 block to confirm A → B transaction...")
rpc_connection.generatetoaddress(1, mining_address)
print("✅ Transaction confirmed with 1 block mined.")

# Save Addresses to File
with open('legacy_addresses.txt', 'w') as f:
    f.write(f"{addr_A}\n{addr_B}\n{addr_C}\n")
print("\n📄 Saved addresses to 'legacy_addresses.txt' for reuse.")

# Decode Raw Transaction
decoded_tx = rpc_connection.decoderawtransaction(signed_tx['hex'])
print("\n🔍 Decoded Transaction A → B:")
pprint(decoded_tx)

