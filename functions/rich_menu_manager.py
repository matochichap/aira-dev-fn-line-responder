import os
from linebot import LineBotApi
from linebot.models import *

CHANNEL_ACCESS_TOKEN = os.environ.get('channel_access_token')
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
AIRA_LANDING_PAGE = "https://www.helloaira.io/"
LIFF_RESUME_UPLOAD_PAGE = "https://liff.line.me/2000163158-e84bk6bW"


def create_rich_menus():
    # define rich menus
    rich_menu_a = RichMenu(
        size=RichMenuSize(width=2500, height=843),
        selected=False,
        name="Menu A",
        chat_bar_text="Upload Resume",
        areas=[
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=843, height=843),
                action=URIAction(label='Aira Website', uri=AIRA_LANDING_PAGE)
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=843, y=0, width=1657, height=843),
                action=URIAction(label='LIFF Resume Upload', uri=LIFF_RESUME_UPLOAD_PAGE)
            )
        ]
    )

    rich_menu_a_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_a)

    # set rich menu image
    with open('../rich-menus/aira-beta-menu-a.png', 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_a_id, 'image/png', f)

    # set default rich menu
    line_bot_api.set_default_rich_menu(rich_menu_a_id)

    print(rich_menu_a_id)


# rich menu functions
def get_all_rich_menu_ids():
    ids = []
    rich_menus = line_bot_api.get_rich_menu_list()
    for menu in rich_menus:
        id = menu.rich_menu_id
        ids.append(id)
    return ids


def delete_all_rich_menus():
    ids = get_all_rich_menu_ids()
    print(ids)
    for id in ids:
        line_bot_api.delete_rich_menu(id)
    ids = get_all_rich_menu_ids()
    print(ids)


# rich menu alias functions
def get_all_rich_menu_alias():
    a = []
    ls = line_bot_api.get_rich_menu_alias_list()
    for alias in ls.aliases:
        a.append(alias.rich_menu_alias_id)
    return a


def delete_all_aliases():
    aliases = get_all_rich_menu_alias()
    print(aliases)
    for a in aliases:
        line_bot_api.delete_rich_menu_alias(a)
    print(get_all_rich_menu_alias())


print(delete_all_rich_menus())
print(create_rich_menus())
