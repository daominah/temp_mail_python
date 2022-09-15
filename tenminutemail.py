import datetime
import urllib
import urllib.request
import time
import json
from threading import Thread

FAKE_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}


class TenMinuteMailer(object):
    """generates 10 minute mails from 10minutemail.com"""

    def __init__(self):
        self.SIDCookie = ""

    def get10MinuteMail(self, simulate=False):
        """gets a new email adress of 10minutemail
        *Returns*: email address"""
        if simulate != True:
            req = urllib.request.Request(
                "https://10minutemail.com/session/address",
                headers=FAKE_REQUEST_HEADERS,
            )
            # req.set_proxy("127.0.0.1:24001", "http")
            # print("debug req:", req.__dict__)

            with urllib.request.urlopen(req) as response:
                jsonResponse = response.read().decode("utf-8")
                self.SIDCookie = response.info().get_all("Set-Cookie")[0]

                return json.loads(jsonResponse)["address"]
        else:
            self.SIDCookie = (
                "JSESSIONID=LIKd7IlHq0lhpTOsWJdPY; path=/; secure; HttpOnly"
            )
            return "r446338@mvrht.net"

    def anyNewMessage(self, currentMessageCount):
        """waits/checks for new messages as long as necessary
        currentMessageCount: The current count of messages the new count of messages shall be compared with
        *Returns*: new message count as int"""

        totalPointCount = 3
        pointCount = 1
        totalWaitTime = 0

        while True:
            messageCount = json.loads(self.doApiRequest("messages/messageCount"))[
                "messageCount"]

            if messageCount > currentMessageCount:
                print("\n> You got new mail! " + str(messageCount))
                break
            else:
                print(
                    "> Waiting for new mails.. currently "
                    + str(messageCount)
                    + " messages"
                    + ("." * pointCount)
                    + (" " * (totalPointCount - pointCount))
                    + "\r",
                    end="",
                    flush=True,
                )

            time.sleep(10)
            totalWaitTime += 10

            if totalWaitTime > 500:
                print("> 500 seconds over.. requesting extension.")
                self.renewInterval()
                totalWaitTime = 0

            # reset point count so we can get a smooth "animation"
            if pointCount >= totalPointCount:
                pointCount = 1
            else:
                pointCount += 1

        return int(messageCount)

    def getMessagesAfter(self, messageID):
        """get message with given ID and return a json object with mail parameters
        messageID: Message to load
        *Returns*: message as json object"""

        print("getting messageID ", str(messageID))
        message = self.doApiRequest(
            "messages/messagesAfter/{0}".format(messageID), True)

        # example:
        # [{"read":false,"expanded":false,"forwarded":false,"repliedTo":false,"sentDate":"2022-06-19T20:37:33.000+00:00","sentDateFormatted":"Jun 19, 2022, 8:37:33 PM","sender":"sender@mail.de","from":"[Ljavax.mail.internet.InternetAddress;@1dd3705c","subject":"Test-Mail","bodyPlainText":"\r\n\r\n\r\nDies ist eine Test-Mail - Yay.\r\n","bodyHtmlContent":"<html>\r\n  <head>\r\n\r\n    <meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\">\r\n  </head>\r\n  <body>\r\n    <p><br>\r\n    </p>\r\n  Dies ist eine Test-Mail - Yay.<br>\r\n    </div>\r\n</div>\r\n  </body>\r\n</html>\r\n","bodyPreview":"\r\n\r\n\r\n-------- Forwarded Message --------\r\nSubject","id":"10123386541204271300"}]
        return json.loads(message)

    def showMessage(self, json):
        mailText = json[0]["bodyPlainText"]

        if mailText == None:
            mailText = json[0]["bodyHtmlContent"]

        return (
            "Sender: "
            + json[0]["sender"]
            + "\nSubject: "
            + json[0]["subject"]
            + "\nMessage: "
            + mailText
            + "\n"
        )

    def renewInterval(self):
        """requests another 10 minutes to keep the mail address active"""
        print("Sending renewal request..")
        return self.doApiRequest("session/reset", True)

    def doApiRequest(self, apiEndpoint: str, printOkay: bool = False):
        req = urllib.request.Request(
            "https://10minutemail.com/" + apiEndpoint, headers=FAKE_REQUEST_HEADERS
        )
        req.add_header("Accept", "application/json, text/javascript, */*")
        req.add_header("Connection", "keep-alive")

        if self.SIDCookie != "":
            req.add_header("cookie", self.SIDCookie)

        with urllib.request.urlopen(req) as response:
            message = response.read().decode("utf-8")

        if printOkay and response.getcode() == 200:
            print("request successful")

        if response.getcode() >= 400:
            print("something went wrong")

        return message


# if __name__ == "__main__":
#
#     mailer = TenMinuteMailer()
#     email0 = mailer.get10MinuteMail()
#     print("> generated email0: " + email0)
#
#     messageId = 0
#     while True:
#         try:
#             mails = mailer.getMessagesAfter(mailer.anyNewMessage(messageId) - 1)
#             messageId += len(mails)
#         except Exception as err:
#             print("error:", err)
#             continue
#         if len(mails) > 0:
#             mail = mails[0]
#             mailBody = mail["bodyHtmlContent"]
#             del (mail["bodyPlainText"])
#             del (mail["bodyHtmlContent"])
#             beauty = json.dumps(mail, indent=4)
#             print(beauty)
#             print(mailBody)


GlobalInboxes = {}


class MailerThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()

        self.lastRefresh = time.time()
        self.mail = ""
        self.mailer = None
        self.msgCount = 0

    def run(self):
        i = -1
        while True:
            i += 1
            if i > 0:
                time.sleep(25)

            if i == 0 or time.time() - self.lastRefresh > 600:  # 10 minutes
                print("begin init TenMinuteMailer i", i)
                self.lastRefresh = time.time()
                self.mail = ""
                self.mailer = None
                self.msgCount = 0
                try:
                    del (GlobalInboxes[self.mail])
                except Exception:
                    pass

                try:
                    self.mailer = TenMinuteMailer()
                    self.mail = self.mailer.get10MinuteMail()
                    GlobalInboxes[self.mail] = []
                    print("ok init TenMinuteMailer:", self.mail)
                except Exception as err:
                    print("error init TenMinuteMailer:", err)
                    continue

            if self.mailer is not None:
                # print(datetime.datetime.now().isoformat(), "begin check new inbox i", i)
                webMsgCount = json.loads(self.mailer.doApiRequest("messages/messageCount"))[
                    "messageCount"]
                if webMsgCount <= self.msgCount:
                    continue
                newMails = self.mailer.getMessagesAfter(self.msgCount)
                self.msgCount += len(newMails)
                if len(newMails) > 0:
                    print("received new mails:", len(newMails))
                    for mail in newMails:
                        del (mail["bodyPlainText"])
                        GlobalInboxes[self.mail].insert(0, mail)
                        print("_" * 80)
                        print("_" * 80)
                        print("subject:", mail["subject"])
                        print("bodyHtmlContent:", mail["bodyHtmlContent"])
                        print("_" * 80)
                        print("_" * 80)
                # print("end check new inbox i", i)


if __name__ == "__main__":
    MailerThread()
    while True:
        time.sleep(10)
