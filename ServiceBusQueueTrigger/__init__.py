import os
import json
import logging
import azure.functions as func
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from message_templates import *

KEY_VAULT_NAME = os.environ.get("KEY_VAULT_NAME")


def main(msg: func.ServiceBusMessage):
    formatted_msg = format_message(msg)
    logging.info(formatted_msg)  # print formatted message
    channel_access_token = get_channel_access_token(f"token{formatted_msg['channelid']}")
    line_bot_api = LineBotApi(channel_access_token)
    try:
        line_bot_api.reply_message(formatted_msg["replyToken"], format_text(formatted_msg["text"]))
    except LineBotApiError:
        logging.info("Reply token expired")
        line_bot_api.push_message(formatted_msg['userId'], format_text(formatted_msg["text"]))
    return

    # send different messages based on type

    # user_id = formatted_msg["user_id"]
    # message_type = formatted_msg["message_type"]
    # if message_type == "welcome":
    #     message = TextMessage(text=formatted_msg["message_text"])
    #     menu = create_menu(formatted_msg["message_data"])
    #     line_bot_api.push_message(user_id, [message, menu])
    # elif message_type == "job_listings":
    #     job_listings = create_job_listings(formatted_msg["message_data"])
    #     line_bot_api.push_message(user_id, job_listings)
    # elif message_type == "job_applications":
    #     job_applications = create_job_applications(formatted_msg["message_data"])
    #     line_bot_api.push_message(user_id, job_applications)
    # else:
    #     message = TextMessage(text="Some other message type")
    #     line_bot_api.push_message(user_id, message)


def format_message(msg):
    msg_str = msg.get_body().decode('utf-8')
    msg_json = json.loads(msg_str)
    return msg_json  # testing

    # format json to pass into message templates

    # formatted_json = {
    #     "user_id": msg_json.get("userId"),
    #     "message_type": msg_json.get("message", {}).get("type"),
    #     "message_text": msg_json.get("message", {}).get("text"),
    #     "message_data": msg_json.get("message", {}).get("data")
    # }
    # return formatted_json


def format_text(text):
    messages = text.split("\\n")  # set which character to split by
    formatted_messages = []
    # append back of messages together if exceed 5 messages
    if len(messages) > 5:
        s = "\n".join(messages[4:])
        messages = messages[:4]
        messages.append(s)
    # create messages
    for message in messages:
        # check if message is "" or " "
        if message != " " and message:
            formatted_messages.append(TextMessage(text=message))
    logging.info(formatted_messages)
    return formatted_messages


def get_channel_access_token(channel_id):
    KVUri = f"https://{KEY_VAULT_NAME}.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KVUri, credential=credential)
    return client.get_secret(channel_id).value
