# Python client library for warehouse

This library implements basic functionality for interaction with a warehouse instance.

Examples of this includes:

* Searching with natural and normal query languages for bundles and files
* Readout of properties for files and bundles
* Download and upload of files
* Creation of bundles
* Trashing and restoration of bundles and files

## Examples

For a basic demonstration of the library functionality, an interactive mode is included. Make sure the two files `~/.warehouse.apikey` and `~/.warehouse.url` are populated with API key and URL to the warehouse instance, respectively, and launch the interative mode:

```sh
> python -m warehouse

Reading config from ~/.warehouse.url and ~/.warehouse.apikey

Successfully connected to warehouse on https://warehouse.local
A client object named 'c' is available

Try running help(c) for more information

>>>
```

### Searching for bundle and listing of properties

```python
import warehouse as wh

c = wh.Client("https://warehouse.local", wh.ApikeyAuth(APIKEY))

for bundle in c.find_bundles('bundle.version exists', sorting=None, limit=1):
    print(bundle.get_properties())
```
