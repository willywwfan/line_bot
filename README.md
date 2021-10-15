# line_bot

Line Bot

ngrok
ngrok authtoken 1zV9ZnkcPpIp7sHglB2kufSqRSs_7Ts3k3x2RVzmftbzsZzvc
ngrok http 8000

paste to settings.py
ALLOWED_HOSTS = [
    '5b25-36-234-32-154.ngrok.io'  #允許的網域名稱
]

paste to Line Developers Messaging API Webhook settings
https://5b25-36-234-32-154.ngrok.io/WillyFanBot/callback

runserver
C:\Users\socrateschch\Documents\src\line_bot\mylinebot>
py -3.8 manage.py runserver

Verify
