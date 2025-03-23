from bitcoinrpc.authproxy import AuthServiceProxy
from decimal import Decimal
from pprint import pprint

# RPC Connection
rpc_user = "bitcoinrpc"
rpc_password = "password"
wallet_name = "segwit_wallet7"

rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443/wallet/{wallet_name}")

# Load Addresses
with open("segwit_addresses.txt", "r") as f:
    addr_A = f.readline().strip()
    addr_B = f.readline().strip()
    addr_C = f.readline().strip()

print(f"Address B: {addr_B}")
print(f"Address C: {addr_C}")

print("\n🔍 Listing UTXOs:")
utxos = rpc_connection.listunspent()
pprint(utxos)

# Find UTXO for B
utxo_B = None
for utxo in utxos:
    if utxo['address'] == addr_B:
        utxo_B = utxo
        break

if utxo_B is None:
    print("❌ No UTXO found for Address B!")
    exit()

print("\n✅ Found UTXO for Address B")

# Transaction B → C
input_txid = utxo_B['txid']
vout = utxo_B['vout']
input_amount = utxo_B['amount']

# Set the transaction fee
fee = Decimal('0.0001')  # Fee for the transaction

# Ensure you send the full balance minus the fee
available_balance = input_amount - fee

# Check if available balance is sufficient for the transaction
if available_balance <= 0:
    print("❌ Insufficient funds after fee.")
    exit()

# Set the amount to send to C as the full available balance minus fee
amount_to_send = available_balance

# Now, there will be no change, and the entire available balance is used
raw_tx = rpc_connection.createrawtransaction(
    [{"txid": input_txid, "vout": vout}],
    {addr_C: float(amount_to_send)}  # Send all the available balance to addr_C
)

print("\nRaw Transaction Hex (B → C):")
print(raw_tx)

# Sign the transaction
signed_tx = rpc_connection.signrawtransactionwithwallet(raw_tx)
print("\nSigned Transaction:")
pprint(signed_tx)

# Broadcast the transaction
try:
    txid_B_to_C = rpc_connection.sendrawtransaction(signed_tx['hex'])
    print(f"\n✅ Broadcasted B → C TxID: {txid_B_to_C}")
except Exception as e:
    print(f"❌ Error broadcasting transaction: {e}")

# Mine 1 block to confirm the transaction
rpc_connection.generatetoaddress(1, addr_B)
print("\n⛏️ Mined 1 block to confirm B → C transaction")
