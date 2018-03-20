# coding=utf-8

def parse_qs(url):
    result = {}
    query = url.partition('?')[2].rpartition('#')[0] if url.find('#') > 0 else url.partition('?')[2]
    for item in query.split('&'):
        key, value = item.split('=')
        result[key] = value
    return result

if __name__ == '__main__':
    url = "https://windard.com/2017/03/12/simple?name=windard&year=21#last"
    print parse_qs(url)
    print parse_qs(url)['name']
    print parse_qs(url)['year']

    url = "https://baidu.com?q=search&p=windard"
    print parse_qs(url)
    print parse_qs(url)['q']
    print parse_qs(url)['p']
