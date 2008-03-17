
from tiddlyweb.tiddler import Tiddler
from tiddlyweb.store import Store, NoTiddlerError
from tiddlyweb.serializer import Serializer, TiddlerFormatError
from tiddlyweb.web.http import HTTP404, HTTP415
from tiddlyweb import web

serializers = {
        'text/x-tiddlywiki': ['wiki', 'text/html'],
        'text/plain': ['text', 'text/plain'],
        'text/html': ['html', 'text/html'],
        'default': ['text', 'text/plain'],
        }

def get(environ, start_response):
    bag_name = environ['wsgiorg.routing_args'][1]['bag_name']
    tiddler_name = environ['wsgiorg.routing_args'][1]['tiddler_name']
    tiddler_name = web.handle_extension(environ, tiddler_name)

    tiddler = Tiddler(tiddler_name)
    tiddler.bag = bag_name

    store = environ['tiddlyweb.store']

    try:
        store.get(tiddler)
    except NoTiddlerError, e:
        raise HTTP404, '%s not found, %s' % (tiddler.title, e)

    serialize_type, mime_type = web.get_serialize_type(environ, serializers)
    serializer = Serializer(serialize_type)
    serializer.object = tiddler

    try:
        content = serializer.to_string()
    except TiddlerFormatError, e:
        raise HTTP415, e

    start_response("200 OK",
            [('Content-Type', mime_type)])

    return [content]
