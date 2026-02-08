import sys
import os
import time
import urllib.request
import urllib.error

HOST = "nginx"
PORT_HTML = 8080
PORT_ERR = 8081
EXPECTED_HTML_SUBSTRING = "Hi! nice to meet you"


def http_get(port):
    url = f"http://{HOST}:{port}/"
    req = urllib.request.Request(url, method="GET")
    try:
        resp = urllib.request.urlopen(url)
        body = resp.read().decode("utf-8")
        return resp.status, body
        
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore") if e.fp else ""
        return e.code, body
    


def wait_for_port(port):
    url = f"http://{HOST}:{port}/"
    
    for i in range(20):
        try:
            urllib.request.urlopen(url)
            break
        except urllib.error.HTTPError: 
            # If the request gets 503 and its the error port, its OK
            if port == PORT_ERR:
                break
        except Exception:
            time.sleep(0.5)
    else:
        print(f"{HOST}:{port} not reachable")



def main():
    HTML_Failed = 0
    PORT_Failed = 0

    # Wait for nginx ports to be reachable 
    wait_for_port(PORT_HTML)
    wait_for_port(PORT_ERR)
    
    # Test the custom HTML server
    status, body = http_get(PORT_HTML)
    
    if status != 200:
        HTML_Failed = 1
        print(f"HTML server expected 200, got {status}")
        
    if EXPECTED_HTML_SUBSTRING not in body:
        HTML_Failed = 1
        print(f"HTML server body missing expected substring: {EXPECTED_HTML_SUBSTRING}")

    # Test the error server 
    status, _ = http_get(PORT_ERR)
    
    if status != 503:
        PORT_Failed = 1
        print(f"Error server expected 503, got {status}")

    if HTML_Failed == 0 and PORT_Failed == 0:
        print("OK: all tests passed")
        sys.exit(0)
    else:
        if HTML_Failed == 1:
            print("ERROR: the HTML test failed")
        else:
            print("ERROR: the 503 nginx server test failed")
        sys.exit(1)

    


if __name__ == "__main__":
    main()
