# COVID19_BOT
A python script when run will scans the official Government website and throws notifications to Slack when new cases arise (Ministry of Health and Family Welfare)
- You need a Slack account + Slack Webhook to send slack notifications to your account
- Install dependencies by running
```bash
pip install tabulate
pip install requests
pip install beautifulsoup4
pip install -r requirements.txt
```
## Creating  SLackWebHookUrl
- Create a Slack account
- Create a Workspace
- Go to settings via your app's management dashboard
- From here select the Incoming Webhooks feature, and click the Activate Incoming Webhooks toggle to switch it on.
- Go ahead and pick a channel that the app will post to, and then click to Authorize your app.
- You'll get a new field named webhookURL
### Post your CustomWebhookUrl in auth.py
```python
DEFAULT_WEBHOOK_URL = "https://hooks.slack.com/services/{Custom_webhook_URL}"
```
