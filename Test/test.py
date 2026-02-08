import sys
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor
import ssl


HOST = "nginx"
PORT_HTML = 8080
PORT_ERR = 8081
EXPECTED_HTML_SUBSTRING = "Hi! nice to meet you"


def http_get(port, ctx):
    url = f"https://{HOST}:{port}/"

    try:
        resp = urllib.request.urlopen(url, context=ctx)
        body = resp.read().decode("utf-8")
        return resp.status, body
        
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore") if e.fp else ""
        return e.code, body
    


def wait_for_port(port, ctx):
    url = f"https://{HOST}:{port}/"
    
    for _ in range(20):
        try:
            urllib.request.urlopen(url, context=ctx)
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

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # Wait for nginx ports to be reachable 
    wait_for_port(PORT_HTML, ctx)
    wait_for_port(PORT_ERR, ctx)
    
    # Test the custom HTML server
    status, body = http_get(PORT_HTML, ctx)
    
    if status != 200:
        HTML_Failed = 1
        print(f"HTML server expected 200, got {status}")
        
    if EXPECTED_HTML_SUBSTRING not in body:
        HTML_Failed = 1
        print(f"HTML server body missing expected substring: {EXPECTED_HTML_SUBSTRING}")

    # Test the error server 
    status, _ = http_get(PORT_ERR, ctx)
    
    if status != 503:
        PORT_Failed = 1
        print(f"Error server expected 503, got {status}")

    # Test rate limit
    def hit(port):
        return http_get(port, ctx)[0] # returns only status code

    # Runs 10 threads that sends a request at the same time
    with ThreadPoolExecutor(max_workers=10) as pool:
        codes = list(pool.map(lambda _: hit(PORT_HTML), range(10)))

    if 429 not in codes:
        HTML_Failed = 1
        print("ERROR: rate limit not working on HTML server")


    if HTML_Failed == 0 and PORT_Failed == 0:
        print("\nOK: all tests passed")
        sys.exit(0)
    else:
        if HTML_Failed == 1:
            print("\nERROR: ome tests failed on the HTML test")
        else:
            print("\nERROR: some tests failed on the 503 nginx server")
        sys.exit(1)

    


if __name__ == "__main__":
    main()
