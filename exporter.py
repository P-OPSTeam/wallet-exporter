"""Application exporter"""

import os
import time
from prometheus_client import start_http_server, Gauge, Enum
from datetime import datetime
import argparse
from dotenv import load_dotenv
import traceback
from utils import read_config_file, configure_logging
from cosmos import get_maincoin_balance

class AppMetrics:
  """
  Representation of Prometheus metrics and loop to fetch and transform
  application metrics into Prometheus metrics.
  """

  def __init__(self, polling_interval_seconds=15, walletconfig=False, logging=False):
    self.polling_interval_seconds = polling_interval_seconds

    self.logging = logging
    self.logging.info("Init the Appmetrics class")
    self.walletconfig=walletconfig

    # all metrics are defined below
    self.account_balance = Gauge("account_balance", "account balance", ["address", "name", "network"])

    logging.debug(walletconfig)

  def run_metrics_loop(self):
    """Metrics fetching loop"""

    while True:
      self.fetch()
      time.sleep(self.polling_interval_seconds)

  def fetch(self):
    """
    Get metrics from application and refresh Prometheus metrics with
    new values.
    """

    self.logging.info("Fetching wallet balances")

    try:
      for network in self.walletconfig["networks"]:
        self.logging.debug(network)
        networkname=network["name"]
        for wallet in network["wallets"]:
          self.logging.info(f"Fetching {wallet['address']}")
          balance=float(get_maincoin_balance(network["api"], 
                  wallet['address'], 
                  network['denom'])) / (10 ** network['decimals'])
          self.logging.info(f"{wallet['address']} has {balance} {network['symbol']}")
          
          self.account_balance.labels(network=networkname, address=wallet['address'],name=wallet['name']).set(balance)
    except Exception as e:
      self.logging.error(str(e))

def argsparse():
  parser = argparse.ArgumentParser(description="Wallets Exporter")
  parser.add_argument( "-c", "--config", help="config file in yaml \
                      format, default is config.yaml",
                      action="store", default="config.yaml")

  parser.add_argument(
    "-lf", "--format", choices=["json", "txt"], 
    help="set the logging format", action="store", default="txt"
  )

  parser.add_argument(
    "-ll", "--level", nargs="?", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], 
    help="set the logging level", action="store", default="INFO"
  )

  args = parser.parse_args()
  return args
          
def main():
  """Main entry point"""

  args = argsparse()
  configfile = args.config
  loglevel = args.level
  logformat = args.format

  log = configure_logging(logformat, loglevel)

  log.debug(f"Argsparse {args}")

  messages, walletconfigs=read_config_file(configfile)
  
  if not walletconfigs:
    log.error(f"config file {configfile} is incorrect, ${messages}")
    exit(1)
  else:
    log.info(messages)
  
  log.debug(messages)
 
  log.debug(f"Loading .env")
  load_dotenv() # take environment variables from .env
  polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "15"))
  exporter_port = int(os.getenv("EXPORTER_PORT", "9877"))

  log.info("Wallet Exporter started and now listening on port " + str(exporter_port))

  app_metrics = AppMetrics(
    polling_interval_seconds=polling_interval_seconds,
    walletconfig=walletconfigs,
    logging=log
  )
  start_http_server(exporter_port)
  app_metrics.run_metrics_loop()

if __name__ == "__main__":
  main()
