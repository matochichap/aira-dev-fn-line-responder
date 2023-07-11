import os
import json
import logging
import requests
import azure.functions as func
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from functions.message_templates import *
from functions.brandfetch_webscraper import *

CAROUSEL_ITEMS_LIMIT = 10
KEY_VAULT_NAME = os.environ.get("KEY_VAULT_NAME")
JOB_DETAILS_ENDPOINT = os.environ.get("JOB_DETAILS_ENDPOINT")
JOB_DETAILS_WEBPAGE = os.environ.get("JOB_DETAILS_WEBPAGE")
KEY_VAULT_NAME = "aira-dev-kv"
JOB_DETAILS_ENDPOINT = "https://aira-dev-fn-line-chatbot.azurewebsites.net/api/jobs/search/"
JOB_DETAILS_WEBPAGE = "https://airadevwebstg.z23.web.core.windows.net/"

PLACEHOLDER_IMG_URL = "https://www.nasco.co.th/wp-content/uploads/2022/06/placeholder.png"


def main(msg: func.ServiceBusMessage):
    global message
    formatted_msg = format_message(msg)
    logging.info(f"FORMATTED MESSAGE: {formatted_msg}")  # print formatted message
    channel_access_token = get_channel_access_token(f"token{formatted_msg['channelId']}")
    line_bot_api = LineBotApi(channel_access_token)
    # append text message to list
    # set limit to 4 for all messages to safely append job listings to messages
    message = format_text(formatted_msg["text"], 4)
    # if searchId is present, add job listings message to the list
    if formatted_msg["type"] == "job_listings":
        message.append(create_job_listings_v4(formatted_msg["job_listings"]))
    try:
        line_bot_api.reply_message(formatted_msg["replyToken"], message)
    except LineBotApiError:
        logging.info("Reply token expired")
        line_bot_api.push_message(formatted_msg['userId'], message)
    return


# convert from fn-chatbot into json
def format_message(msg):
    msg_str = msg.get_body().decode('utf-8')
    msg_json = json.loads(msg_str)
    formatted_json = {
        "channelId": msg_json.get("channelid"),
        "replyToken": msg_json.get("replyToken"),
        "text": msg_json.get("text"),
        "userId": msg_json.get("userId"),
        "type": "text"
    }
    # if searchId not "" use endpoint to get job details
    if msg_json["searchId"]:
        formatted_json["type"] = "job_listings"
        response = requests.get(f"{JOB_DETAILS_ENDPOINT}{msg_json['searchId']}")
        if response.status_code == 200:
            data = response.json()
            # add new job_listings field to formatted json
            formatted_json["job_listings"] = format_data(data, msg_json["searchId"])
    # else return decoded json
    return formatted_json


# format data from endpoint to pass into message templates
# return type: json
def format_data(data, search_id):
    # cycle through colors
    colors = ["#CAD7F2", "#E0A4F4", "#F5C947", "#F2644C", "#7ACBF1", "#F5F4F5"]
    color = 0
    data = data["data"]
    formatted_data = []
    for job in data[:CAROUSEL_ITEMS_LIMIT]:
        # get enriched data
        company_url = job.get("company", {}).get("companyUrl", "")
        logo_url, social_links = scrape_brandfetch(company_url)
        if not logo_url:
            logo_url = PLACEHOLDER_IMG_URL

        # concat all job functions
        job_functions = job.get("jobFunctions", [])
        job_desc = ""
        for function in job_functions:
            job_desc += function + ". "

        # make sure job id is not None
        job_id = job.get("id", "#")
        if not job_id:
            job_id = "#"

        new_job = {
            "job_title": job.get("details", {}).get("position", "No job title"),
            "company": job.get("company", {}).get("company", "No company"),
            "location": job.get("details", {}).get("location", "No location"),
            "color": colors[color],
            "job_details_url": f"{JOB_DETAILS_WEBPAGE}{search_id}/{job_id}",
            "job_id": job_id,
            "job_desc": job_desc,
            # "job_summary": enriched_data.get("description", "No description"),
            # "industry": enriched_data.get("industry"),
            # "contact_details": enriched_data.get("contact_details"),
            # "company_size": enriched_data.get("company_size"),
            "img_url": logo_url,
            "social_links": social_links
        }
        color += 1
        if color >= len(colors):
            color = 0
        formatted_data.append(new_job)
    return formatted_data


# return type: TextMessage list
def format_text(text, messages_limit):
    messages = text.split("\\n")  # set which character to split by
    formatted_messages = []
    # append back of messages together if exceed 5 messages
    if len(messages) > messages_limit:
        s = "\n".join(messages[messages_limit - 1:])
        messages = messages[:messages_limit - 1]
        messages.append(s)
    # create messages
    for message in messages:
        # check if message is "" or " "
        if not message or message == " ":
            continue
        formatted_messages.append(TextMessage(text=message))
    logging.info(f"FORMAT_TEXT CALLED: {formatted_messages}")
    return formatted_messages


def get_channel_access_token(channel_id):
    KVUri = f"https://{KEY_VAULT_NAME}.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KVUri, credential=credential)
    return client.get_secret(channel_id).value
