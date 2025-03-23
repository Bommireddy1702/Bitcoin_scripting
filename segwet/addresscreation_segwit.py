from bitcoinrpc.authproxy import AuthServiceProxy
from decimal import Decimal
from pprint import pprint

# RPC Connection Setup
rpc_user = "bitcoinrpc"
rpc_password = "password"
wallet_name = "segwit_wallet7"

# Connect to the SegWit Wallet
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443/wallet/{wallet_name}")

# Generate 3 SegWit Addresses (P2SH-P2WPKH)
addr_A = rpc_connection.getnewaddress("Address_A", "p2sh-segwit")
addr_B = rpc_connection.getnewaddress("Address_B", "p2sh-segwit")
addr_C = rpc_connection.getnewaddress("Address_C", "p2sh-segwit")

print("\nGenerated Addresses:")
print(f"Address A: {addr_A}")
print(f"Address B: {addr_B}")
print(f"Address C: {addr_C}")

# Save to file for use in wallet1 and wallet2
with open("segwit_addresses.txt", "w") as f:
    f.write(f"{addr_A}\n{addr_B}\n{addr_C}")

print("\n✅ Addresses saved to segwit_addresses.txt")

