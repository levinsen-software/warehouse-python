# Python client library for warehouse

This library implements limited functionality for interaction with a warehouse instance. The current functionality includes:

* Searching with natural and normal query languages for bundles and files
* Readout of properties for files and bundles
* Download of files

## Examples


```python
import warehouse as wh

c = wh.Client("https://warehouse.local", wh.ApikeyAuth(APIKEY))

for bundle in c.findBundles('bundle.version exists', None, 1):
    print(bundle.getProperties())
```