import logging


def save_response(response):
    url = response.request.url.split('www.')[1].replace('/', '_')
    filename = '%s.html' % url
    with open(filename, 'wb') as f:
        f.write(response.body)
    logging.info('Saved file %s' % filename)
