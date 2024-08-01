# Wallet Exporter

## Description

wallet balance exporter to monitor your bot, restake account, your operator account and what not ...

## Installation

```
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

Supported types of wallet: cosmos, evm, substrate (polkadot for example)

For cosmos wallets (celestia for example), the name of the network must match what is in https://chains.cosmos.directory

For evm wallets, if it is an erc20 token, you need to specify the contract address in the field contract_address in the wallet.

## Run it

```
python exporter.py
```

## As a service

```
sudo cp wallet-exporter.service /etc/systemd/system/
sudo sed -i "s:<home>:${HOME}:g" /etc/systemd/system/wallet-exporter.service
sudo sed -i "s/<user>/${USER}/g" /etc/systemd/system/wallet-exporter.service
sudo systemctl daemon-reload 
sudo systemctl enable wallet-exporter
sudo systemctl start wallet-exporter
```

# Test it

```
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
# TODO

- [X] support for cosmos staking (delegated token, undelegated, Staking Reward)
- [X] support for ETH and ERC20 token
- [] support other chain (DOT, AVAX, ...)
- [] create grafana dashboard
