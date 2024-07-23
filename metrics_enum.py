from enum import Enum


class MetricsUrlStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"


class MetricsAccountInfo(Enum):
    BALANCE = "balance"
    DELEGATIONS = "delegations"
    UNBOUNDING_DELEGATIONS = "unbounding_delegations"
    REWARDS = "rewards"
