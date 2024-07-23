"""Application exporter"""

import os
import time
from prometheus_client import start_http_server, Gauge, Counter
import argparse
from dotenv import load_dotenv
from utils import read_config_file, configure_logging
from cosmos import (
    get_maincoin_balance,
    get_delegations,
    get_unbonding_delegations,
    get_rewards,
)
from metrics_enum import MetricsAccountInfo


class AppMetrics:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    application metrics into Prometheus metrics.
    """

    def __init__(self, polling_interval_seconds=60, walletconfig=False, logging=False):
        self.polling_interval_seconds = polling_interval_seconds

        self.logging = logging
        self.logging.info("Init the Appmetrics class")
        self.walletconfig = walletconfig

        # all metrics are defined below
        self.account_info = Gauge(
            "account_info",
            "account information",
            ["address", "name", "network", "type"],
        )
        self.rpc_call_status_counter = Counter(
            "rpc_call_status",
            "Count the number of success or failed http call for a given url",
            ["url", "status"],
        )

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

        for network in self.walletconfig["networks"]:
            self.logging.debug(network)
            networkname = network["name"]
            for wallet in network["wallets"]:
                try:
                    self.logging.info(f"Fetching {wallet['address']}")
                    balance = float(
                        get_maincoin_balance(
                            network["api"],
                            wallet["address"],
                            network["denom"],
                            self.rpc_call_status_counter,
                        )
                    ) / (10 ** network["decimals"])
                    self.logging.info(
                        f"{wallet['address']} has {balance} {network['symbol']}"
                    )

                    self.account_info.labels(
                        network=networkname,
                        address=wallet["address"],
                        name=wallet["name"],
                        type=MetricsAccountInfo.BALANCE.value,
                    ).set(balance)

                    delegations = float(
                        get_delegations(
                            network["api"],
                            wallet["address"],
                            network["denom"],
                            self.rpc_call_status_counter,
                        )
                    ) / (10 ** network["decimals"])
                    self.logging.info(
                        f"{wallet['address']} has {delegations} delegations"
                    )
                    self.account_info.labels(
                        network=networkname,
                        address=wallet["address"],
                        name=wallet["name"],
                        type=MetricsAccountInfo.DELEGATIONS.value,
                    ).set(delegations)

                    unbounding_delegations = float(
                        get_unbonding_delegations(
                            network["api"],
                            wallet["address"],
                            self.rpc_call_status_counter,
                        )
                    ) / (10 ** network["decimals"])
                    self.logging.info(
                        f"{wallet['address']} has {unbounding_delegations} unbounding delegations"
                    )
                    self.account_info.labels(
                        network=networkname,
                        address=wallet["address"],
                        name=wallet["name"],
                        type=MetricsAccountInfo.UNBOUNDING_DELEGATIONS.value,
                    ).set(unbounding_delegations)

                    rewards = float(
                        get_rewards(
                            network["api"],
                            wallet["address"],
                            network["denom"],
                            self.rpc_call_status_counter,
                        )
                    ) / (10 ** network["decimals"])
                    self.logging.info(f"{wallet['address']} has {rewards} rewards")
                    self.account_info.labels(
                        network=networkname,
                        address=wallet["address"],
                        name=wallet["name"],
                        type=MetricsAccountInfo.REWARDS.value,
                    ).set(rewards)
                except Exception as e:
                    self.logging.error(str(e))


def argsparse():
    parser = argparse.ArgumentParser(description="Wallets Exporter")
    parser.add_argument(
        "-c",
        "--config",
        help="config file in yaml \
                      format, default is config.yaml",
        action="store",
        default="config.yaml",
    )

    parser.add_argument(
        "-lf",
        "--format",
        choices=["json", "txt"],
        help="set the logging format",
        action="store",
        default="txt",
    )

    parser.add_argument(
        "-ll",
        "--level",
        nargs="?",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="set the logging level",
        action="store",
        default="INFO",
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

    messages, walletconfigs = read_config_file(configfile)

    if not walletconfigs:
        log.error(f"config file {configfile} is incorrect, ${messages}")
        exit(1)
    else:
        log.info(messages)

    log.debug(messages)

    log.debug(f"Loading .env")
    load_dotenv()  # take environment variables from .env
    polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "60"))
    exporter_port = int(os.getenv("EXPORTER_PORT", "9877"))

    log.info("Wallet Exporter started and now listening on port " + str(exporter_port))

    app_metrics = AppMetrics(
        polling_interval_seconds=polling_interval_seconds,
        walletconfig=walletconfigs,
        logging=log,
    )
    start_http_server(exporter_port)
    app_metrics.run_metrics_loop()


if __name__ == "__main__":
    main()
