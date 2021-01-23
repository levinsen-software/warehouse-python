"""__main__ module"""

import rlcompleter
import sys
import os
import code
import readline

import warehouse as wh

print('Reading config from ~/.warehouse.url and ~/.warehouse.apikey')
try:
    warehouse_apikey = open(os.path.expanduser(
        '~/.warehouse.apikey')).read().strip()
    warehouse_url = open(os.path.expanduser('~/.warehouse.url')).read().strip()
    print()
except (FileNotFoundError, PermissionError) as e:
    print(e)
    sys.exit(1)

# urllib3 *will* warn about insecure HTTPS
# verify is set to False as the intention of this tool
# is solely to demonstrate the python library.
#
# Always use certificate validation in production.
c = wh.Client(warehouse_url, wh.ApikeyAuth(warehouse_apikey), verify=False)

# Check that the provided API Key is valid
try:
    c.check_token()
except wh.WarehouseClientException as e:
    print("Error connecting to warehouse: %s" % e)
    sys.exit(1)

print()
print("Successfully connected to warehouse on %s" % warehouse_url)
print("A client object named 'c' is available")
print()
print("Try running help(c) for more information")
print()

global_vars = globals()
global_vars.update(locals())

readline.set_completer(rlcompleter.Completer(global_vars).complete)
readline.parse_and_bind("tab: complete")
code.InteractiveConsole(global_vars).interact()
