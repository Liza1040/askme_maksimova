import cgi


def app(environ, start_response):
    get_parameters = ("GET parameters:\n" + environ['QUERY_STRING'] + '\n\n').replace('&', '\n').encode('utf-8')

    environ['QUERY_STRING'] = ''
    post = cgi.FieldStorage(
        fp=environ['wsgi.input'],
        environ=environ
    )

    post_parameters = "POST parameters:\n"
    for parameter in post.keys():
        value = str(post.getvalue(parameter))
        post_parameters = post_parameters + str(parameter) + ': ' + value + '\n'

    post_parameters = post_parameters.encode('utf-8')

    data = get_parameters + post_parameters
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)
    return iter([data])
