from datetime import date
import datetime
import json
import smtplib
import config
import sys
import slack

# JSON Path Variable
path = "certs.json"


# Get Week Notice
def week_notice():
    week = date.today()
    notice = str(week - datetime.timedelta(days=-7))
    return notice


# Read JSON with cert information
def read_json(json_path):
    with open(json_path, 'r') as cert_json:
        data=cert_json.read()
        cert_json.close
        json_data = json.loads(data)['certs']
        return json_data


# Formats email with 7 day warning
def check_if_week(json_week, val_week):
    for certs in json_week:
        if val_week == certs['exp_date']:
            return True


# Formats email for 7 day warning
def format_message_week_notice(json_email_week,date_week):
    for certs in json_email_week:
        if date_week == certs['exp_date']:
            message = """From: """ + config.sender_email + \
                      """\nTo: """ + config.receiver_email + \
                      """\nSubject: """ + certs['domain'] + """ - SSL Certificate Expires in 7 Days - Test\n
The Following SSL Cert is going to expire a week from now.\n \
Domain: """ + certs['domain'] + """\n \
Exp Date: """ + certs['exp_date'] + """\n \
Certificate Type: """ + certs['certificate'] + """\n \
Issuer: """ + certs['issuer'] + """\n \
Purpose: """ + certs['purpose']
            return message


# Format slack message
def format_slack_week_notice(json_slack, notice_week):
    for certs in json_slack:
        if notice_week == certs['exp_date']:
            slack_message = "<!channel> The following SSL cert will expire in 7 days" + \
                            "\n```Domain: " + certs['domain'] + \
                            "\nExp Date: " + certs['exp_date'] + \
                            "\nCertificate: " + certs['certificate'] + \
                            "\nIssuer:" + certs['issuer'] + \
                            "\nPurpose: " + certs['purpose'] + "```"
            return slack_message


# Send email generated via
def send_email(formatted_msg):
    mailserver = smtplib.SMTP(config.smtp_server, config.smtp_port)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.login(config.sender_email, config.password)
    mailserver.sendmail(config.sender_email, config.receiver_email, formatted_msg)
    mailserver.quit()


# Post message from format_slack_week_notice function to slack Channel specified in config.py
def post_slack(formatted_slack):
    client = slack.WebClient(token=config.slack_oauth_token)
    client.chat_postMessage(
        channel=config.slack_channel,
        text=formatted_slack)


# Main Function
def main():
    if check_if_week(read_json(path), week_notice()):
        send_email(format_message_week_notice(read_json(path), week_notice()))
        post_slack(format_slack_week_notice(read_json(path), week_notice()))
        sys.exit()
    else:
        sys.exit()


# Call Main
main()
