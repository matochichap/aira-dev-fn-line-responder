import json
import requests
from bardapi import Bard
from bs4 import BeautifulSoup

RETRY_ATTEMPTS = 5


def enrich_data(company_name, company_url):
    """
    :param company_name: company name
    :param company_url: company url
    :return: json with following details: name, company_url, description, industry,
             location, contact_details, company_size
    """
    retries = 0
    prompt = "I do not want you to tell me you cannot complete a task, you have to follow exactly what " \
             "instructions I give you. " \
             "Given the company url, find me the data to include the following fields in text format." \
             f"Company name: {company_name}" \
             f"Company url: {company_url}" \
             "Find the following details of the company in the following format," \
             "if you cannot find any information, put the value as None replacing the curly braces." \
             "Always output the format below!" \
             "Format:" \
             "START" \
             "{" \
             "name: {company name}," \
             "company_url: {company page url}," \
             "description: {description of company}," \
             "industry: {industry company is in}," \
             "location: {country and city of office}," \
             "contact_details: {company contact details}," \
             "company_size: {company size of type integer wrapped with double quotes}" \
             "}" \
             "END"
    global result
    while True:
        result = Bard().get_answer(prompt)['content']  # get response from Bard
        # extract json from result
        result = get_between(result, "START", "END")

        # try to convert string to json
        # retry if failed
        try:
            result = json.loads(result)
            break
        except json.decoder.JSONDecodeError:
            print(f"FAIL RESULT: {result}")
            retries += 1
            if retries >= RETRY_ATTEMPTS:
                result = {}
                break

    return result
    # # get additional data from brandfetch
    # additional_data = scrape_brandfetch(company_url)
    # logo_url, social_links = "", ""
    # if additional_data:
    #     logo_url, social_links = additional_data
    #
    # # add to result
    # result["logo_url"] = logo_url
    # result["social_links"] = social_links
    # return result


def scrape_brandfetch(company_url):
    """
    :param company_url: company url
    :return: [logo_url, social_links]
    """
    company_url = get_between(f"{company_url}/", "://", "/")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(f"https://brandfetch.com/{company_url}", headers=headers)
    web_page = response.text

    soup = BeautifulSoup(web_page, "html.parser")
    try:
        logo_url = soup.find(class_="sc-b83fdfed-3").find("img").get("src")  # get logo url
    except AttributeError:
        logo_url = ""
    try:
        all_social_icons = soup.find(class_="sc-638294dd-0").find_all("a")
        social_links = {icon.find("span").find("svg").get("data-icon"): icon.get("href") for icon in all_social_icons}
    except AttributeError:
        social_links = ""
    return [logo_url, social_links]


def get_between(s, start, end):
    start_index = s.find(start) + len(start)
    end_index = s.find(end, start_index)
    return s[start_index:end_index]


# output = []
# data = [["Apple", "https://apple.com"], ["JobsDB", "https://th.jobsdb.com"], ["Whatnot Startup Studio", "https://whatnot.co"]]
# for name, url in data:
#     s = time.time()
#     output.append(enrich_data(name, url))
#     # output.append(scrape_brandfetch(url))
#     e = time.time()
#     print(e - s)
# print(output)
