import json
import traceback
import urllib.request
import urllib.error

payload = {
    'method': 'AIA* (A-Estrela Limitada)',
    'origem': '7,0',
    'destino': '1,4',
    'mapId': 0,
    'limite': 10
}

req = urllib.request.Request(
    'http://127.0.0.1:5000/run',
    data=json.dumps(payload).encode(),
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req, timeout=20) as r:
        print(r.status)
        print(r.read().decode())
except urllib.error.HTTPError as e:
    print('STATUS', e.code)
    print(e.read().decode())
except Exception as e:
    print(type(e).__name__, e)
    print('---')
    traceback.print_exc()
