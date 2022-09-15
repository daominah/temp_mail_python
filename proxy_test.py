import ssl
import urllib.request

import user_agents

urllib.request.install_opener(
    urllib.request.build_opener(urllib.request.HTTPHandler(debuglevel=1)))


def main():
    url0 = "https://ipinfo.io/ip"
    # url0 = "https://ipv4.icanhazip.com"
    # url0 = "http://103.74.123.67:20891/"
    headers = {
        user_agents.HeaderKeyUserAgent: user_agents.GetRandomUserAgent(),
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "text/html,application/json,application/xml",
    }

    req = urllib.request.Request(url0, headers=headers)
    # req.set_proxy("127.0.0.1:24003", "http")

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        response = urllib.request.urlopen(req, context=ctx)
    except Exception as err:
        print("error urllib.request.urlopen:", err)
        return

    responseBody = response.read().decode("utf-8")
    response.close()
    print("responseBody:", responseBody)

    print("returned normally")


if __name__ == "__main__":
    main()
