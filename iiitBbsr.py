from pprint import pprint
import requests
from bs4 import BeautifulSoup
import asyncio

noticeData = []


def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)

    return wrapped


@background
def fetchNotice(noticeUrl, noticeHeading):
    entryReq = requests.get(url=noticeUrl)
    entrySoup = BeautifulSoup(entryReq.content, features="lxml")

    entryContent = entrySoup.find(class_="well text-left").get_text()
    entryDate = entrySoup.find(class_="btn btn-primary").get_text()[6:]
    entryPostedBy = entrySoup.find(class_="btn btn-success").get_text()[11:]
    entryFor = entrySoup.find(class_="btn btn-danger").get_text()[11:]

    entryAttachment = (
        True
        if entrySoup.find(class_="btn btn-info btn-md btn-danger  hvr-wobble-top")
        else False
    )

    noticeData.append(
        {
            "heading": noticeHeading,
            "date": entryDate,
            "by": entryPostedBy,
            "for": entryFor,
            "content": entryContent,
            "hasAttachment": entryAttachment,
        }
    )


def getNotice():
    noticeBoard = BeautifulSoup(
        requests.get(
            url="https://hib.iiit-bh.ac.in/m-ums-2.0/app.pub/nb/nbList1.php"
        ).content,
        features="lxml",
    ).find_all("font", {"color": "red"})

    tasks = []
    for noticeEntry in noticeBoard:
        tasks.append(
            asyncio.ensure_future(
                fetchNotice(
                    f"https://hib.iiit-bh.ac.in/m-ums-2.0/app.pub/nb/{noticeEntry.parent['href']}",
                    noticeEntry.string,
                )
            )
        )

    asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
    return noticeData
