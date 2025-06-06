# renderers/splash_renderer.py
from scrapy_splash import SplashRequest

SPLASH_ARGS = {"wait": 1}

def splash_request(url, callback, meta=None):
    return SplashRequest(url, callback=callback, args=SPLASH_ARGS, meta=meta or {})
