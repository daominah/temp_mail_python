import base64
import datetime
import json
import random
import time

from flask import Flask
from flask import request

import tenminutemail

app = Flask(__name__)


@app.route('/', methods=['GET'])
def handleIndex():
    return """<html>
<head><title>Temporary mail</title></head>
<body>
    Read readme.md. APIs: "/random-mail", "/last-inbox"
</body>
</html>"""


@app.route('/random-mail', methods=['GET'])
def handleRandomMail():
    randomMail = ""
    if len(tenminutemail.GlobalInboxes) > 0:
        randomMail = random.choice(list(tenminutemail.GlobalInboxes.keys()))
    return {"Mail": randomMail}


@app.route('/last-inbox', methods=['GET'])
def handleSolve2():
    # ret = {
    #     "read": False,
    #     "expanded": False,
    #     "forwarded": False,
    #     "repliedTo": False,
    #     "sentDate": "2022-09-15T13:55:39.000+00:00",
    #     "sentDateFormatted": "Sep 15, 2022, 1:55:39 PM",
    #     "sender": "bounce-md_31225438.63232edb.v1-439628f12f3b42c5bb69edfea5c6d28c@mandrillapp.com",
    #     "from": "[Ljavax.mail.internet.InternetAddress;@55b52646",
    #     "subject": "Connect to Dtravel",
    #     "bodyPreview": "    Dtravel waitlist register email\r\nVerify your e",
    #     "id": "2067000055726154537",
    #     "bodyHtmlContent": "<!DOCTYPE html><html><body>Just an example</body></html>",
    # }
    mail = request.args.get('mail')
    subject = request.args.get('subject')
    print("request mail: %s, subject: %s" % (mail, subject))
    ret = {}
    try:
        inbox = tenminutemail.GlobalInboxes[mail]
    except Exception as err:
        ret["IsMailNotFound"] = "maybe expired mail"
        return ret
    for mail in inbox:
        if subject in mail["subject"]:
            ret = mail
            return ret
    return ret


if __name__ == '__main__':
    for i in range(10):
        time.sleep(2)
        tenminutemail.MailerThread()

    print("_" * 80)
    print("listening http://127.0.0.1:16716/random-mail")
    print("listening http://127.0.0.1:16716/last-inbox?mail=&subject=")
    print("_" * 80)
    app.run(port=16716, host="0.0.0.0")
