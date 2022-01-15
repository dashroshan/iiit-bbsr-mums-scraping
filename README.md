# IIIT Bbsr M-UMS Scraping

## Notice Board

Get latest notices as a list of dictionaries in the below format

```py
{
    "heading" : "Notice heading",
    "date" : "YYYY-MM-DD",
    "for" : "For whom is the notice posted",
    "by" : "Who posted the notice",
    "hasAttachment" : True or False,
    "content" : "Notice text"
}
```

### Sample use:

```py
# iiitBbsr.py in the same folder as this python file
from iiitBbsr import getNotice
for notice in getNotice():
    print(notice["heading"])
```