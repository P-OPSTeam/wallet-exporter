# Wallet Exporter

## Description

wallet balance exporter to monitor your bot, restake account, your operator account and what not ...

## Installation

```bash
cd ~
git clone https://github.com/P-OPSTeam/wallet-exporter.git
sudo apt install software-properties-common -y
sudo apt install python3 python3-virtualenv
cd wallet-exporter
virtualenv -p /usr/bin/python3 .venv
source .venv/bin/activate
curl -sS https://bootstrap.pypa.io/get-pip.py | python3
pip install -r requirements.txt
```

## Edit config.yaml

Supported types of wallet: cosmos, evm, substrate (polkadot for example), solana

For cosmos wallets (celestia for example), the name of the network must match what is in ```https://chains.cosmos.directory```

For evm wallets, if it is an erc20 token, you need to specify the contract address in the field contract_address in the wallet.

Replace the 'API', 'RPC' accordingly (for example, use ```https://moonbeam.public.blastapi.io``` if you use the moonbeam evm)

For berachain wallet, you need to specify the bgt token contract address (see config.yaml as example).

For solana wallets, you need to specify the RPC endpoint (e.g., ```https://api.mainnet-beta.solana.com``` for mainnet or ```https://api.devnet.solana.com``` for devnet).

## Run it

```bash
python exporter.py
```

## As a service

```bash
sudo cp wallet-exporter.service /etc/systemd/system/
sudo sed -i "s:<home>:${HOME}:g" /etc/systemd/system/wallet-exporter.service
sudo sed -i "s/<user>/${USER}/g" /etc/systemd/system/wallet-exporter.service
sudo systemctl daemon-reload 
sudo systemctl enable wallet-exporter
sudo systemctl start wallet-exporter
```

## Test it

```bash
Example
curl -s localhost:9877/metric

account_info{address="cosmos1gswfh88s88s2evtsutwt8heh59jttjglhdlwtwj",name="validator",network="cosmoshub", type="balance"} 54.451031
account_info{address="cosmos1gswfh88s88s2evtsutwt8heh59jttjglhdlwtwj",name="validator",network="cosmoshub", type="delegations"} 0.0
account_info{address="cosmos1gswfh88s88s2evtsutwt8heh59jttjglhdlwtwj",name="validator",network="cosmoshub", type="unbounding_delegations"} 0.0
account_info{address="cosmos1gswfh88s88s2evtsutwt8heh59jttjglhdlwtwj",name="validator",network="cosmoshub", type="rewards"} 0.0
account_info{address="0x95222290DD7278Aa3Ddd389Cc1E1d165CC4BAfe9",name="broadcaster ethereum",network="ethereum",type="balance"} 6.388107948244274
account_info{address="0x95222290DD7278Aa3Ddd389Cc1E1d165CC4BAfe9",name="broadcaster matic",network="ethereum",type="balance"} 0.4753891567500353
account_info{address="1FwzEXsZedfWFPGtJ3Ex8SFLhvugrA9aJN9GL1GeHpYeqf7",name="broadcaster polkadot",network="polkadot",type="balance"} 46000.0

```

## Berachain

For Berachain, there are specific metrics

```bash
Example
curl -s localhost:9877/metric

account_info{address="0x34ae6F60D246ee786a01F4941047fEbe3A4198fA",name="bera validator",network="berachain",type="balance"} 9.554170322670004
account_info{address="0x34ae6F60D246ee786a01F4941047fEbe3A4198fA",name="bera validator",network="berachain",type="boosts"} 8.253249496763132
account_info{address="0x34ae6F60D246ee786a01F4941047fEbe3A4198fA",name="bera validator",network="berachain",type="validator_boostees"} 0.0
account_info{address="0x34ae6F60D246ee786a01F4941047fEbe3A4198fA",name="bera validator",network="berachain",type="unboosted"} 1.0009208259068711
account_info{address="0x34ae6F60D246ee786a01F4941047fEbe3A4198fA",name="bera validator",network="berachain",type="queued_boost"} 0.3

```

The type "boosts" is the amount of BGT used by an account for boosts

The type "validator_boostees" is the amount of BGT attributed to the validator for boosts

The type "unboosted" is the unboosted balance of an account

The type "queued_boost" is the amount of BGT queued up to be used by an account for boosts

## Solana

For Solana wallets, the exporter will track SOL balance:

```bash
Example
curl -s localhost:9877/metric

account_info{address="YourSolanaAddressHere",name="my-solana-wallet",network="solana-mainnet",token="SOL",token_type="native",type="balance"} 12.345678
```

## TODO

- [X] support for cosmos staking (delegated token, undelegated, Staking Reward)
- [X] support for ETH and ERC20 token
- [] support other chain (DOT, AVAX, ...)
- [] create grafana dashboard
