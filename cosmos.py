from utils import http_json_call

def get_coins_balances(restprovider, addr: str, rpc_call_status_counter):
  d = ""
  coins = {}
  try:
    d = http_json_call(url=f'{restprovider}/cosmos/bank/v1beta1/balances/{addr}', rpc_call_status_counter=rpc_call_status_counter)
    if "balances" in str(d):
      for i in d["balances"]:
          coins[i["denom"]] = i["amount"]
      return coins
    else:
      return 0
  except Exception as addr_balancer_err:
    raise(addr_balancer_err)

def get_maincoin_balance(apiprovider, addr: str, maindenom, rpc_call_status_counter):
  d = ""
  try:
    d = http_json_call(url=f'{apiprovider}/cosmos/bank/v1beta1/balances/{addr}', rpc_call_status_counter=rpc_call_status_counter)
    if "balances" in str(d):
      for i in d["balances"]:
        if i["denom"] == maindenom:
          return i["amount"]
    else:
      return 0
  except Exception as addr_balancer_err:
    raise(addr_balancer_err)