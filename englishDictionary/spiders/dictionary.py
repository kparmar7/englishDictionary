import scrapy
from scrapy import Request
import re

class DictionarySpider(scrapy.Spider):
    name = 'dictionary'
    start_urls = ['https://www.ldoceonline.com/browse/english/']
    i = 0

    def parse(self, response):
        all_alphbt = response.css(".browse_letters a::attr(href)").getall()[1] #i
        #for next_page in all_alphbt:
        #    link = response.urljoin(next_page)
        yield Request(url=response.urljoin(all_alphbt), callback=self.parse_list)

    def parse_list(self, response):
        all_list = response.css('.browse_groups a::attr(href)').getall()[0]
        #all_list = response.css('ul.browse_groups').css('li').css('a::attr(href)').getall()
        #for next_page in all_list:
        #    link = response.urljoin(next_page)
        #yield Request(url=link, callback=self.parse_next)
        yield Request(url=response.urljoin(all_list), callback=self.parse_next)
    
    def parse_next(self, response):
        all_next = response.css('.browse_results a::attr(href)').getall()[0]
        #all_next = response.css('ul.browse_results').css('li').css('a::attr(href)').getall()
        #for next_page in all_next:
        #   link = response.urljoin(next_page)
        #yield Request(url=link, callback=self.parse_final)
        yield Request(url=response.urljoin(all_next), callback=self.parse_final)

    def parse_final(self, response):
        title = response.css('.pagetitle::text').get()
        all_next = DictionarySpider.i + 1
        data = response.css('.dictlink').css('.ldoceEntry.Entry')
        #print(str(DictionarySpider.i) + ' '+title)#0 A
        dataList = []
        for i in data:
            Head = i.css('.Head').getall()[0].split("<span data-src-mp3", 1)[0].rstrip()
            Head = Head.replace('</span>','')
            Head = Head.replace('<span ','<')
            Head = Head + '<'
            #print(Head,"******************************************************")
            Sense = i.css('.Sense').getall()
            #print(Sense,"SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
            senseList = []
            for i in range (len(Sense)):
                
                trim = Sense[i].replace('</span>','').replace('<span ','<')
                # trim = trim.replace('data-src-mp3="https://www.ldoceonline.com/media/english/exaProns/','')
                trim = re.sub('data-src-mp3.*? ','',trim)
                trim = trim.replace(' exafile fas fa-volume-up hideOnAmp','')
                trim = trim.replace('title="Play Example"','')
                senseList.append({i+1:trim})
            
           # print('***************************************',senseList)
            dataList.append([{'Head':Head},{"Sense" :senseList}])
            #print(i.css('.Head').extract()[0].split("<span data-src-mp3", 1)[0].rstrip(),'********************')
            #print(i.css('.Head').getall(),'***************')
            #print(data[0].css('.Head').extract()[0].split("<span data-src-mp3", 1)[0].rstrip())
        #print(dataList[2])
        yield {"title" : title, "data" : dataList}

#response.css('.pagetitle::text').get()
#response.css('.POS , .PRON , .HYPHENATION::text').getall()
# response.css('.DEF::text').getall() 
#response.css('.Hint , .PROPFORMPREP , .DEF , .HYPHENATION::text').getall()
# response.css('.dictentry').getall()