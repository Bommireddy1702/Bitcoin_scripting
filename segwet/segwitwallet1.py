from bitcoinrpc.authproxy import AuthServiceProxy
from decimal import Decimal
from pprint import pprint

# RPC Connection Setup
rpc_user = "bitcoinrpc"
rpc_password = "password"
wallet_name = "segwit_wallet7"

rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443/wallet/{wallet_name}")

# Load Addresses from file
with open("segwit_addresses.txt", "r") as f:
    addr_A = f.readline().strip()
    addr_B = f.readline().strip()
    addr_C = f.readline().strip()

print(f"Address A: {addr_A}")
print(f"Address B: {addr_B}")
print(f"Address C: {addr_C}")

# Mine 150 blocks to A for balance
rpc_connection.generatetoaddress(150, addr_A)

print("\n🔍 Listing UTXOs:")
utxos = rpc_connection.listunspent()
pprint(utxos)

# Find UTXO for A
utxo_A = None
for utxo in utxos:
    if utxo['address'] == addr_A:
        utxo_A = utxo
        break

if utxo_A is None:
    print("❌ No UTXO found for Address A")
    exit()

print("\n✅ Found UTXO for Address A")

# Transaction A → B
input_txid = utxo_A['txid']
vout = utxo_A['vout']
input_amount = utxo_A['amount']
# Set the transaction fee
fee = Decimal('0.0001')  # Fee for the transaction

# Ensure you send the full balance minus the fee
available_balance = input_amount - fee

# Check if available balance is sufficient for the transaction
if available_balance <= 0:
    print("❌ Insufficient funds after fee.")
    exit()

# Set the amount to send to B as the full available balance minus fee
amount_to_send = available_balance

# Now, there will be no change, and the entire available balance is used
raw_tx = rpc_connection.createrawtransaction(
    [{"txid": input_txid, "vout": vout}],
    {addr_B: float(amount_to_send)}  # Send all the available balance to addr_B
)

print("\nRaw Transaction Hex (A → B):")
print(raw_tx)

# Sign the transaction
signed_tx = rpc_connection.signrawtransactionwithwallet(raw_tx)
print("\nSigned Transaction:")
pprint(signed_tx)

# Broadcast the transaction
try:
    txid_A_to_B = rpc_connection.sendrawtransaction(signed_tx['hex'])
    print(f"\n✅ Broadcasted A → B TxID: {txid_A_to_B}")
except Exception as e:
    print(f"❌ Error broadcasting transaction: {e}")

# Mine 1 block to confirm the transaction
rpc_connection.generatetoaddress(1, addr_A)
print("\n⛏️ Mined 1 block to confirm A → B transaction")




