# -*- coding: utf-8 -*-

import urllib

params = "https://windard.com"

print urllib.quote(params)
print urllib.quote_plus(params)
print urllib.unquote(urllib.quote(params))
print urllib.unquote_plus(urllib.quote_plus(params))
