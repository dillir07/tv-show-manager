from jsontraverse.parser import JsonTraverseParser
import urllib.request
x = None
with urllib.request.urlopen("https://api.tvmaze.com/shows/27436/seasons") as f:
    x = JsonTraverseParser(f.read().decode())
print(x)
