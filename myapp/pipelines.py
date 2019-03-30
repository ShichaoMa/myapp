from structor.pipelines import BasePipeline
from toolkit import re_search
from urllib.parse import unquote
import os
import json
import async_downloader

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'Accept-Encoding': 'deflate, gzip'
}

class Mp4DownloadPipeline(BasePipeline):

    def __init__(self, settings):
        super(Mp4DownloadPipeline, self).__init__(settings)
        import requests
        self.downloader = requests.Session()

    def download(self, url, name, proxy):
        if not(os.path.exists(name) and os.path.getsize(name)>100000):
            try:
                try:
                    resp = self.downloader.get(url, headers=headers,
                                               stream=True, timeout=20,
                                               )
                except Exception:
                    resp = self.downloader.get(url, headers=headers,
                                               stream=True, timeout=20,
                                               proxies={"http": proxy,
                                                        "https": proxy})
                with open(name, "wb") as f:
                    have_recv = 0
                    total = int(re_search(
                        "(\d+)", resp.headers.get("Content-Length"), default=0))
                    if total:
                        for chunk in resp.iter_content(chunk_size=1024000):
                            have_recv += len(chunk)
                            self.logger.debug("Got %s from: %s, speed: %s" % (
                                name, url, round(have_recv/total, 2)))
                            f.write(chunk)
                    else:
                        self.logger.error("Have got any data from %s. " % url)
            finally:
                try:
                    if not os.path.getsize(name):
                        os.unlink(name)
                except:
                    pass

    def remote_download(self, url, filename, spider):
        spider.redis_conn.rpush(
            "download_meta", json.dumps({"url": url, "filename": filename}))

    def process_item(self, item, spider):
        proxy = "http://" + spider.redis_conn.srandmember("good_proxies").decode()
        if item["video_url"]:
            self.remote_download(item["video_url"], "%s.mp4"%item["title"].split(" ")[-1], spider)
            #self.download(item["video_url"], "%s.mp4"%item["title"].split(" ")[-1], proxy)
        return item