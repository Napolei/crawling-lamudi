from typing import Optional
import logging
import re
import json


class LamudiPropertyPage:

    def __init__(self, response):
        self.response = response
        json_str = self.extract_json()
        self.error = False
        if json_str:
            self.dict = json_str
        else:
            self.error = True

    def extract_name(self) -> Optional[str]:
        # name = self.response.css('h1::text').get().strip()
        return self.response.css('.Header-title-block>h1::text').get().strip()

    def extract_price(self) -> Optional[str]:
        return self.response.css('.Overview-main.FirstPrice::text').get().strip()

    def extract_floor_area(self) -> Optional[int]:
        selector = self.response.xpath('//*[@class="last"]/text()')
        for s in selector:
            logging.info(s.get())
        return 100

    def extract_properties_list(self):

        selector = self.response.xpath('//*[@id="listing-details"]/*[@class="row"]/*/*[@class="columns-2"]/*')
        for s in selector:
            children = s.xpath('/descendant::text()')
            logging.info("#############net selector#############")
            for c in children:
                text = c.get().strip()
                if text:
                    logging.info("text is :" + text)

            # text = s.get()
        return 0

    def extract_json(self) -> Optional[str]:
        try:
            json_text = re.findall("dataLayer = (.+?);\n", self.response.body.decode("utf-8"), re.S)[0]
            json_text_fixed = re.sub('"categories.+?\n', '', json_text)
            json_text_fixed = re.sub('"device_agent.+?\n', '', json_text_fixed)
            json_text_fixed = re.sub('\t', '\\t', json_text_fixed)
            json_text_fixed = re.sub(r'\u0009', ' ', json_text_fixed)
            json_text_fixed = re.sub(r'\u0020', ' ', json_text_fixed)
            json_text_fixed = re.sub(r'\u00A0', ' ', json_text_fixed)
            json_text_fixed = re.sub(',\n +}', '\n}', json_text_fixed)
        except:
            logging.error('#####################################')
            logging.error(self.response.body)
            logging.error('#####################################')
            return None
        # json_text_fixed = json_text.replace('"categories.+?\n', '\n')

        # logging.info(json_text_fixed)
        try:
            json_array = json.loads(json_text_fixed)
            return json_array[0]
        except:
            logging.error(json_text_fixed)
            return None
