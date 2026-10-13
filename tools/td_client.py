"""Small JSON-RPC client for the local, official TDMCP component."""
import argparse
import json
from pathlib import Path
import urllib.request

URL = "http://127.0.0.1:13316/mcp"

def rpc(method, params=None):
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}
    request = urllib.request.Request(URL, json.dumps(payload).encode(), {
        "Content-Type": "application/json", "Accept": "application/json, text/event-stream"
    })
    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.load(response)
    if "error" in result:
        raise RuntimeError(result["error"])
    return result.get("result", result)

def call(name, arguments=None):
    return rpc("tools/call", {"name": name, "arguments": arguments or {}})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tool")
    parser.add_argument("arguments", nargs="?", default="{}")
    parser.add_argument("--file")
    args = parser.parse_args()
    if args.tool == "list":
        result = rpc("tools/list")
    elif args.file:
        result = call(args.tool, {"code": Path(args.file).read_text(encoding="utf-8")})
    else:
        result = call(args.tool, json.loads(args.arguments))
    if "content" in result:
        for item in result["content"]:
            if item.get("type") == "text":
                output = item['text']
                if args.tool == 'get_help':
                    parsed = json.loads(output)
                    output = '\n'.join(r['opType']+': '+json.dumps({k:v.get('menuNames',v.get('components',v.get('parType'))) for k,v in r.get('parameters',{}).items()}) for r in parsed.get('results',[]))
                print(output.encode('ascii', errors='backslashreplace').decode())
    else:
        print(json.dumps(result, ensure_ascii=True, indent=2))
