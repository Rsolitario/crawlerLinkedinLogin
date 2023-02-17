import scrapy
from scrapy_splash import SplashRequest
from pathlib import Path

lua_script = """
function main(splash, args)
    splash:init_cookies(splash.args.cookies)

    assert(splash:go(args.url))
    assert(splash:wait(1))

    splash:set_viewport_full()

    local email_input = splash:select('input[name=session_key]')
    email_input:send_text("caruasdo@gmail.com")
    assert(splash:wait(1))

    local password_input = splash:select('input[name=session_password]')
    password_input:send_text("sasukeuchiha")
    assert(splash:wait(1))

    local credentials_submit = splash:select('.sign-in-form__submit-button')
    credentials_submit:click()
    assert(splash:wait(3))

    return {
        html = splash:html(),
        url = splash:url(),
        cookies = splash:get_cookies(),
    }
    end
"""

class LinkedinLoginSpider(scrapy.Spider):
    name="linkedin"

    def start_requests(self):
        signin_url = "https://www.linkedin.com/home"
        yield SplashRequest(
            url= signin_url,
            callback = self.start_scrapping,
            endpoint="execute",
            args={
                'width':1000,
                'lua_source': lua_script,
                'ua': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
            },
        )
    
    def start_scrapping(self, response):
        cookies_dict = {cookie['name']: cookie['value'] for cookie in response.data['cookies']}
        url_list = ['http://www.linkedin.com/in/reidhoffman/']
        for url in url_list:
            yield scrapy.Request(url=url, cookies=cookies_dict, callback=self.parse)
    
    def parse(self, response):
        print(response.body)
        Path('page.html').write_bytes(response.body)
        with open('response.html', 'wb') as f:
            f.write(response.body)