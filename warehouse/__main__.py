"""__main__ module"""

import rlcompleter
import sys
import os
import code
import readline

import warehouse as wh

sys.stdout.write(
    'Trying to read config from ~/warehouse.url and ~/.warehouse.apikey.. ')
try:
    warehouse_apikey = open(os.path.expanduser(
        '~/.warehouse.apikey')).read().strip()
    warehouse_url = open(os.path.expanduser('~/.warehouse.url')).read().strip()
    print('OK')
    print()
except (FileNotFoundError, PermissionError):
    print('ERROR')
    sys.exit(1)

c = wh.Client(warehouse_url, wh.ApikeyAuth(warehouse_apikey))

# Check that the provided API Key is valid
try:
    c.check_token()
except wh.WarehouseClientException as e:
    print("error connecting to warehouse: %s", e)

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
