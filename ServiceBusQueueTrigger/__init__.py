import os
import json
import logging
import azure.functions as func
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from message_templates import *

CHANNEL_ACCESS_TOKEN = os.environ.get("channel_access_token")
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)


def main(msg: func.ServiceBusMessage):
    formatted_msg = format_message(msg)
    logging.info(formatted_msg)
    try:
        line_bot_api.reply_message(formatted_msg["replyToken"], TextMessage(text=formatted_msg["text"]))
    except LineBotApiError:
        logging.info("LineBotApiError")
        line_bot_api.push_message(formatted_msg['userId'], TextMessage(text=formatted_msg["text"]))
    return

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
    # formatted_json = {
    #     "user_id": msg_json.get("userId"),
    #     "message_type": msg_json.get("message", {}).get("type"),
    #     "message_text": msg_json.get("message", {}).get("text"),
    #     "message_data": msg_json.get("message", {}).get("data")
    # }
    # return formatted_json

# test