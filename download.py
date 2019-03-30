import os
import json
import aiohttp
import aiofiles
import traceback

from async_downloader.utils import readexactly
from async_downloader.download_engines import _safe_download 

async def co_session_download(self, url, filename, failed_times=0, sessions=[]):
    """所有请求使用同一个session，但需要增加将session的close方法传递给download函数"""
    if not sessions:
        sessions.append(aiohttp.ClientSession(
            conn_timeout=10, read_timeout=1800))
        co_session_download.close = sessions[0].close
    return await _safe_download(self, url, filename, failed_times, sessions[0])


