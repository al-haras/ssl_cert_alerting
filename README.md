## SSL Cert - Notifications
This tool was built because there was a need to receive alerts about expiring SSL certs that we had for various things. This infomation was traditionally stored in Confluence articles but I was able to create a JSON to organize everything in a way that we were able to work with it. This is built to send both a Slack notification and an email via SMTP with a 7 day notice. Any of this can be modified if needed.

### Requirements
This is built using Python 3.7 and `requirements.txt` has the packages needed to be installed via pip (`pip install -r requirements.txt`)

### Configuration
`config_template.py` needs to be modified and changed to `config.py`. This requires you to specify information to authenticate to your SMTP server and where it is supposed to send messages to. Additionally you will need to specify similar parameters for the Slack functions.

### Running the tool
The tool was essentially designed to run once per day. It should be able to be implemented anywhere you want it (cron, docker, etc). A Dockerfile is included to deploy to a container.

### Future Plans
- ?
