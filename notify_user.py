import sys
import os
import smtplib
from flask import Flask,request
from email.mime.text import MIMEText
from flask_cors import CORS, cross_origin
from configparser import SafeConfigParser
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

parser = SafeConfigParser()
parser.read('config.ini')

MAIL_SERVER = "localhost.cs.indiana.edu"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = "rentnleaseservice@gmail.com"
MAIL_PASSWORD = "rentnlease#2019"      
MAIL_DEFAULT_SENDER = "rentnleaseservice@gmail.com"

app = Flask(__name__)

app.config["MAIL_SERVER"] = MAIL_SERVER
app.config["MAIL_PORT"] = MAIL_PORT
app.config["MAIL_USE_SSL"] = MAIL_USE_SSL
app.config['MAIL_USE_TLS'] = False
app.config["MAIL_DEFAULT_SENDER"] = MAIL_DEFAULT_SENDER

@app.route('/notify', methods=['POST'])
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def sendEmail():
    try:
        post_data = request.get_json()
        recipient = post_data.get('recipient')
        subject = post_data.get('subject')
        body = post_data.get('body')
        sender = MAIL_USERNAME
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'], msg['To'] = sender, recipient
        # Send the message via gmail SMTP server
        s = smtplib.SMTP('smtp.gmail.com', 587)
        #connect to the gmail server
        s.ehlo()
        s.starttls()
        s.login(MAIL_USERNAME, MAIL_PASSWORD)
        #TODO: make it parse email and pass from config.ini?
        s.sendmail(MAIL_USERNAME, recipient, msg.as_string())
        s.quit()
        return "Mail sent Successfully"
    except Exception as e:
        app.logger.error(e)

@app.route('/test', methods=['GET'])
def test():
    return "Hello, World!"


if __name__ == '__main__':
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5001)
    IOLoop.instance().start()
