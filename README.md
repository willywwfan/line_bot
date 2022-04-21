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

AWS solution

1. package the python file to .zip
2. set lambda_function.py to lambda in AWS (us-east-2)


Heroku postgresql connect with aws lambda

https://github.com/jkehler/awslambda-psycopg2
download the psycopg2-3.8 and rename as psycopg2, put into python before it compress.
(PostgreSQL and psycopg2 build file)(with_ssl_support)

Verify

# reference:
https://www.ecloudture.com/deploy-line-chatbot-using-aws-lambda-1/
https://github.com/jkehler/awslambda-psycopg2
