#!/usr/bin/python

import re
import json
import urllib.request as urllib
import codecs

class WikipediaError(Exception):
    pass

class Wikipedia:
    url_article = 'http://%s.wikipedia.org/w/index.php?action=render&title=%s'
    url_image = 'http://%s.wikipedia.org/w/index.php?title=Special:FilePath&file=%s'
    url_search = 'http://%s.wikipedia.org/w/api.php?action=query&list=search&srsearch=%s&sroffset=%d&srlimit=%d&format=json'
    
    def __init__(self, lang):
        self.lang = lang
    
    def __fetch(self, url):
        #request = urllib.Request(url)
        #request.add_header('User-Agent', 'Mozilla/5.0')
        
        try:
            result, headers = urllib.urlretrieve(url)
        except urllib.HTTPError as e:
            raise WikipediaError(e.code)
        except urllib.URLError as e:
            raise WikipediaError(e.reason)
        
        return codecs . open ( result, "r", encoding = "utf-8" )
    
    def article(self, article):
        url = self.url_article % (self.lang, urllib.quote(article))
        content = self.__fetch(url).read()
        if content.upper().startswith('#REDIRECT'):
            match = re.match('(?i)#REDIRECT \[\[([^\[\]]+)\]\]', content)
            
            if not match == None:
                return self.article(match.group(1))
            
            raise WikipediaError('Can\'t found redirect article.')

        return content
    
    def image(self, image, thumb=None):
        url = self.url_image % (self.lang, image)
        result = self.__fetch(url)
        content = result.read()
        
        if thumb:
            url = result.geturl() + '/' + thumb + 'px-' + image
            url = url.replace('/commons/', '/commons/thumb/')
            url = url.replace('/' + self.lang + '/', '/' + self.lang + '/thumb/')
            
            return self.__fetch(url).read()
        
        return content
    
    def search(self, query, page=1, limit=10):
        offset = (page - 1) * limit
        url = self.url_search % (self.lang, urllib.quote(query), offset, limit)
        content = self.__fetch(url).read()
        parsed = json.loads(content)
        search = parsed['query']['search']
        
        results = []
        
        if search:
            for article in search:
                title = article['title'].strip()
                
                snippet = article['snippet']
                snippet = re.sub(r'(?m)<.*?>', '', snippet)
                snippet = re.sub(r'\s+', ' ', snippet)
                snippet = snippet.replace(' . ', '. ')
                snippet = snippet.replace(' , ', ', ')
                snippet = snippet.strip()
                
                wordcount = article['wordcount']
                
                results.append({
                    'title' : title,
                    'snippet' : snippet,
                    'wordcount' : wordcount
                })
        
        # json.dump(results, default_style='', default_flow_style=False,
        #     allow_unicode=True)
        return results

if __name__ == '__main__':
    wiki = Wikipedia('simple')
    wiki.article('Uruguay')
    wiki.image('Bono_at_the_2009_Tribeca_Film_Festival.jpg', '640')
    wiki.search('Wikipedia')
    
    print ( 'OK' )