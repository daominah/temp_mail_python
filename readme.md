# Temporary mail

This package provides API to use free disposable mail services.

Now only [10minutemail](https://10minutemail.com/) is available

## API

This server listens HTTP on port 16716 (hard coded).

### [/random-mail](http://127.0.0.1:16716/random-mail) GET

Example response body:

````json
{"mail": "esxeycqfuldznltgyt@nvhrw.com"}
````

### [/last-inbox](http://127.0.0.1:16716/last-inbox) GET

Update per 25 seconds.

Example request:

````
http://127.0.0.1:16716/last-inbox?mail=esxeycqfuldznltgyt@nvhrw.com&subject=dtravel
````

Example response body:
````json
{
    "read": false,
    "expanded": false,
    "forwarded": false,
    "repliedTo": false,
    "sentDate": "2022-09-15T13:55:39.000+00:00",
    "sentDateFormatted": "Sep 15, 2022, 1:55:39 PM",
    "sender": "bounce-md_31225438.63232edb.v1-439628f12f3b42c5bb69edfea5c6d28c@mandrillapp.com",
    "from": "[Ljavax.mail.internet.InternetAddress;@55b52646",
    "subject": "Connect to Dtravel",
    "bodyPreview": "    Dtravel waitlist register email\r\nVerify your e",
    "id": "2067000055726154537",
    "bodyHtmlContent": "..."
}
````

## Dockerfile

````bash
docker build --tag=daominah/temp_mail_python .

docker rm -f temp_mail_python

docker run -dit --restart always --name temp_mail_python \
    -p 16716:16716 -e daominah/temp_mail_python
````

## References

[https://github.com/Nockiro/tenminmailgen](https://github.com/Nockiro/tenminmailgen)
