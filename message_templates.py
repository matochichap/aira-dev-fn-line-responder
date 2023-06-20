from linebot.models import *


def create_menu(menu_items):
    # menu_items = data["menu"]
    """
    item: title, subtitle, color, img_url
    """
    bubbles = []
    for item in menu_items:
        bubble = BubbleContainer(
            size="kilo",
            body=BoxComponent(
                layout="vertical",
                padding_all="0px",
                action=URIAction(
                    label="action",
                    uri="https://example.com"
                ),
                contents=[
                    ImageComponent(
                        url=item["img_url"],
                        size="full",
                        aspect_mode="cover",
                        aspect_ratio="2:3",
                        gravity="top"
                    ),
                    BoxComponent(
                        layout="vertical",
                        position="absolute",
                        offset_bottom="0px",
                        offset_start="0px",
                        offset_end="0px",
                        background_color="#03303Acc",
                        padding_all="20px",
                        padding_top="18px",
                        height="130px",
                        contents=[
                            BoxComponent(
                                layout="vertical",
                                contents=[
                                    TextComponent(
                                        text=item["title"],
                                        size="xl",
                                        color=item["color"],
                                        weight="bold",
                                        wrap=True
                                    )
                                ]
                            ),
                            BoxComponent(
                                layout="baseline",
                                spacing="lg",
                                contents=[
                                    TextComponent(
                                        text=item["subtitle"],
                                        size="sm",
                                        color=item["color"],
                                        wrap=True
                                    )
                                ]
                            ),
                            FillerComponent()
                        ]
                    )
                ]
            )
        )

        # Add the bubble to the list of bubbles
        bubbles.append(bubble)

    # Create a CarouselContainer for the FlexMessage
    carousel = CarouselContainer(contents=bubbles)

    # Create the FlexMessage and return it
    return FlexSendMessage(alt_text="Menu", contents=carousel)


def create_job_listings(job_listings):
    # job_listings = data["job_listings"]
    """
    job: job_title, company, location, salary_range, color, img_url
    """
    bubbles = []
    for job in job_listings:
        bubble = BubbleContainer(
            size="kilo",
            body=BoxComponent(
                layout="vertical",
                padding_all="0px",
                contents=[
                    ImageComponent(
                        url=job["img_url"],
                        size="full",
                        aspect_mode="cover",
                        aspect_ratio="1:1",
                        gravity="top"
                    ),
                    BoxComponent(
                        layout="vertical",
                        position="absolute",
                        background_color="#03303Acc",
                        offset_bottom="0px",
                        offset_start="0px",
                        offset_end="0px",
                        padding_top="10px",
                        padding_bottom="10px",
                        contents=[
                            BoxComponent(
                                layout="vertical",
                                padding_start="20px",
                                contents=[
                                    TextComponent(
                                        text=job["job_title"],
                                        size="xl",
                                        color=job['color'],
                                        weight="bold"
                                    )
                                ]
                            ),
                            BoxComponent(
                                layout="baseline",
                                spacing="lg",
                                padding_top="1px",
                                padding_bottom="8px",
                                padding_start="20px",
                                contents=[
                                    TextComponent(
                                        text=f"{job['company']} {job['location']} | {job['salary_range']}",
                                        color="#ebebeb",
                                        size="sm",
                                        flex=0
                                    )
                                ]
                            ),
                            BoxComponent(
                                layout="horizontal",
                                contents=[
                                    BoxComponent(
                                        layout="vertical",
                                        flex=5,
                                        spacing="sm",
                                        margin="xxl",
                                        height="40px",
                                        border_width="1px",
                                        border_color="#ffffff",
                                        corner_radius="4px",
                                        action=URIAction(
                                            label="action",
                                            uri="https://example.com"
                                        ),
                                        contents=[
                                            FillerComponent(),
                                            BoxComponent(
                                                layout="baseline",
                                                spacing="sm",
                                                contents=[
                                                    FillerComponent(),
                                                    TextComponent(
                                                        text="Explore",
                                                        flex=0,
                                                        size="xs",
                                                        color="#ffffff",
                                                        weight="bold",
                                                        offset_top="-2px",
                                                        offset_start="-1px"
                                                    ),
                                                    FillerComponent()
                                                ]
                                            ),
                                            FillerComponent()
                                        ]
                                    ),
                                    BoxComponent(
                                        layout="vertical",
                                        flex=5,
                                        spacing="sm",
                                        margin="xl",
                                        height="40px",
                                        border_width="1px",
                                        border_color="#ffffff",
                                        corner_radius="4px",
                                        action=URIAction(
                                            label="action",
                                            uri="https://example.com"
                                        ),
                                        contents=[
                                            FillerComponent(),
                                            BoxComponent(
                                                layout="baseline",
                                                spacing="sm",
                                                contents=[
                                                    FillerComponent(),
                                                    TextComponent(
                                                        text="Chat",
                                                        flex=0,
                                                        size="xs",
                                                        color="#ffffff",
                                                        weight="bold",
                                                        offset_top="-2px",
                                                        offset_start="-1px"
                                                    ),
                                                    FillerComponent()
                                                ]
                                            ),
                                            FillerComponent()
                                        ]
                                    ),
                                    FillerComponent()
                                ]
                            )
                        ]
                    )
                ]
            )
        )
        bubbles.append(bubble)

    carousel = CarouselContainer(contents=bubbles)

    return FlexSendMessage(alt_text="Job Listings", contents=carousel)


