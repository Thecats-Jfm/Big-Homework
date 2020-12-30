# coding = utf-8
import sys
import json
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus
import Libs
def YuYinHeCheng(TEXT,Save_Path):
    Libs.Baidu_YuYinHeCheng(TEXT,Save_Path)