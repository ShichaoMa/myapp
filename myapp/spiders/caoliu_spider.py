# -*- coding:utf-8 -*-
"""
spider编写规则
1 spider必须继承自StructureSpider
2 若执行分类抓取则需要配置item_pattern = (), page_pattern = ()，其中：
    1）item_pattern元组中的元素为分类页中每个item链接所对应的xpath表达式
    2）page_pattern元组中的元素可以是下一页链接所所对应的正则表达式，或者其它规则，详见
    https://github.com/ShichaoMa/structure_spider/wiki/%08page_partten%E5%92%8Citem_partten%E7%BC%96%E5%86%99%E8%A7%84%E5%88%99
3 提供get_base_loader静态方法，传入response，返回CustomLoader对应一个Item
4 提供enrich_data方法，必须被enrich_wrapper装饰，其中：
    1）传入item_loader, response，使用item_loader的方法(add_value, add_xpath, add_re)添加要抓取的属性名及其对应表达式或值。
    2）如该次渲染需要产生新的请求，返回三元组列表[(prop, item_loader, request_meta)]。其中：
        prop: 指下次请求获取的全部字段如果做为一个子item返回时，子item在其父item中对应的字段名称。
        item_loader: 用来抽取下次请求中字段的item_loader，如果下次请求返回子item，则此item_loader与父级item_loader不同
        request_meta: 组建request所需要的kwargs type: dict
4 下次请求所回调的enrich函数名称为 enrich_`prop`
"""
from structor.spiders import StructureSpider
from structor.utils import CustomLoader, enrich_wrapper
from ..items.caoliu_item import CaoliuItem
from ..parse import parse
from html.parser import unescape


class CaoliuSpider(StructureSpider):
    name = "caoliu"
    # 分类抓取的时候使用这两个属性
    item_pattern = ('//tr/td/h3/a/@href',)
    page_pattern = ('//a[@id="last"]/preceding-sibling::a[1]/@href',)
    custom_settings = {
        "ITEM_PIPELINES": {
            "myapp.pipelines.Mp4DownloadPipeline": 100,
        }
    }

    @staticmethod
    def get_base_loader(response):
        return CustomLoader(item=CaoliuItem())

    @enrich_wrapper
    def enrich_data(self, item_loader, response):
        item_loader.add_re("id", r'tid=(\d+)')
        title = "".join(response.xpath('//h4/text()').extract())
        item_loader.add_value("title", title)
        video_url = unescape("".join(response.selector.re(r"\.src='(.*)#iframeload'")))
        return [("video_url", item_loader, {"url": video_url})]

    @enrich_wrapper
    def enrich_video_url(self, item_loader, response):
        video_urls = response.selector.re(r"video\w*?_url: '(.*?)'")
        code = "".join(response.selector.re(r"\w+?code: '(.*?)'"))

        def gen():
            for i in range(10):
                yield "video_url_%d" % i

        download_url = ""
        if video_urls:
            video_meta = dict(zip(gen(), video_urls))
            video_meta["code"] = code
            parse(video_meta)
            for k, v in sorted(video_meta.items(), key=lambda x: x[0], reverse=True):
                if k.startswith("video_url"):
                    download_url = video_meta.get(k)
                    if download_url.count("mp4"):
                        break
        if not download_url:
            download_url = "".join(response.selector.re(r'source:"(.*?)"'))
        if not download_url:
            download_url = "".join(response.selector.re(r"video:'(.*?)'"))
        if download_url:
            item_loader.add_value("video_url", download_url)
        else:
            item_loader.add_xpath("video_url", "//source/@src")
