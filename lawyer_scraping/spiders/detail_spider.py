import scrapy

class DetailSpider(scrapy.Spider):
    name = "detail"

    def start_requests(self):
        file = open('all_numbers.csv')
        numbers = [n.strip() for n in file.readlines()]

        for number in numbers:
            yield scrapy.Request(
                url= "https://www.nichibenren.jp/member_general/lawyer/lawyerSearchResultsList/showMembersDetailedInfo?org.apache.struts.taglib.html.TOKEN=713ca456257edad795948f6833868883&membership_classification=1&registration_no=" + number,
                method='POST',
                headers = {
                    'Cookie:': 'JSESSIONID=5FBF0FF382E0EA762244E77129A4BCAD',
                },
                callback=self.parse
            )

    def parse(self, response):
        common_xpath = '/html/body/div[@class="container"]/div[@id="wrapper"]/div[@class="mainCont"]/form/'
        number_xpath = common_xpath + '/table[1]/tbody/tr[@class="tdColorGray"]/td[2]/text()'
        detail_xpath = common_xpath + '/table[2]/tbody/tr/td/span'

        if len(response.xpath(number_xpath)) <= 0:
            return # 取得できないケースはスキップ

        details = response.xpath(detail_xpath)
        number = response.xpath(number_xpath).extract()[0]
        kana = details[0].css('span::text')[0].extract() if len(details[0].css('span::text')) > 0 else ''
        name = details[1].css('span::text')[0].extract() if len(details[1].css('span::text')) > 0 else ''
        office = details[2].css('span::text')[0].extract() if len(details[2].css('span::text')) > 0 else ''
        postal_code = details[3].css('span::text')[0].extract() if len(details[3].css('span::text')) > 0 else ''
        office_address = details[4].css('span::text')[0].extract() if len(details[4].css('span::text')) > 0 else ''
        tel = details[5].css('span::text')[0].extract() if len(details[5].css('span::text')) > 0 else ''
        fax = details[6].css('span::text')[0].extract() if len(details[6].css('span::text')) > 0 else ''

        yield {
            'number': number,
            'kana': kana,
            'name': name,
            'office': office,
            'postal_code': postal_code,
            'office_address': office_address,
            'tel': tel,
            'fax': fax,
        }
