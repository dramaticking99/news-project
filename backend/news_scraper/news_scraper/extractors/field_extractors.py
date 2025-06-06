from scrapy import Selector

FIELD_DEFS = {
    "ndtv": {
        "title":     "//h1[contains(@class,'sp-ttl')]/text()",
        "author":    "//div[contains(@class,'byline')]/span[contains(@class,'author')]/a/text()",
        "published": "//div[contains(@class,'byline')]/span[@class='posted-by']/time/@datetime",
        "content":   "//div[@id='ins_storybody']//p/text()",
    },
    "siteB": {
        "title":     "//h1[@class='headline']/text()",
        "author":    "//span[@class='writer-name']/text()",
        "published": "//time[@class='publish-date']/@datetime",
        "content":   "//div[@class='article-content']//p/text()",
    },
    "siteC": {
        # add Site C’s XPaths here
    },
    # …and so on for every site you support
}

def extract_fields(response, site_key):
    sel = Selector(response)
    data = {}
    defs = FIELD_DEFS.get(site_key, {})
    for field, xpath in defs.items():
        vals = sel.xpath(xpath).getall()
        cleaned = [v.strip() for v in vals if v.strip()]
        data[field] = " ".join(cleaned)
    return data
