import json
import yaml
import requests
from requests.exceptions import HTTPError
import logging
import structlog
    
def http_json_call(url):
  try:
    r = requests.get(url)
    r.raise_for_status()
  except HTTPError as http_err:
     if r.content is not None:
      raise Exception(f'HTTP error occurred: {http_err}: {r.content}')  # Python 3.6
     else:
       raise Exception(f'HTTP error occurred: {http_err}')
  except Exception as err:
    raise Exception(f'Other error occurred: {err}')  # Python 3.6
  else:
    return json.loads(r.content)

def read_config_file(file_path):
  """Read and Make sure field are present

  Args:
    file_path: path to the config file
  Returns:
    A Tuple (a message and the config if all good)
  """
  try:
    with open(file_path, "r") as f:
      config_data = yaml.safe_load(f)
  except Exception:
    raise


  # validate the contents of the configuration file
  if ('networks' not in config_data or 
      not isinstance(config_data['networks'], list)):
    return 'Error: Invalid configuration file: networks should be a list', None

  for network in config_data['networks']:
    if 'name' not in network:
      return f'Error: no "name" in {network["name"]}', False
    if 'rpc' not in network:
      return f'Error: no "rpc" in {network["name"]}', False
    if 'api' not in network:
      return f'Error: no "api" in {network["name"]}', False
    if 'decimals' not in network:
      return f'Error: no "decimals" in {network["name"]}', False
    if 'denom' not in network:
      return f'Error: no "denom" in {network["name"]}', False
    if 'symbol' not in network:
      return f'Error: no "symbols" in {network["name"]}', False
    if 'type' not in network:
      return f'Error: no "type" in {network["name"]}', False

    if 'wallets' not in network or not isinstance(network['wallets'], list):
      return f'Error: Invalid configuration file:\
{network["name"]} should have a wallets as a list', False

    for wallet in network['wallets']:
      if 'name' not in wallet or 'address' not in wallet:
        return f'Error: Invalid {network["name"]} wallet configuration \
either name and/or address are missing', False
  return 'Configuration file validation successful', config_data

def configure_logging(format, level):
  """Configure logging for a Python program using the structlog framework.

  Args:
    format: The format of the log messages. Can be `json` or `text`.
    level: The log level. Can be `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`.

  Returns:
    A logging configuration object.
  """

  processorrender=""
  if format == "json":
    processorrender=structlog.processors.JSONRenderer()
  else:
    processorrender=structlog.dev.ConsoleRenderer()

  loglevel = logging.getLevelName(level)
  structlog.configure(processors=[
    structlog.contextvars.merge_contextvars,
    structlog.processors.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
    structlog.processors.UnicodeDecoder(),
    structlog.processors.TimeStamper(fmt='iso',utc=True),
    processorrender],
    wrapper_class=structlog.make_filtering_bound_logger(loglevel),
    cache_logger_on_first_use=True)

  logger = structlog.getLogger()

  return logger