def create_job_applications(job_applications):
    # job_applications = data["job_listings"]
    bubbles = []
    blue = "#6486E3"
    red = "#EF454D"
    grey = "#000000"
    date1 = "29/04"
    date2 = "31/04"
    date3 = "01/05"
    for job in job_applications:
        bubble = BubbleContainer(
            size="mega",
            styles=BubbleStyle(
                header=BlockStyle(
                    background_color=job["color"]
                ),
                body=BlockStyle(
                    background_color=job["color"]
                ),
                footer=BlockStyle(
                    background_color=job["color"]
                )
            ),
            header=BoxComponent(
                layout="horizontal",
                background_color="#00000050",
                contents=[
                    BoxComponent(
                        layout="vertical",
                        flex=4,
                        corner_radius="100px",
                        contents=[
                            ImageComponent(
                                url=job["img_url"],
                                aspect_mode="cover"
                            )
                        ]
                    ),
                    FillerComponent(flex=1),
                    BoxComponent(
                        layout="vertical",
                        flex=10,
                        contents=[
                            FillerComponent(),
                            TextComponent(
                                text=job["job_title"],
                                size="md",
                                color=job["color"],
                                weight="bold"
                            ),
                            FillerComponent(),
                            TextComponent(
                                text=f"{job['company']} {job['location']} | {job['salary_range']}",
                                size="sm",
                                color="#ffffff",
                                wrap=True
                            ),
                            FillerComponent()
                        ]
                    )
                ]
            ),
            body=BoxComponent(
                layout="vertical",
                contents=[
                    BoxComponent(
                        layout="horizontal",
                        spacing="lg",
                        corner_radius="30px",
                        contents=[
                            TextComponent(
                                text=date1,
                                size="sm",
                                gravity="center"
                            ),
                            BoxComponent(
                                layout="vertical",
                                flex=0,
                                contents=[
                                    FillerComponent(),
                                    BoxComponent(
                                        layout="vertical",
                                        width="12px",
                                        height="12px",
                                        border_width="2px",
                                        border_color=red,
                                        corner_radius="30px",
                                    ),
                                    FillerComponent()
                                ]
                            ),
                            TextComponent(
                                text="Application Begin",
                                flex=4,
                                size="sm",
                                weight="bold",
                                gravity="center"
                            )
                        ]
                    ),
                    BoxComponent(
                        layout="horizontal",
                        spacing="lg",
                        height="64px",
                        contents=[
                            BoxComponent(
                                layout="baseline",
                                flex=1,
                                contents=[
                                    FillerComponent()
                                ]
                            ),
                            BoxComponent(
                                layout="vertical",
                                width="12px",
                                contents=[
                                    BoxComponent(
                                        layout="horizontal",
                                        flex=1,
                                        contents=[
                                            FillerComponent(),
                                            BoxComponent(
                                                layout="vertical",
                                                width="2px",
                                                background_color=red,
                                                contents=[]
                                            ),
                                            FillerComponent()
                                        ]
                                    )
                                ]
                            ),
                            BoxComponent(
                                layout="vertical",
                                flex=4,
                                contents=[
                                    TextComponent(
                                        text="Resume Editing",
                                        flex=4,
                                        size="xs",
                                        color=grey,
                                        gravity="center"
                                    ),
                                    TextComponent(
                                        text="Cover Letter Generation",
                                        flex=4,
                                        size="xs",
                                        color=grey,
                                        gravity="center"
                                    )
                                ]
                            )
                        ]
                    ),
                    BoxComponent(
                        layout="horizontal",
                        spacing="lg",
                        corner_radius="30px",
                        contents=[
                            TextComponent(
                                text=date2,
                                size="sm",
                                gravity="center"
                            ),
                            BoxComponent(
                                layout="vertical",
                                flex=0,
                                contents=[
                                    FillerComponent(),
                                    BoxComponent(
                                        layout="vertical",
                                        width="12px",
                                        height="12px",
                                        border_width="2px",
                                        border_color=blue,
                                        corner_radius="30px",
                                    ),
                                    FillerComponent()
                                ]
                            ),
                            TextComponent(
                                text="Documents Complete",
                                flex=4,
                                size="sm",
                                weight="bold",
                                gravity="center"
                            )
                        ]
                    ),
                    BoxComponent(
                        layout="horizontal",
                        spacing="lg",
                        height="64px",
                        contents=[
                            BoxComponent(
                                layout="baseline",
                                flex=1,
                                contents=[
                                    FillerComponent()
                                ]
                            ),
                            BoxComponent(
                                layout="vertical",
                                width="12px",
                                contents=[
                                    BoxComponent(
                                        layout="horizontal",
                                        flex=1,
                                        contents=[
                                            FillerComponent(),
                                            BoxComponent(
                                                layout="vertical",
                                                width="2px",
                                                background_color=blue,
                                                contents=[]
                                            ),
                                            FillerComponent()
                                        ]
                                    )
                                ]
                            ),
                            BoxComponent(
                                layout="vertical",
                                flex=4,
                                contents=[
                                    TextComponent(
                                        text="Submit Application",
                                        flex=4,
                                        size="xs",
                                        color=grey,
                                        gravity="center"
                                    )
                                ]
                            )
                        ]
                    ),
                    BoxComponent(
                        layout="horizontal",
                        spacing="lg",
                        corner_radius="30px",
                        contents=[
                            TextComponent(
                                text=date3,
                                size="sm",
                                gravity="center"
                            ),
                            BoxComponent(
                                layout="vertical",
                                flex=0,
                                contents=[
                                    FillerComponent(),
                                    BoxComponent(
                                        layout="vertical",
                                        width="12px",
                                        height="12px",
                                        border_width="2px",
                                        border_color=blue,
                                        corner_radius="30px",
                                    ),
                                    FillerComponent()
                                ]
                            ),
                            TextComponent(
                                text="Application Submitted",
                                flex=4,
                                size="sm",
                                weight="bold",
                                gravity="center"
                            )
                        ]
                    )
                ]
            ),
            footer=BoxComponent(
                layout="vertical",
                contents=[
                    ButtonComponent(
                        height="sm",
                        action=URIAction(
                            label="Continue Application",
                            uri="https://example.com"
                        )
                    )
                ]
            )
        )
        bubbles.append(bubble)

    carousel = CarouselContainer(contents=bubbles)

    return FlexSendMessage(alt_text="Job Applications", contents=carousel)
