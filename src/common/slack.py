import os

from slack_sdk import WebClient

SLACK_USER_TOKEN = os.environ["SLACK_USER_TOKEN"]
INBOX_CHANNEL = "C05GUTE35RU"  # inboxのチャンネルID


def post_to_dm(query: str) -> None:
    client = WebClient(token=SLACK_USER_TOKEN)
    client.chat_postMessage(channel=INBOX_CHANNEL, text=query)
