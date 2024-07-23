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

> type is currently not used. In the future, it will be used for other chain (ETH, DOT, ...)


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
curl -s localhost:9877/metric

account_info{address="cosmos1gswfh88s88s2evtsutwt8heh59jttjglhdlwtwj",name="validator",network="cosmos", type="balance"} 54.451031
account_info{address="cosmos1r59ugu6w72s88s2evtsutwt8heh59jpqp9mm3ew",name="delegator",network="cosmos", type="balance"} 25600.995009
```
# TODO

- [X] support for cosmos staking (delegated token, undelegated, Staking Reward)
- [X] support for ETH and ERC20 token
- [] support other chain (DOT, AVAX, ...)
- [] create grafana dashboard
