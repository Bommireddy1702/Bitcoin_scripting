from bitcoinrpc.authproxy import AuthServiceProxy
from decimal import Decimal
from pprint import pprint

# RPC Connection Setup
rpc_user = "bitcoinrpc"
rpc_password = "password"
wallet_name = "legacy_wallet1"

rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443/wallet/{wallet_name}")
print("\n✅ Connected to Bitcoin Core Wallet\n")

# Read Addresses from File
with open('legacy_addresses.txt', 'r') as f:
    addr_A, addr_B, addr_C = f.read().splitlines()

print(f"Address A: {addr_A}")
print(f"Address B: {addr_B}")
print(f"Address C: {addr_C}")

# List UTXOs
print("\n🔍 Listing UTXOs:")
utxos = rpc_connection.listunspent()
pprint(utxos)

# Find UTXO for Address B
utxo_B = None
for utxo in utxos:
    if utxo['address'] == addr_B:
        utxo_B = utxo
        break

if utxo_B is None:
    print("\n❌ No UTXO found for Address B. Make sure A → B transaction confirmed!")
    exit()

print("\n✅ Found UTXO for Address B")

# Create Raw Transaction: B → C
input_txid = utxo_B['txid']
vout = utxo_B['vout']
input_amount = utxo_B['amount']

amount_to_send = Decimal('9.999')
fee = Decimal('0.0001')
change_amount = input_amount - amount_to_send - fee

print(f"\nInput Amount: {input_amount} BTC")
print(f"Sending {amount_to_send} BTC to C")
print(f"Fee: {fee} BTC")
print(f"Change Back to B: {round(change_amount, 8)} BTC")

raw_tx = rpc_connection.createrawtransaction(
    [{"txid": input_txid, "vout": vout}],
    {
        addr_C: float(amount_to_send),
        addr_B: float(round(change_amount, 8))
    }
)
print("\n🔨 Raw Transaction Hex (B → C):")
print(raw_tx)

# Sign Transaction
signed_tx = rpc_connection.signrawtransactionwithwallet(raw_tx)
print("\n🖊️ Signed Transaction:")
pprint(signed_tx)

# Broadcast Transaction
txid_B_to_C = rpc_connection.sendrawtransaction(signed_tx['hex'])
print(f"\n✅ Broadcasted Transaction B → C TxID: {txid_B_to_C}")

# Mine 1 Block
mining_address = rpc_connection.getnewaddress()
print("\n⛏️ Mining 1 block to confirm B → C transaction...")
rpc_connection.generatetoaddress(1, mining_address)
print("✅ Transaction confirmed with 1 block mined.")

# Decode Raw Transaction
decoded_tx = rpc_connection.decoderawtransaction(signed_tx['hex'])
print("\n🔍 Decoded Transaction B → C:")
pprint(decoded_tx)

# Save TxID to File for Debugging
with open('b_to_c_txid.txt', 'w') as f:
    f.write(txid_B_to_C)
print("\n📄 Saved B → C Transaction ID to 'b_to_c_txid.txt'. Use it for decoding/debugging.")

