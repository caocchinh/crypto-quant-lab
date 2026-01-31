from eth_account import Account
import secrets
import pandas

address = []

for i in range(1000):
    pair = []
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    pair.append(private_key)
    acct = Account.from_key(private_key)
    pair.append(acct.address)
    address.append(pair)

df = pandas.DataFrame(address, columns=['private', 'public'])
df.to_csv("ethereum_wallet.csv", index=False)

