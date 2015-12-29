#!/usr/bin/env python
from __future__ import with_statement

from gi.repository import Gtk, GdkPixbuf, Gdk
import urllib, urllib2, os, thread, socket, base64

import sys, cgi, email.utils, functools, hmac, imp, itertools, mimetypes, re, tempfile, threading, time, warnings
from types import FunctionType
from datetime import date as datedate, datetime, timedelta
from tempfile import TemporaryFile
from traceback import format_exc, print_exc
from unicodedata import normalize

#################################################################
####              THE MINIFIED BOTTLE SERVER
#################################################################

try:
    from inspect import signature
    def getargspec(func):
        params = signature(func).parameters
        args, varargs, keywords, defaults = [], None, None, []
        for name, param in params.items():
            if param.kind == param.VAR_POSITIONAL:
                varargs = name
            elif param.kind == param.VAR_KEYWORD:
                keywords = name
            else:
                args.append(name)
                if param.default is not param.empty:
                    defaults.append(param.default)
        return (args, varargs, keywords, tuple(defaults) or None)
except ImportError:
    try:
        from inspect import getfullargspec
        def getargspec(func):
            spec = getfullargspec(func)
            kwargs = makelist(spec[0]) + makelist(spec.kwonlyargs)
            return kwargs, spec[1], spec[2], spec[3]
    except ImportError:
        from inspect import getargspec
try:
    from simplejson import dumps as json_dumps, loads as json_lds
except ImportError:
    try:
        from json import dumps as json_dumps, loads as json_lds
    except ImportError:
        try:
            from django.utils.simplejson import dumps as json_dumps, loads as json_lds
        except ImportError:
            def json_dumps(data):
                raise ImportError("JSON support requires Python 2.6 or simplejson.")
            json_lds = json_dumps
py = sys.version_info
py3k = py >= (3, 0, 0)
py25 = py <  (2, 6, 0)
py31 = (3, 1, 0) <= py < (3, 2, 0)
def _e():
    return sys.exc_info()[1]
try:
    _stdout, _stderr = sys.stdout.write, sys.stderr.write
except IOError:
    _stdout = lambda x: sys.stdout.write(x)
    _stderr = lambda x: sys.stderr.write(x)
if py3k:
    import http.client as httplib
    import _thread as thread
    from urllib.parse import urljoin, SplitResult as UrlSplitResult
    from urllib.parse import urlencode, quote as urlquote, unquote as urlunquote
    urlunquote = functools.partial(urlunquote, encoding='latin1')
    from http.cookies import SimpleCookie
    from collections import MutableMapping as DictMixin
    import pickle
    from io import BytesIO
    from configparser import ConfigParser, Error as ConfigParserError
    basestring = str
    unicode = str
    json_loads = lambda s: json_lds(touni(s))
    callable = lambda x: hasattr(x, '__call__')
    imap = map
    def _raise(*a):
        raise a[0](a[1]).with_traceback(a[2])
else:
    import httplib
    import thread
    from urlparse import urljoin, SplitResult as UrlSplitResult
    from urllib import urlencode, quote as urlquote, unquote as urlunquote
    from Cookie import SimpleCookie
    from itertools import imap
    import cPickle as pickle
    from StringIO import StringIO as BytesIO
    from ConfigParser import SafeConfigParser as ConfigParser, \
                             Error as ConfigParserError
    if py25:
        from UserDict import DictMixin
        def next(it):
            return it.next()
        bytes = str
    else:
        from collections import MutableMapping as DictMixin
    unicode = unicode
    json_loads = json_lds
    eval(compile('def _raise(*a): raise a[0], a[1], a[2]', '<py3fix>', 'exec'))
if py25 or py31:
    warnings.warn("Python 2.5 and 3.1 support will be dropped in future versions of Bottle.", DeprecationWarning)
def tob(s, enc='utf8'):
    return s.encode(enc) if isinstance(s, unicode) else bytes(s)
def touni(s, enc='utf8', err='strict'):
    if isinstance(s, bytes):
        return s.decode(enc, err)
    else:
        return unicode(s or ("" if s is None else s))
tonat = touni if py3k else tob
def update_wrapper(wrapper, wrapped, *a, **ka):
    try:
        functools.update_wrapper(wrapper, wrapped, *a, **ka)
    except AttributeError:
        pass
def depr(major, minor, cause, fix):
    text = "Warning: Use of deprecated feature or API. (Deprecated in Bottle-%d.%d)\n"\
           "Cause: %s\n"\
           "Fix: %s\n" %  (major, minor, cause, fix)
    if DEBUG == 'strict':
        raise DeprecationWarning(text)
    warnings.warn(text, DeprecationWarning, stacklevel=3)
    return DeprecationWarning(text)
def makelist(data):
    if isinstance(data, (tuple, list, set, dict)):
        return list(data)
    elif data:
        return [data]
    else:
        return []
class DictProperty(object):
    def __init__(self, attr, key=None, read_only=False):
        self.attr, self.key, self.read_only = attr, key, read_only
    def __call__(self, func):
        functools.update_wrapper(self, func, updated=[])
        self.getter, self.key = func, self.key or func.__name__
        return self
    def __get__(self, obj, cls):
        if obj is None: return self
        key, storage = self.key, getattr(obj, self.attr)
        if key not in storage: storage[key] = self.getter(obj)
        return storage[key]
    def __set__(self, obj, value):
        if self.read_only: raise AttributeError("Read-Only property.")
        getattr(obj, self.attr)[self.key] = value
    def __delete__(self, obj):
        if self.read_only: raise AttributeError("Read-Only property.")
        del getattr(obj, self.attr)[self.key]
class cached_property(object):
    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func
    def __get__(self, obj, cls):
        if obj is None: return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value
class lazy_attribute(object):
    def __init__(self, func):
        functools.update_wrapper(self, func, updated=[])
        self.getter = func
    def __get__(self, obj, cls):
        value = self.getter(cls)
        setattr(cls, self.__name__, value)
        return value
class BottleException(Exception):
    pass
class RouteError(BottleException):
    pass
class RouteReset(BottleException):
    pass
class RouterUnknownModeError(RouteError):
    pass
class RouteSyntaxError(RouteError):
    pass
class RouteBuildError(RouteError):
    pass
def _re_flatten(p):
    if '(' not in p:
        return p
    return re.sub(r'(\\*)(\(\?P<[^>]+>|\((?!\?))', lambda m: m.group(0) if
                  len(m.group(1)) % 2 else m.group(1) + '(?:', p)
class Router(object):
    default_pattern = '[^/]+'
    default_filter = 're'
    _MAX_GROUPS_PER_PATTERN = 99
    def __init__(self, strict=False):
        self.rules = []
        self._groups = {}
        self.builder = {}
        self.static = {}
        self.dyna_routes = {}
        self.dyna_regexes = {}
        self.strict_order = strict
        self.filters = {
            're': lambda conf: (_re_flatten(conf or self.default_pattern),
                                None, None),
            'int': lambda conf: (r'-?\d+', int, lambda x: str(int(x))),
            'float': lambda conf: (r'-?[\d.]+', float, lambda x: str(float(x))),
            'path': lambda conf: (r'.+?', None, None)
        }
    def add_filter(self, name, func):
        self.filters[name] = func
    rule_syntax = re.compile('(\\\\*)'
        '(?:(?::([a-zA-Z_][a-zA-Z_0-9]*)?()(?:#(.*?)#)?)'
          '|(?:<([a-zA-Z_][a-zA-Z_0-9]*)?(?::([a-zA-Z_]*)'
            '(?::((?:\\\\.|[^\\\\>]+)+)?)?)?>))')
    def _itertokens(self, rule):
        offset, prefix = 0, ''
        for match in self.rule_syntax.finditer(rule):
            prefix += rule[offset:match.start()]
            g = match.groups()
            if g[2] is not None:
                depr(0, 13, "Use of old route syntax.",
                            "Use <name> instead of :name in routes.")
            if len(g[0]) % 2:
                prefix += match.group(0)[len(g[0]):]
                offset = match.end()
                continue
            if prefix:
                yield prefix, None, None
            name, filtr, conf = g[4:7] if g[2] is None else g[1:4]
            yield name, filtr or 'default', conf or None
            offset, prefix = match.end(), ''
        if offset <= len(rule) or prefix:
            yield prefix + rule[offset:], None, None
    def add(self, rule, method, target, name=None):
        anons = 0  
        keys = []  
        pattern = ''  
        filters = []  
        builder = []  
        is_static = True
        for key, mode, conf in self._itertokens(rule):
            if mode:
                is_static = False
                if mode == 'default': mode = self.default_filter
                mask, in_filter, out_filter = self.filters[mode](conf)
                if not key:
                    pattern += '(?:%s)' % mask
                    key = 'anon%d' % anons
                    anons += 1
                else:
                    pattern += '(?P<%s>%s)' % (key, mask)
                    keys.append(key)
                if in_filter: filters.append((key, in_filter))
                builder.append((key, out_filter or str))
            elif key:
                pattern += re.escape(key)
                builder.append((None, key))
        self.builder[rule] = builder
        if name: self.builder[name] = builder
        if is_static and not self.strict_order:
            self.static.setdefault(method, {})
            self.static[method][self.build(rule)] = (target, None)
            return
        try:
            re_pattern = re.compile('^(%s)$' % pattern)
            re_match = re_pattern.match
        except re.error:
            raise RouteSyntaxError("Could not add Route: %s (%s)" % (rule, _e()))
        if filters:
            def getargs(path):
                url_args = re_match(path).groupdict()
                for name, wildcard_filter in filters:
                    try:
                        url_args[name] = wildcard_filter(url_args[name])
                    except ValueError:
                        raise HTTPError(400, 'Path has wrong format.')
                return url_args
        elif re_pattern.groupindex:
            def getargs(path):
                return re_match(path).groupdict()
        else:
            getargs = None
        flatpat = _re_flatten(pattern)
        whole_rule = (rule, flatpat, target, getargs)
        if (flatpat, method) in self._groups:
            if DEBUG:
                msg = 'Route <%s %s> overwrites a previously defined route'
                warnings.warn(msg % (method, rule), RuntimeWarning)
            self.dyna_routes[method][
                self._groups[flatpat, method]] = whole_rule
        else:
            self.dyna_routes.setdefault(method, []).append(whole_rule)
            self._groups[flatpat, method] = len(self.dyna_routes[method]) - 1
        self._compile(method)
    def _compile(self, method):
        all_rules = self.dyna_routes[method]
        comborules = self.dyna_regexes[method] = []
        maxgroups = self._MAX_GROUPS_PER_PATTERN
        for x in range(0, len(all_rules), maxgroups):
            some = all_rules[x:x + maxgroups]
            combined = (flatpat for (_, flatpat, _, _) in some)
            combined = '|'.join('(^%s$)' % flatpat for flatpat in combined)
            combined = re.compile(combined).match
            rules = [(target, getargs) for (_, _, target, getargs) in some]
            comborules.append((combined, rules))
    def build(self, _name, *anons, **query):
        builder = self.builder.get(_name)
        if not builder:
            raise RouteBuildError("No route with that name.", _name)
        try:
            for i, value in enumerate(anons):
                query['anon%d' % i] = value
            url = ''.join([f(query.pop(n)) if n else f for (n, f) in builder])
            return url if not query else url + '?' + urlencode(query)
        except KeyError:
            raise RouteBuildError('Missing URL argument: %r' % _e().args[0])
    def match(self, environ):
        verb = environ['REQUEST_METHOD'].upper()
        path = environ['PATH_INFO'] or '/'
        if verb == 'HEAD':
            methods = ['PROXY', verb, 'GET', 'ANY']
        else:
            methods = ['PROXY', verb, 'ANY']
        for method in methods:
            if method in self.static and path in self.static[method]:
                target, getargs = self.static[method][path]
                return target, getargs(path) if getargs else {}
            elif method in self.dyna_regexes:
                for combined, rules in self.dyna_regexes[method]:
                    match = combined(path)
                    if match:
                        target, getargs = rules[match.lastindex - 1]
                        return target, getargs(path) if getargs else {}
        allowed = set([])
        nocheck = set(methods)
        for method in set(self.static) - nocheck:
            if path in self.static[method]:
                allowed.add(verb)
        for method in set(self.dyna_regexes) - allowed - nocheck:
            for combined, rules in self.dyna_regexes[method]:
                match = combined(path)
                if match:
                    allowed.add(method)
        if allowed:
            allow_header = ",".join(sorted(allowed))
            raise HTTPError(405, "Method not allowed.", Allow=allow_header)
        raise HTTPError(404, "Not found: " + repr(path))
class Route(object):
    def __init__(self, app, rule, method, callback, name=None, plugins=None, skiplist=None, **config):
        self.app = app
        self.rule = rule
        self.method = method
        self.callback = callback
        self.name = name or None
        self.plugins = plugins or []
        self.skiplist = skiplist or []
        self.config = ConfigDict().load_dict(config)
    @cached_property
    def call(self):
        return self._make_callback()
    def reset(self):
        self.__dict__.pop('call', None)
    def prepare(self):
        self.call
    def all_plugins(self):
        unique = set()
        for p in reversed(self.app.plugins + self.plugins):
            if True in self.skiplist: break
            name = getattr(p, 'name', False)
            if name and (name in self.skiplist or name in unique): continue
            if p in self.skiplist or type(p) in self.skiplist: continue
            if name: unique.add(name)
            yield p
    def _make_callback(self):
        callback = self.callback
        for plugin in self.all_plugins():
            try:
                if hasattr(plugin, 'apply'):
                    callback = plugin.apply(callback, self)
                else:
                    callback = plugin(callback)
            except RouteReset:  
                return self._make_callback()
            if not callback is self.callback:
                update_wrapper(callback, self.callback)
        return callback
    def get_undecorated_callback(self):
        func = self.callback
        func = getattr(func, '__func__' if py3k else 'im_func', func)
        closure_attr = '__closure__' if py3k else 'func_closure'
        while hasattr(func, closure_attr) and getattr(func, closure_attr):
            attributes = getattr(func, closure_attr)
            func = attributes[0].cell_contents
            if not isinstance(func, FunctionType):
                func = filter(lambda x: isinstance(x, FunctionType),
                              map(lambda x: x.cell_contents, attributes))
                func = list(func)[0]
        return func
    def get_callback_args(self):
        return getargspec(self.get_undecorated_callback())[0]
    def get_config(self, key, default=None):
        for conf in (self.config, self.app.config):
            if key in conf: return conf[key]
        return default
    def __repr__(self):
        cb = self.get_undecorated_callback()
        return '<%s %r %r>' % (self.method, self.rule, cb)
class Bottle(object):
    def __init__(self, catchall=True, autojson=True):
        self.config = ConfigDict()
        self.config._add_change_listener(functools.partial(self.trigger_hook, 'config'))
        self.config.meta_set('autojson', 'validate', bool)
        self.config.meta_set('catchall', 'validate', bool)
        self.config['catchall'] = catchall
        self.config['autojson'] = autojson
        self._mounts = []
        self.resources = ResourceManager()
        self.routes = []
        self.router = Router()
        self.error_handler = {}
        self.plugins = []
        if self.config['autojson']:
            self.install(JSONPlugin())
    catchall = DictProperty('config', 'catchall')
    __hook_names = 'before_request', 'after_request', 'app_reset', 'config'
    __hook_reversed = 'after_request'
    @cached_property
    def _hooks(self):
        return dict((name, []) for name in self.__hook_names)
    def add_hook(self, name, func):
        if name in self.__hook_reversed:
            self._hooks[name].insert(0, func)
        else:
            self._hooks[name].append(func)
    def remove_hook(self, name, func):
        if name in self._hooks and func in self._hooks[name]:
            self._hooks[name].remove(func)
            return True
    def trigger_hook(self, __name, *args, **kwargs):
        return [hook(*args, **kwargs) for hook in self._hooks[__name][:]]
    def hook(self, name):
        def decorator(func):
            self.add_hook(name, func)
            return func
        return decorator
    def _mount_wsgi(self, prefix, app, **options):
        segments = [p for p in prefix.split('/') if p]
        if not segments:
            raise ValueError('WSGI applications cannot be mounted to "/".')
        path_depth = len(segments)
        def mountpoint_wrapper():
            try:
                request.path_shift(path_depth)
                rs = HTTPResponse([])
                def start_response(status, headerlist, exc_info=None):
                    if exc_info:
                        _raise(*exc_info)
                    rs.status = status
                    for name, value in headerlist:
                        rs.add_header(name, value)
                    return rs.body.append
                body = app(request.environ, start_response)
                rs.body = itertools.chain(rs.body, body) if rs.body else body
                return rs
            finally:
                request.path_shift(-path_depth)
        options.setdefault('skip', True)
        options.setdefault('method', 'PROXY')
        options.setdefault('mountpoint', {'prefix': prefix, 'target': app})
        options['callback'] = mountpoint_wrapper
        self.route('/%s/<:re:.*>' % '/'.join(segments), **options)
        if not prefix.endswith('/'):
            self.route('/' + '/'.join(segments), **options)
    def _mount_app(self, prefix, app, **options):
        if app in self._mounts or '_mount.app' in app.config:
            depr(0, 13, "Application mounted multiple times. Falling back to WSGI mount.",
                 "Clone application before mounting to a different location.")
            return self._mount_wsgi(prefix, app, **options)
        if options:
            depr(0, 13, "Unsupported mount options. Falling back to WSGI mount.", "Do not specify any route options when mounting bottle application.")
            return self._mount_wsgi(prefix, app, **options)
        if not prefix.endswith("/"):
            depr(0, 13, "Prefix must end in '/'. Falling back to WSGI mount.", "Consider adding an explicit redirect from '/prefix' to '/prefix/' in the parent application.")
            return self._mount_wsgi(prefix, app, **options)
        self._mounts.append(app)
        app.config['_mount.prefix'] = prefix
        app.config['_mount.app'] = self
        for route in app.routes:
            route.rule = prefix + route.rule.lstrip('/')
            self.add_route(route)
    def mount(self, prefix, app, **options):
        if not prefix.startswith('/'):
            raise ValueError("Prefix must start with '/'")
        if isinstance(app, Bottle):
            return self._mount_app(prefix, app, **options)
        else:
            return self._mount_wsgi(prefix, app, **options)
    def merge(self, routes):
        if isinstance(routes, Bottle):
            routes = routes.routes
        for route in routes:
            self.add_route(route)
    def install(self, plugin):
        if hasattr(plugin, 'setup'): plugin.setup(self)
        if not callable(plugin) and not hasattr(plugin, 'apply'):
            raise TypeError("Plugins must be callable or implement .apply()")
        self.plugins.append(plugin)
        self.reset()
        return plugin
    def uninstall(self, plugin):
        removed, remove = [], plugin
        for i, plugin in list(enumerate(self.plugins))[::-1]:
            if remove is True or remove is plugin or remove is type(plugin) \
            or getattr(plugin, 'name', True) == remove:
                removed.append(plugin)
                del self.plugins[i]
                if hasattr(plugin, 'close'): plugin.close()
        if removed: self.reset()
        return removed
    def reset(self, route=None):
        if route is None: routes = self.routes
        elif isinstance(route, Route): routes = [route]
        else: routes = [self.routes[route]]
        for route in routes:
            route.reset()
        if DEBUG:
            for route in routes:
                route.prepare()
        self.trigger_hook('app_reset')
    def close(self):
        for plugin in self.plugins:
            if hasattr(plugin, 'close'): plugin.close()
    def run(self, **kwargs):
        run(self, **kwargs)
    def match(self, environ):
        return self.router.match(environ)
    def get_url(self, routename, **kargs):
        scriptname = request.environ.get('SCRIPT_NAME', '').strip('/') + '/'
        location = self.router.build(routename, **kargs).lstrip('/')
        return urljoin(urljoin('/', scriptname), location)
    def add_route(self, route):
        self.routes.append(route)
        self.router.add(route.rule, route.method, route, name=route.name)
        if DEBUG: route.prepare()
    def route(self, path=None, method='GET', callback=None, name=None, apply=None, skip=None, **config):
        if callable(path): path, callback = None, path
        plugins = makelist(apply)
        skiplist = makelist(skip)
        def decorator(callback):
            if isinstance(callback, basestring): callback = load(callback)
            for rule in makelist(path) or yieldroutes(callback):
                for verb in makelist(method):
                    verb = verb.upper()
                    route = Route(self, rule, verb, callback, name=name, plugins=plugins, skiplist=skiplist, **config)
                    self.add_route(route)
            return callback
        return decorator(callback) if callback else decorator
    def get(self, path=None, method='GET', **options):
        return self.route(path, method, **options)
    def delete(self, path=None, method='DELETE', **options):
        return self.route(path, method, **options)
    def patch(self, path=None, method='PATCH', **options):
        return self.route(path, method, **options)
    def error(self, code=500):
        def wrapper(handler):
            self.error_handler[int(code)] = handler
            return handler
        return wrapper
    def default_error_handler(self, res):
        return tob(template(ERROR_PAGE_TEMPLATE, e=res))
    def _handle(self, environ):
        path = environ['bottle.raw_path'] = environ['PATH_INFO']
        if py3k:
            environ['PATH_INFO'] = path.encode('latin1').decode('utf8', 'ignore')
        def _inner_handle():
            try:
                route, args = self.router.match(environ)
                environ['route.handle'] = route
                environ['bottle.route'] = route
                environ['route.url_args'] = args
                return route.call(**args)
            except HTTPResponse:
                return _e()
            except RouteReset:
                route.reset()
                return _inner_handle()
            except (KeyboardInterrupt, SystemExit, MemoryError):
                raise
            except Exception:
                if not self.catchall: raise
                stacktrace = format_exc()
                environ['wsgi.errors'].write(stacktrace)
                return HTTPError(500, "Internal Server Error", _e(), stacktrace)
        try:
            out = None
            environ['bottle.app'] = self
            request.bind(environ)
            response.bind()
            self.trigger_hook('before_request')
            out = _inner_handle()
            return out;
        finally:
            if isinstance(out, HTTPResponse):
                out.apply(response)
            self.trigger_hook('after_request')
    def _cast(self, out, peek=None):
        if not out:
            if 'Content-Length' not in response:
                response['Content-Length'] = 0
            return []
        if isinstance(out, (tuple, list))\
        and isinstance(out[0], (bytes, unicode)):
            out = out[0][0:0].join(out)
        if isinstance(out, unicode):
            out = out.encode(response.charset)
        if isinstance(out, bytes):
            if 'Content-Length' not in response:
                response['Content-Length'] = len(out)
            return [out]
        if isinstance(out, HTTPError):
            out.apply(response)
            out = self.error_handler.get(out.status_code, self.default_error_handler)(out)
            return self._cast(out)
        if isinstance(out, HTTPResponse):
            out.apply(response)
            return self._cast(out.body)
        if hasattr(out, 'read'):
            if 'wsgi.file_wrapper' in request.environ:
                return request.environ['wsgi.file_wrapper'](out)
            elif hasattr(out, 'close') or not hasattr(out, '__iter__'):
                return WSGIFileWrapper(out)
        try:
            iout = iter(out)
            first = next(iout)
            while not first:
                first = next(iout)
        except StopIteration:
            return self._cast('')
        except HTTPResponse:
            first = _e()
        except (KeyboardInterrupt, SystemExit, MemoryError):
            raise
        except:
            if not self.catchall: raise
            first = HTTPError(500, 'Unhandled exception', _e(), format_exc())
        if isinstance(first, HTTPResponse):
            return self._cast(first)
        elif isinstance(first, bytes):
            new_iter = itertools.chain([first], iout)
        elif isinstance(first, unicode):
            encoder = lambda x: x.encode(response.charset)
            new_iter = imap(encoder, itertools.chain([first], iout))
        else:
            msg = 'Unsupported response type: %s' % type(first)
            return self._cast(HTTPError(500, msg))
        if hasattr(out, 'close'):
            new_iter = _closeiter(new_iter, out.close)
        return new_iter
    def wsgi(self, environ, start_response):
        try:
            out = self._cast(self._handle(environ))
            if response._status_code in (100, 101, 204, 304)\
            or environ['REQUEST_METHOD'] == 'HEAD':
                if hasattr(out, 'close'): out.close()
                out = []
            start_response(response._status_line, response.headerlist)
            return out
        except (KeyboardInterrupt, SystemExit, MemoryError):
            raise
        except:
            if not self.catchall: raise
            err = '<h1>Critical error while processing request: %s</h1>' \
                  % html_escape(environ.get('PATH_INFO', '/'))
            if DEBUG:
                err += '<h2>Error:</h2>\n<pre>\n%s\n</pre>\n' \
                       '<h2>Traceback:</h2>\n<pre>\n%s\n</pre>\n' \
                       % (html_escape(repr(_e())), html_escape(format_exc()))
            environ['wsgi.errors'].write(err)
            headers = [('Content-Type', 'text/html; charset=UTF-8')]
            start_response('500 INTERNAL SERVER ERROR', headers, sys.exc_info())
            return [tob(err)]
    def __call__(self, environ, start_response):
        return self.wsgi(environ, start_response)
    def __enter__(self):
        default_app.push(self)
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        default_app.pop()
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("Attribute %s already defined. Plugin conflict?" % name)
        self.__dict__[name] = value
class BaseRequest(object):
    __slots__ = ('environ', )
    MEMFILE_MAX = 102400
    def __init__(self, environ=None):
        self.environ = {} if environ is None else environ
        self.environ['bottle.request'] = self
    @DictProperty('environ', 'bottle.app', read_only=True)
    def app(self):
        raise RuntimeError('This request is not connected to an application.')
    @DictProperty('environ', 'bottle.route', read_only=True)
    def route(self):
        raise RuntimeError('This request is not connected to a route.')
    @DictProperty('environ', 'route.url_args', read_only=True)
    def url_args(self):
        raise RuntimeError('This request is not connected to a route.')
    @property
    def path(self):
        return '/' + self.environ.get('PATH_INFO', '').lstrip('/')
    @property
    def method(self):
        return self.environ.get('REQUEST_METHOD', 'GET').upper()
    @DictProperty('environ', 'bottle.request.headers', read_only=True)
    def headers(self):
        return WSGIHeaderDict(self.environ)
    def get_header(self, name, default=None):
        return self.headers.get(name, default)
    def get_cookie(self, key, default=None, secret=None):
        value = self.cookies.get(key)
        if secret and value:
            dec = cookie_decode(value, secret)
            return dec[1] if dec and dec[0] == key else default
        return value or default
    @DictProperty('environ', 'bottle.request.query', read_only=True)
    def query(self):
        get = self.environ['bottle.get'] = FormsDict()
        pairs = _parse_qsl(self.environ.get('QUERY_STRING', ''))
        for key, value in pairs:
            get[key] = value
        return get
    @DictProperty('environ', 'bottle.request.forms', read_only=True)
    def forms(self):
        forms = FormsDict()
        for name, item in self.POST.allitems():
            if not isinstance(item, FileUpload):
                forms[name] = item
        return forms
    @DictProperty('environ', 'bottle.request.params', read_only=True)
    def params(self):
        params = FormsDict()
        for key, value in self.query.allitems():
            params[key] = value
        for key, value in self.forms.allitems():
            params[key] = value
        return params
    @DictProperty('environ', 'bottle.request.files', read_only=True)
    def files(self):
        files = FormsDict()
        for name, item in self.POST.allitems():
            if isinstance(item, FileUpload):
                files[name] = item
        return files
    @DictProperty('environ', 'bottle.request.json', read_only=True)
    def json(self):
        ctype = self.environ.get('CONTENT_TYPE', '').lower().split(';')[0]
        if ctype == 'application/json':
            b = self._get_body_string()
            if not b:
                return None
            try:
                return json_loads(b)
            except (ValueError, TypeError):
                raise HTTPError(400, 'Invalid JSON')
        return None
    def _iter_body(self, read, bufsize):
        maxread = max(0, self.content_length)
        while maxread:
            part = read(min(maxread, bufsize))
            if not part: break
            yield part
            maxread -= len(part)
    @staticmethod
    def _iter_chunked(read, bufsize):
        err = HTTPError(400, 'Error while parsing chunked transfer body.')
        rn, sem, bs = tob('\r\n'), tob(';'), tob('')
        while True:
            header = read(1)
            while header[-2:] != rn:
                c = read(1)
                header += c
                if not c: raise err
                if len(header) > bufsize: raise err
            size, _, _ = header.partition(sem)
            try:
                maxread = int(tonat(size.strip()), 16)
            except ValueError:
                raise err
            if maxread == 0: break
            buff = bs
            while maxread > 0:
                if not buff:
                    buff = read(min(maxread, bufsize))
                part, buff = buff[:maxread], buff[maxread:]
                if not part: raise err
                yield part
                maxread -= len(part)
            if read(2) != rn:
                raise err
    @DictProperty('environ', 'bottle.request.body', read_only=True)
    def _body(self):
        try:
            read_func = self.environ['wsgi.input'].read
        except KeyError:
            self.environ['wsgi.input'] = BytesIO()
            return self.environ['wsgi.input']
        body_iter = self._iter_chunked if self.chunked else self._iter_body
        body, body_size, is_temp_file = BytesIO(), 0, False
        for part in body_iter(read_func, self.MEMFILE_MAX):
            body.write(part)
            body_size += len(part)
            if not is_temp_file and body_size > self.MEMFILE_MAX:
                body, tmp = TemporaryFile(mode='w+b'), body
                body.write(tmp.getvalue())
                del tmp
                is_temp_file = True
        self.environ['wsgi.input'] = body
        body.seek(0)
        return body
    def _get_body_string(self):
        clen = self.content_length
        if clen > self.MEMFILE_MAX:
            raise HTTPError(413, 'Request entity too large')
        if clen < 0: clen = self.MEMFILE_MAX + 1
        data = self.body.read(clen)
        if len(data) > self.MEMFILE_MAX:
            raise HTTPError(413, 'Request entity too large')
        return data
    @property
    def body(self):
        self._body.seek(0)
        return self._body
    @property
    def chunked(self):
        return 'chunked' in self.environ.get(
            'HTTP_TRANSFER_ENCODING', '').lower()
    GET = query
    @property
    def url(self):
        return self.urlparts.geturl()
    @DictProperty('environ', 'bottle.request.urlparts', read_only=True)
    def urlparts(self):
        env = self.environ
        http = env.get('HTTP_X_FORWARDED_PROTO') \
             or env.get('wsgi.url_scheme', 'http')
        host = env.get('HTTP_X_FORWARDED_HOST') or env.get('HTTP_HOST')
        if not host:
            host = env.get('SERVER_NAME', '127.0.0.1')
            port = env.get('SERVER_PORT')
            if port and port != ('80' if http == 'http' else '443'):
                host += ':' + port
        path = urlquote(self.fullpath)
        return UrlSplitResult(http, host, path, env.get('QUERY_STRING'), '')
    @property
    def fullpath(self):
        return urljoin(self.script_name, self.path.lstrip('/'))
    @property
    def query_string(self):
        return self.environ.get('QUERY_STRING', '')
    @property
    def script_name(self):
        script_name = self.environ.get('SCRIPT_NAME', '').strip('/')
        return '/' + script_name + '/' if script_name else '/'
    def path_shift(self, shift=1):
        script, path = path_shift(self.environ.get('SCRIPT_NAME', '/'), self.path, shift)
        self['SCRIPT_NAME'], self['PATH_INFO'] = script, path
    @property
    def content_length(self):
        return int(self.environ.get('CONTENT_LENGTH') or -1)
    @property
    def content_type(self):
        return self.environ.get('CONTENT_TYPE', '').lower()
    @property
    def is_xhr(self):
        requested_with = self.environ.get('HTTP_X_REQUESTED_WITH', '')
        return requested_with.lower() == 'xmlhttprequest'
    @property
    def is_ajax(self):
        return self.is_xhr
    @property
    def auth(self):
        basic = parse_auth(self.environ.get('HTTP_AUTHORIZATION', ''))
        if basic: return basic
        ruser = self.environ.get('REMOTE_USER')
        if ruser: return (ruser, None)
        return None
    @property
    def remote_route(self):
        proxy = self.environ.get('HTTP_X_FORWARDED_FOR')
        if proxy: return [ip.strip() for ip in proxy.split(',')]
        remote = self.environ.get('REMOTE_ADDR')
        return [remote] if remote else []
    def copy(self):
        return Request(self.environ.copy())
    def get(self, value, default=None):
        return self.environ.get(value, default)
    def __getitem__(self, key):
        return self.environ[key]
    def __delitem__(self, key):
        self[key] = ""
        del (self.environ[key])
    def __iter__(self):
        return iter(self.environ)
    def __len__(self):
        return len(self.environ)
    def keys(self):
        return self.environ.keys()
    def __setitem__(self, key, value):
        if self.environ.get('bottle.request.readonly'):
            raise KeyError('The environ dictionary is read-only.')
        self.environ[key] = value
        todelete = ()
        if key == 'wsgi.input':
            todelete = ('body', 'forms', 'files', 'params', 'post', 'json')
        elif key == 'QUERY_STRING':
            todelete = ('query', 'params')
        elif key.startswith('HTTP_'):
            todelete = ('headers', 'cookies')
        for key in todelete:
            self.environ.pop('bottle.request.' + key, None)
    def __repr__(self):
        return '<%s: %s %s>' % (self.__class__.__name__, self.method, self.url)
    def __getattr__(self, name):
        try:
            var = self.environ['bottle.request.ext.%s' % name]
            return var.__get__(self) if hasattr(var, '__get__') else var
        except KeyError:
            raise AttributeError('Attribute %r not defined.' % name)
    def __setattr__(self, name, value):
        if name == 'environ': return object.__setattr__(self, name, value)
        key = 'bottle.request.ext.%s' % name
        if key in self.environ:
            raise AttributeError("Attribute already defined: %s" % name)
        self.environ[key] = value
    def __delattr__(self, name, value):
        try:
            del self.environ['bottle.request.ext.%s' % name]
        except KeyError:
            raise AttributeError("Attribute not defined: %s" % name)
def _hkey(s):
    return s.title().replace('_', '-')
class HeaderProperty(object):
    def __init__(self, name, reader=None, writer=str, default=''):
        self.name, self.default = name, default
        self.reader, self.writer = reader, writer
        self.__doc__ = 'Current value of the %r header.' % name.title()
    def __get__(self, obj, _):
        if obj is None: return self
        value = obj.headers.get(self.name, self.default)
        return self.reader(value) if self.reader else value
    def __set__(self, obj, value):
        obj.headers[self.name] = self.writer(value)
    def __delete__(self, obj):
        del obj.headers[self.name]
class BaseResponse(object):
    default_status = 200
    default_content_type = 'text/html; charset=UTF-8'
    bad_headers = { 204: set(('Content-Type', )), 304: set(('Allow', 'Content-Encoding', 'Content-Language', 'Content-Length', 'Content-Range', 'Content-Type', 'Content-Md5', 'Last-Modified')) }
    def __init__(self, body='', status=None, headers=None, **more_headers):
        self._cookies = None
        self._headers = {}
        self.body = body
        self.status = status or self.default_status
        if headers:
            if isinstance(headers, dict):
                headers = headers.items()
            for name, value in headers:
                self.add_header(name, value)
        if more_headers:
            for name, value in more_headers.items():
                self.add_header(name, value)
    def copy(self, cls=None):
        cls = cls or BaseResponse
        assert issubclass(cls, BaseResponse)
        copy = cls()
        copy.status = self.status
        copy._headers = dict((k, v[:]) for (k, v) in self._headers.items())
        if self._cookies:
            copy._cookies = SimpleCookie()
            copy._cookies.load(self._cookies.output(header=''))
        return copy
    def __iter__(self):
        return iter(self.body)
    def close(self):
        if hasattr(self.body, 'close'):
            self.body.close()
    @property
    def status_line(self):
        return self._status_line
    @property
    def status_code(self):
        return self._status_code
    def _set_status(self, status):
        if isinstance(status, int):
            code, status = status, _HTTP_STATUS_LINES.get(status)
        elif ' ' in status:
            status = status.strip()
            code = int(status.split()[0])
        else:
            raise ValueError('String status line without a reason phrase.')
        if not 100 <= code <= 999:
            raise ValueError('Status code out of range.')
        self._status_code = code
        self._status_line = str(status or ('%d Unknown' % code))
    def _get_status(self):
        return self._status_line
    status = property(_get_status, _set_status, None,)
    del _get_status, _set_status
    @property
    def headers(self):
        hdict = HeaderDict()
        hdict.dict = self._headers
        return hdict
    def __contains__(self, name):
        return _hkey(name) in self._headers
    def __delitem__(self, name):
        del self._headers[_hkey(name)]
    def __getitem__(self, name):
        return self._headers[_hkey(name)][-1]
    def __setitem__(self, name, value):
        self._headers[_hkey(name)] = [value if isinstance(value, unicode) else
                                      str(value)]
    def get_header(self, name, default=None):
        return self._headers.get(_hkey(name), [default])[-1]
    def set_header(self, name, value):
        self._headers[_hkey(name)] = [value if isinstance(value, unicode)
                                            else str(value)]
    def add_header(self, name, value):
        self._headers.setdefault(_hkey(name), []).append(
            value if isinstance(value, unicode) else str(value))
    def iter_headers(self):
        return self.headerlist
    @property
    def headerlist(self):
        out = []
        headers = list(self._headers.items())
        if 'Content-Type' not in self._headers:
            headers.append(('Content-Type', [self.default_content_type]))
        if self._status_code in self.bad_headers:
            bad_headers = self.bad_headers[self._status_code]
            headers = [h for h in headers if h[0] not in bad_headers]
        out += [(name, val) for (name, vals) in headers for val in vals]
        if self._cookies:
            for c in self._cookies.values():
                out.append(('Set-Cookie', c.OutputString()))
        if py3k:
            return [(k, v.encode('utf8').decode('latin1')) for (k, v) in out]
        else:
            return [(k, v.encode('utf8') if isinstance(v, unicode) else v)
                    for (k, v) in out]
    content_type = HeaderProperty('Content-Type')
    content_length = HeaderProperty('Content-Length', reader=int)
    expires = HeaderProperty( 'Expires', reader=lambda x: datetime.utcfromtimestamp(parse_date(x)), writer=lambda x: http_date(x))
    @property
    def charset(self, default='UTF-8'):
        if 'charset=' in self.content_type:
            return self.content_type.split('charset=')[-1].split(';')[0].strip()
        return default
    def __repr__(self):
        out = ''
        for name, value in self.headerlist:
            out += '%s: %s\n' % (name.title(), value.strip())
        return out
def _local_property():
    ls = threading.local()
    def fget(_):
        try:
            return ls.var
        except AttributeError:
            raise RuntimeError("Request context not initialized.")
    def fset(_, value):
        ls.var = value
    def fdel(_):
        del ls.var
    return property(fget, fset, fdel, 'Thread-local property')
class LocalRequest(BaseRequest):
    bind = BaseRequest.__init__
    environ = _local_property()
class LocalResponse(BaseResponse):
    bind = BaseResponse.__init__
    _status_line = _local_property()
    _status_code = _local_property()
    _cookies = _local_property()
    _headers = _local_property()
    body = _local_property()
Request = BaseRequest
Response = BaseResponse
class HTTPResponse(Response, BottleException):
    def __init__(self, body='', status=None, headers=None, **more_headers):
        super(HTTPResponse, self).__init__(body, status, headers, **more_headers)
    def apply(self, other):
        other._status_code = self._status_code
        other._status_line = self._status_line
        other._headers = self._headers
        other._cookies = self._cookies
        other.body = self.body
class HTTPError(HTTPResponse):
    default_status = 500
    def __init__(self, status=None, body=None, exception=None, traceback=None, **more_headers):
        self.exception = exception
        self.traceback = traceback
        super(HTTPError, self).__init__(body, status, **more_headers)
class PluginError(BottleException):
    pass
class JSONPlugin(object):
    name = 'json'
    api = 2
    def __init__(self, json_dumps=json_dumps):
        self.json_dumps = json_dumps
    def apply(self, callback, _):
        dumps = self.json_dumps
        if not dumps: return callback
        def wrapper(*a, **ka):
            try:
                rv = callback(*a, **ka)
            except HTTPError:
                rv = _e()
            if isinstance(rv, dict):
                json_response = dumps(rv)
                response.content_type = 'application/json'
                return json_response
            elif isinstance(rv, HTTPResponse) and isinstance(rv.body, dict):
                rv.body = dumps(rv.body)
                rv.content_type = 'application/json'
            return rv
        return wrapper
class _ImportRedirect(object):
    def __init__(self, name, impmask):
        self.name = name
        self.impmask = impmask
        self.module = sys.modules.setdefault(name, imp.new_module(name))
        self.module.__dict__.update({ '__file__': __file__, '__path__': [], '__all__': [], '__loader__': self })
        sys.meta_path.append(self)
    def find_module(self, fullname, path=None):
        if '.' not in fullname: return
        packname = fullname.rsplit('.', 1)[0]
        if packname != self.name: return
        return self
    def load_module(self, fullname):
        if fullname in sys.modules: return sys.modules[fullname]
        modname = fullname.rsplit('.', 1)[1]
        realname = self.impmask % modname
        __import__(realname)
        module = sys.modules[fullname] = sys.modules[realname]
        setattr(self.module, modname, module)
        module.__loader__ = self
        return module
class MultiDict(DictMixin):
    def __init__(self, *a, **k):
        self.dict = dict((k, [v]) for (k, v) in dict(*a, **k).items())
    def __len__(self):
        return len(self.dict)
    def __iter__(self):
        return iter(self.dict)
    def __contains__(self, key):
        return key in self.dict
    def __delitem__(self, key):
        del self.dict[key]
    def __getitem__(self, key):
        return self.dict[key][-1]
    def __setitem__(self, key, value):
        self.append(key, value)
    def keys(self):
        return self.dict.keys()
    if py3k:
        def values(self):
            return (v[-1] for v in self.dict.values())
        def items(self):
            return ((k, v[-1]) for k, v in self.dict.items())
        def allitems(self):
            return ((k, v) for k, vl in self.dict.items() for v in vl)
        iterkeys = keys
        itervalues = values
        iteritems = items
        iterallitems = allitems
    else:
        def values(self):
            return [v[-1] for v in self.dict.values()]
        def items(self):
            return [(k, v[-1]) for k, v in self.dict.items()]
        def iterkeys(self):
            return self.dict.iterkeys()
        def itervalues(self):
            return (v[-1] for v in self.dict.itervalues())
        def iteritems(self):
            return ((k, v[-1]) for k, v in self.dict.iteritems())
        def iterallitems(self):
            return ((k, v) for k, vl in self.dict.iteritems() for v in vl)
        def allitems(self):
            return [(k, v) for k, vl in self.dict.iteritems() for v in vl]
    def get(self, key, default=None, index=-1, type=None):
        try:
            val = self.dict[key][index]
            return type(val) if type else val
        except Exception:
            pass
        return default
    def append(self, key, value):
        self.dict.setdefault(key, []).append(value)
    def replace(self, key, value):
        self.dict[key] = [value]
    def getall(self, key):
        return self.dict.get(key) or []
    getone = get
    getlist = getall
class FormsDict(MultiDict):
    input_encoding = 'utf8'
    recode_unicode = True
    def _fix(self, s, encoding=None):
        if isinstance(s, unicode) and self.recode_unicode:
            return s.encode('latin1').decode(encoding or self.input_encoding)
        elif isinstance(s, bytes):
            return s.decode(encoding or self.input_encoding)
        else:
            return s
    def decode(self, encoding=None):
        copy = FormsDict()
        enc = copy.input_encoding = encoding or self.input_encoding
        copy.recode_unicode = False
        for key, value in self.allitems():
            copy.append(self._fix(key, enc), self._fix(value, enc))
        return copy
    def getunicode(self, name, default=None, encoding=None):
        try:
            return self._fix(self[name], encoding)
        except (UnicodeError, KeyError):
            return default
    def __getattr__(self, name, default=unicode()):
        if name.startswith('__') and name.endswith('__'):
            return super(FormsDict, self).__getattr__(name)
        return self.getunicode(name, default=default)
class HeaderDict(MultiDict):
    def __init__(self, *a, **ka):
        self.dict = {}
        if a or ka: self.update(*a, **ka)
    def __contains__(self, key):
        return _hkey(key) in self.dict
    def __delitem__(self, key):
        del self.dict[_hkey(key)]
    def __getitem__(self, key):
        return self.dict[_hkey(key)][-1]
    def __setitem__(self, key, value):
        self.dict[_hkey(key)] = [value if isinstance(value, unicode) else str(value)]
    def append(self, key, value):
        self.dict.setdefault(_hkey(key), []).append(value if isinstance(value, unicode) else str(value))
    def replace(self, key, value):
        self.dict[_hkey(key)] = [value if isinstance(value, unicode) else str(value)]
    def getall(self, key):
        return self.dict.get(_hkey(key)) or []
    def get(self, key, default=None, index=-1):
        return MultiDict.get(self, _hkey(key), default, index)
    def filter(self, names):
        for name in [_hkey(n) for n in names]:
            if name in self.dict:
                del self.dict[name]
class WSGIHeaderDict(DictMixin):
    cgikeys = ('CONTENT_TYPE', 'CONTENT_LENGTH')
    def __init__(self, environ):
        self.environ = environ
    def _ekey(self, key):
        key = key.replace('-', '_').upper()
        if key in self.cgikeys:
            return key
        return 'HTTP_' + key
    def raw(self, key, default=None):
        return self.environ.get(self._ekey(key), default)
    def __getitem__(self, key):
        val = self.environ[self._ekey(key)]
        if py3k:
            if isinstance(val, unicode):
                val = val.encode('latin1').decode('utf8')
            else:
                val = val.decode('utf8')
        return val
    def __setitem__(self, key, value):
        raise TypeError("%s is read-only." % self.__class__)
    def __delitem__(self, key):
        raise TypeError("%s is read-only." % self.__class__)
    def __iter__(self):
        for key in self.environ:
            if key[:5] == 'HTTP_':
                yield _hkey(key[5:])
            elif key in self.cgikeys:
                yield _hkey(key)
    def keys(self):
        return [x for x in self]
    def __len__(self):
        return len(self.keys())
    def __contains__(self, key):
        return self._ekey(key) in self.environ
class ConfigDict(dict):
    __slots__ = ('_meta', '_change_listener', '_fallbacks')
    def __init__(self):
        self._meta = {}
        self._change_listener = []
        self._fallbacks = []
    def load_module(self, path, squash):
        config_obj = __import__(path)
        obj = dict([(key, getattr(config_obj, key))
                for key in dir(config_obj) if key.isupper()])
        if squash:
            self.load_dict(obj)
        else:
            self.update(obj)
        return self
    def load_config(self, filename):
        conf = ConfigParser()
        conf.read(filename)
        for section in conf.sections():
            for key, value in conf.items(section):
                if section not in ('DEFAULT', 'bottle'):
                    key = section + '.' + key
                self[key] = value
        return self
    def load_dict(self, source, namespace=''):
        for key, value in source.items():
            if isinstance(key, basestring):
                nskey = (namespace + '.' + key).strip('.')
                if isinstance(value, dict):
                    self.load_dict(value, namespace=nskey)
                else:
                    self[nskey] = value
            else:
                raise TypeError('Key has type %r (not a string)' % type(key))
        return self
    def update(self, *a, **ka):
        prefix = ''
        if a and isinstance(a[0], basestring):
            prefix = a[0].strip('.') + '.'
            a = a[1:]
        for key, value in dict(*a, **ka).items():
            self[prefix + key] = value
    def setdefault(self, key, value):
        if key not in self:
            self[key] = value
        return self[key]
    def __setitem__(self, key, value):
        if not isinstance(key, basestring):
            raise TypeError('Key has type %r (not a string)' % type(key))
        value = self.meta_get(key, 'filter', lambda x: x)(value)
        if key in self and self[key] is value:
            return
        self._on_change(key, value)
        dict.__setitem__(self, key, value)
    def __delitem__(self, key):
        self._on_change(key, None)
        dict.__delitem__(self, key)
    def __missing__(self, key):
        for fallback in self._fallbacks:
            if key in fallback:
                value = self[key] = fallback[key]
                self.meta_set(key, 'fallback', fallback)
                return value
        raise KeyError(key)
    def _on_change(self, key, value):
        for cb in self._change_listener:
            if cb(self, key, value):
                return True
    def _add_change_listener(self, func):
        self._change_listener.append(func)
        return func
    def _set_fallback(self, fallback):
        self._fallbacks.append(fallback)
        @fallback._add_change_listener
        def fallback_update(conf, key, value):
            if self.meta_get(key, 'fallback') is conf:
                self.meta_set(key, 'fallback', None)
                dict.__delitem__(self, key)
        @self._add_change_listener
        def self_update(conf, key, value):
            if conf.meta_get(key, 'fallback'):
                conf.meta_set(key, 'fallback', None)
    def meta_get(self, key, metafield, default=None):
        return self._meta.get(key, {}).get(metafield, default)
    def meta_set(self, key, metafield, value):
        self._meta.setdefault(key, {})[metafield] = value
    def meta_list(self, key):
        return self._meta.get(key, {}).keys()
class AppStack(list):
    def __call__(self):
        return self[-1]
    def push(self, value=None):
        if not isinstance(value, Bottle):
            value = Bottle()
        self.append(value)
        return value
class WSGIFileWrapper(object):
    def __init__(self, fp, buffer_size=1024 * 64):
        self.fp, self.buffer_size = fp, buffer_size
        for attr in ('fileno', 'close', 'read', 'readlines', 'tell', 'seek'):
            if hasattr(fp, attr): setattr(self, attr, getattr(fp, attr))
    def __iter__(self):
        buff, read = self.buffer_size, self.read
        while True:
            part = read(buff)
            if not part: return
            yield part
class _closeiter(object):
    def __init__(self, iterator, close=None):
        self.iterator = iterator
        self.close_callbacks = makelist(close)
    def __iter__(self):
        return iter(self.iterator)
    def close(self):
        for func in self.close_callbacks:
            func()
class ResourceManager(object):
    def __init__(self, base='./', opener=open, cachemode='all'):
        self.opener = opener
        self.base = base
        self.cachemode = cachemode
        self.path = []
        self.cache = {}
    def add_path(self, path, base=None, index=None, create=False):
        base = os.path.abspath(os.path.dirname(base or self.base))
        path = os.path.abspath(os.path.join(base, os.path.dirname(path)))
        path += os.sep
        if path in self.path:
            self.path.remove(path)
        if create and not os.path.isdir(path):
            os.makedirs(path)
        if index is None:
            self.path.append(path)
        else:
            self.path.insert(index, path)
        self.cache.clear()
        return os.path.exists(path)
    def __iter__(self):
        search = self.path[:]
        while search:
            path = search.pop()
            if not os.path.isdir(path): continue
            for name in os.listdir(path):
                full = os.path.join(path, name)
                if os.path.isdir(full): search.append(full)
                else: yield full
    def lookup(self, name):
        if name not in self.cache or DEBUG:
            for path in self.path:
                fpath = os.path.join(path, name)
                if os.path.isfile(fpath):
                    if self.cachemode in ('all', 'found'):
                        self.cache[name] = fpath
                    return fpath
            if self.cachemode == 'all':
                self.cache[name] = None
        return self.cache[name]
    def open(self, name, mode='r', *args, **kwargs):
        fname = self.lookup(name)
        if not fname: raise IOError("Resource %r not found." % name)
        return self.opener(fname, mode=mode, *args, **kwargs)
class FileUpload(object):
    def __init__(self, fileobj, name, filename, headers=None):
        self.file = fileobj
        self.name = name
        self.raw_filename = filename
        self.headers = HeaderDict(headers) if headers else HeaderDict()
    content_type = HeaderProperty('Content-Type')
    content_length = HeaderProperty('Content-Length', reader=int, default=-1)
    @cached_property
    def filename(self):
        fname = self.raw_filename
        if not isinstance(fname, unicode):
            fname = fname.decode('utf8', 'ignore')
        fname = normalize('NFKD', fname)
        fname = fname.encode('ASCII', 'ignore').decode('ASCII')
        fname = os.path.basename(fname.replace('\\', os.path.sep))
        fname = re.sub(r'[^a-zA-Z0-9-_.\s]', '', fname).strip()
        fname = re.sub(r'[-\s]+', '-', fname).strip('.-')
        return fname[:255] or 'empty'
    def _copy_file(self, fp, chunk_size=2 ** 16):
        read, write, offset = self.file.read, fp.write, self.file.tell()
        while 1:
            buf = read(chunk_size)
            if not buf: break
            write(buf)
        self.file.seek(offset)
    def save(self, destination, overwrite=False, chunk_size=2 ** 16):
        if isinstance(destination, basestring):
            if os.path.isdir(destination):
                destination = os.path.join(destination, self.filename)
            if not overwrite and os.path.exists(destination):
                raise IOError('File exists.')
            with open(destination, 'wb') as fp:
                self._copy_file(fp, chunk_size)
        else:
            self._copy_file(destination, chunk_size)
def abort(code=500, text='Unknown Error.'):
    raise HTTPError(code, text)
def redirect(url, code=None):
    if not code:
        code = 303 if request.get('SERVER_PROTOCOL') == "HTTP/1.1" else 302
    res = response.copy(cls=HTTPResponse)
    res.status = code
    res.body = ""
    res.set_header('Location', urljoin(request.url, url))
    raise res
def _file_iter_range(fp, offset, bytes, maxread=1024 * 1024):
    fp.seek(offset)
    while bytes > 0:
        part = fp.read(min(bytes, maxread))
        if not part: break
        bytes -= len(part)
        yield part
def static_file(filename, root,mimetype='auto', download=False, charset='UTF-8'):
    root = os.path.abspath(root) + os.sep
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    headers = dict()
    if not filename.startswith(root):
        return HTTPError(403, "Access denied.")
    if not os.path.exists(filename) or not os.path.isfile(filename):
        return HTTPError(404, "File does not exist.")
    if not os.access(filename, os.R_OK):
        return HTTPError(403, "You do not have permission to access this file.")
    if mimetype == 'auto':
        if download and download != True:
            mimetype, encoding = mimetypes.guess_type(download)
        else:
            mimetype, encoding = mimetypes.guess_type(filename)
        if encoding: headers['Content-Encoding'] = encoding
    if mimetype:
        if (mimetype[:5] == 'text/' or mimetype == 'application/javascript') and charset and 'charset' not in mimetype:
            mimetype += '; charset=%s' % charset
        headers['Content-Type'] = mimetype
    if download:
        download = os.path.basename(filename if download == True else download)
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download
    stats = os.stat(filename)
    headers['Content-Length'] = clen = stats.st_size
    lm = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(stats.st_mtime))
    headers['Last-Modified'] = lm
    ims = request.environ.get('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
    if ims is not None and ims >= int(stats.st_mtime):
        headers['Date'] = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
        return HTTPResponse(status=304, **headers)
    body = '' if request.method == 'HEAD' else open(filename, 'rb')
    headers["Accept-Ranges"] = "bytes"
    ranges = request.environ.get('HTTP_RANGE')
    if 'HTTP_RANGE' in request.environ:
        ranges = list(parse_range_header(request.environ['HTTP_RANGE'], clen))
        if not ranges:
            return HTTPError(416, "Requested Range Not Satisfiable")
        offset, end = ranges[0]
        headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
        headers["Content-Length"] = str(end - offset)
        if body: body = _file_iter_range(body, offset, end - offset)
        return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)
def debug(mode=True):
    global DEBUG
    if mode: warnings.simplefilter('default')
    DEBUG = bool(mode)
def http_date(value):
    if isinstance(value, (datedate, datetime)):
        value = value.utctimetuple()
    elif isinstance(value, (int, float)):
        value = time.gmtime(value)
    if not isinstance(value, basestring):
        value = time.strftime("%a, %d %b %Y %H:%M:%S GMT", value)
    return value
def parse_date(ims):
    try:
        ts = email.utils.parsedate_tz(ims)
        return time.mktime(ts[:8] + (0, )) - (ts[9] or 0) - time.timezone
    except (TypeError, ValueError, IndexError, OverflowError):
        return None
def parse_auth(header):
    try:
        method, data = header.split(None, 1)
        if method.lower() == 'basic':
            user, pwd = touni(base64.b64decode(tob(data))).split(':', 1)
            return user, pwd
    except (KeyError, ValueError):
        return None
def parse_range_header(header, maxlen=0):
    if not header or header[:6] != 'bytes=': return
    ranges = [r.split('-', 1) for r in header[6:].split(',') if '-' in r]
    for start, end in ranges:
        try:
            if not start:
                start, end = max(0, maxlen - int(end)), maxlen
            elif not end:
                start, end = int(start), maxlen
            else:
                start, end = int(start), min(int(end) + 1, maxlen)
            if 0 <= start < end <= maxlen:
                yield start, end
        except ValueError:
            pass
def _parse_qsl(qs):
    r = []
    for pair in qs.replace(';', '&').split('&'):
        if not pair: continue
        nv = pair.split('=', 1)
        if len(nv) != 2: nv.append('')
        key = urlunquote(nv[0].replace('+', ' '))
        value = urlunquote(nv[1].replace('+', ' '))
        r.append((key, value))
    return r
def _lscmp(a, b):
    return not sum(0 if x == y else 1
                   for x, y in zip(a, b)) and len(a) == len(b)
def html_escape(string):
    return string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')\
                 .replace('"', '&quot;').replace("'", '&#039;')
def html_quote(string):
    return '"%s"' % html_escape(string).replace('\n', '&#10;')\
                    .replace('\r', '&#13;').replace('\t', '&#9;')
def yieldroutes(func):
    path = '/' + func.__name__.replace('__', '/').lstrip('/')
    spec = getargspec(func)
    argc = len(spec[0]) - len(spec[3] or [])
    path += ('/<%s>' * argc) % tuple(spec[0][:argc])
    yield path
    for arg in spec[0][argc:]:
        path += '/<%s>' % arg
        yield path
def path_shift(script_name, path_info, shift=1):
    if shift == 0: return script_name, path_info
    pathlist = path_info.strip('/').split('/')
    scriptlist = script_name.strip('/').split('/')
    if pathlist and pathlist[0] == '': pathlist = []
    if scriptlist and scriptlist[0] == '': scriptlist = []
    if 0 < shift <= len(pathlist):
        moved = pathlist[:shift]
        scriptlist = scriptlist + moved
        pathlist = pathlist[shift:]
    elif 0 > shift >= -len(scriptlist):
        moved = scriptlist[shift:]
        pathlist = moved + pathlist
        scriptlist = scriptlist[:shift]
    else:
        empty = 'SCRIPT_NAME' if shift < 0 else 'PATH_INFO'
        raise AssertionError("Cannot shift. Nothing left from %s" % empty)
    new_script_name = '/' + '/'.join(scriptlist)
    new_path_info = '/' + '/'.join(pathlist)
    if path_info.endswith('/') and pathlist: new_path_info += '/'
    return new_script_name, new_path_info
def auth_basic(check, realm="private", text="Access denied"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*a, **ka):
            user, password = request.auth or (None, None)
            if user is None or not check(user, password):
                err = HTTPError(401, text)
                err.add_header('WWW-Authenticate', 'Basic realm="%s"' % realm)
                return err
            return func(*a, **ka)
        return wrapper
    return decorator
def make_default_app_wrapper(name):
    @functools.wraps(getattr(Bottle, name))
    def wrapper(*a, **ka):
        return getattr(app(), name)(*a, **ka)
    return wrapper
route     = make_default_app_wrapper('route')
get       = make_default_app_wrapper('get')
delete    = make_default_app_wrapper('delete')
patch     = make_default_app_wrapper('patch')
error     = make_default_app_wrapper('error')
mount     = make_default_app_wrapper('mount')
hook      = make_default_app_wrapper('hook')
install   = make_default_app_wrapper('install')
uninstall = make_default_app_wrapper('uninstall')
url       = make_default_app_wrapper('get_url')
class ServerAdapter(object):
    quiet = False
    def __init__(self, host='127.0.0.1', port=8080, **options):
        self.options = options
        self.host = host
        self.port = int(port)
    def run(self, handler):
        pass
    def __repr__(self):
        args = ', '.join(['%s=%s' % (k, repr(v))
                          for k, v in self.options.items()])
        return "%s(%s)" % (self.__class__.__name__, args)
class WSGIRefServer(ServerAdapter):
    def run(self, app):
        from wsgiref.simple_server import make_server
        from wsgiref.simple_server import WSGIRequestHandler, WSGIServer
        import socket
        class FixedHandler(WSGIRequestHandler):
            def address_string(self):
                return self.client_address[0]
            def log_request(*args, **kw):
                if not self.quiet:
                    return WSGIRequestHandler.log_request(*args, **kw)
        handler_cls = self.options.get('handler_class', FixedHandler)
        server_cls = self.options.get('server_class', WSGIServer)
        if ':' in self.host:
            if getattr(server_cls, 'address_family') == socket.AF_INET:
                class server_cls(server_cls):
                    address_family = socket.AF_INET6
        self.srv = make_server(self.host, self.port, app, server_cls, handler_cls)
        self.port = self.srv.server_port
        try:
            self.srv.serve_forever()
        except KeyboardInterrupt:
            self.srv.server_close()
            raise
server_names = {'wsgiref': WSGIRefServer}
def load(target, **namespace):
    module, target = target.split(":", 1) if ':' in target else (target, None)
    if module not in sys.modules: __import__(module)
    if not target: return sys.modules[module]
    if target.isalnum(): return getattr(sys.modules[module], target)
    package_name = module.split('.')[0]
    namespace[package_name] = sys.modules[package_name]
    return eval('%s.%s' % (module, target), namespace)
def load_app(target):
    global NORUN
    NORUN, nr_old = True, NORUN
    tmp = default_app.push()
    try:
        rv = load(target)
        return rv if callable(rv) else tmp
    finally:
        default_app.remove(tmp)
        NORUN = nr_old
_debug = debug
def run(app=None, server='wsgiref', host='127.0.0.1', port=8080, interval=1, reloader=False, quiet=False, plugins=None, debug=None, config=None, **kargs):
    if NORUN: return
    if reloader and not os.environ.get('BOTTLE_CHILD'):
        import subprocess
        lockfile = None
        try:
            fd, lockfile = tempfile.mkstemp(prefix='bottle.', suffix='.lock')
            os.close(fd)
            while os.path.exists(lockfile):
                args = [sys.executable] + sys.argv
                environ = os.environ.copy()
                environ['BOTTLE_CHILD'] = 'true'
                environ['BOTTLE_LOCKFILE'] = lockfile
                p = subprocess.Popen(args, env=environ)
                while p.poll() is None:
                    os.utime(lockfile, None)
                    time.sleep(interval)
                if p.poll() != 3:
                    if os.path.exists(lockfile): os.unlink(lockfile)
                    sys.exit(p.poll())
        except KeyboardInterrupt:
            pass
        finally:
            if os.path.exists(lockfile):
                os.unlink(lockfile)
        return
    try:
        if debug is not None: _debug(debug)
        app = app or default_app()
        if isinstance(app, basestring):
            app = load_app(app)
        if not callable(app):
            raise ValueError("Application is not callable: %r" % app)
        for plugin in plugins or []:
            if isinstance(plugin, basestring):
                plugin = load(plugin)
            app.install(plugin)
        if config:
            app.config.update(config)
        if server in server_names:
            server = server_names.get(server)
        if isinstance(server, basestring):
            server = load(server)
        if isinstance(server, type):
            server = server(host=host, port=port, **kargs)
        if not isinstance(server, ServerAdapter):
            raise ValueError("Unknown or unsupported server: %r" % server)
        server.quiet = server.quiet or quiet
        if not server.quiet:
            _stderr("Bottle server starting up (using %s)...\n" %  (repr(server)))
            _stderr("Listening on http://%s:%d/\n" % (server.host, server.port))
        if reloader:
            lockfile = os.environ.get('BOTTLE_LOCKFILE')
            bgcheck = FileCheckerThread(lockfile, interval)
            with bgcheck:
                server.run(app)
            if bgcheck.status == 'reload':
                sys.exit(3)
        else:
            server.run(app)
    except KeyboardInterrupt:
        pass
    except (SystemExit, MemoryError):
        raise
    except:
        if not reloader: raise
        if not getattr(server, 'quiet', quiet):
            print_exc()
        time.sleep(interval)
        sys.exit(3)
class FileCheckerThread(threading.Thread):
    def __init__(self, lockfile, interval):
        threading.Thread.__init__(self)
        self.daemon = True
        self.lockfile, self.interval = lockfile, interval
        self.status = None
    def run(self):
        exists = os.path.exists
        mtime = lambda p: os.stat(p).st_mtime
        files = dict()
        for module in list(sys.modules.values()):
            path = getattr(module, '__file__', '')
            if path[-4:] in ('.pyo', '.pyc'): path = path[:-1]
            if path and exists(path): files[path] = mtime(path)
        while not self.status:
            if not exists(self.lockfile)\
            or mtime(self.lockfile) < time.time() - self.interval - 5:
                self.status = 'error'
                thread.interrupt_main()
            for path, lmtime in list(files.items()):
                if not exists(path) or mtime(path) > lmtime:
                    self.status = 'reload'
                    thread.interrupt_main()
                    break
            time.sleep(self.interval)
    def __enter__(self):
        self.start()
    def __exit__(self, exc_type, *_):
        if not self.status: self.status = 'exit'
        self.join()
        return exc_type is not None and issubclass(exc_type, KeyboardInterrupt)
class TemplateError(HTTPError):
    def __init__(self, message):
        HTTPError.__init__(self, 500, message)
class BaseTemplate(object):
    extensions = ['tpl', 'html', 'thtml', 'stpl']
    settings = {}
    defaults = {}
    def __init__(self, source=None,  name=None, lookup=None, encoding='utf8', **settings):
        self.name = name
        self.source = source.read() if hasattr(source, 'read') else source
        self.filename = source.filename if hasattr(source, 'filename') else None
        self.lookup = [os.path.abspath(x) for x in lookup] if lookup else []
        self.encoding = encoding
        self.settings = self.settings.copy()
        self.settings.update(settings)
        if not self.source and self.name:
            self.filename = self.search(self.name, self.lookup)
            if not self.filename:
                raise TemplateError('Template %s not found.' % repr(name))
        if not self.source and not self.filename:
            raise TemplateError('No template specified.')
        self.prepare(**self.settings)
    @classmethod
    def search(cls, name, lookup=None):
        if not lookup:
            raise depr(0, 12, "Empty template lookup path.", "Configure a template lookup path.")
        if os.path.isabs(name):
            raise depr(0, 12, "Use of absolute path for template name.", "Refer to templates with names or paths relative to the lookup path.")
        for spath in lookup:
            spath = os.path.abspath(spath) + os.sep
            fname = os.path.abspath(os.path.join(spath, name))
            if not fname.startswith(spath): continue
            if os.path.isfile(fname): return fname
            for ext in cls.extensions:
                if os.path.isfile('%s.%s' % (fname, ext)):
                    return '%s.%s' % (fname, ext)
    @classmethod
    def global_config(cls, key, *args):
        if args:
            cls.settings = cls.settings.copy()
            cls.settings[key] = args[0]
        else:
            return cls.settings[key]
    def prepare(self, **options):
        raise NotImplementedError
    def render(self, *args, **kwargs):
        raise NotImplementedError
class SimpleTemplate(BaseTemplate):
    def prepare(self,escape_func=html_escape, noescape=False, syntax=None, **ka):
        self.cache = {}
        enc = self.encoding
        self._str = lambda x: touni(x, enc)
        self._escape = lambda x: escape_func(touni(x, enc))
        self.syntax = syntax
        if noescape:
            self._str, self._escape = self._escape, self._str
    @cached_property
    def co(self):
        return compile(self.code, self.filename or '<string>', 'exec')
    @cached_property
    def code(self):
        source = self.source
        if not source:
            with open(self.filename, 'rb') as f:
                source = f.read()
        try:
            source, encoding = touni(source), 'utf8'
        except UnicodeError:
            raise depr(0, 11, 'Unsupported template encodings.', 'Use utf-8 for templates.')
        parser = StplParser(source, encoding=encoding, syntax=self.syntax)
        code = parser.translate()
        self.encoding = parser.encoding
        return code
    def _rebase(self, _env, _name=None, **kwargs):
        _env['_rebase'] = (_name, kwargs)
    def _include(self, _env, _name=None, **kwargs):
        env = _env.copy()
        env.update(kwargs)
        if _name not in self.cache:
            self.cache[_name] = self.__class__(name=_name, lookup=self.lookup)
        return self.cache[_name].execute(env['_stdout'], env)
    def execute(self, _stdout, kwargs):
        env = self.defaults.copy()
        env.update(kwargs)
        env.update({ '_stdout': _stdout, '_printlist': _stdout.extend, 'include': functools.partial(self._include, env), 'rebase': functools.partial(self._rebase, env), '_rebase': None, '_str': self._str, '_escape': self._escape, 'get': env.get, 'setdefault': env.setdefault, 'defined': env.__contains__ })
        eval(self.co, env)
        if env.get('_rebase'):
            subtpl, rargs = env.pop('_rebase')
            rargs['base'] = ''.join(_stdout)
            del _stdout[:]
            return self._include(env, subtpl, **rargs)
        return env
    def render(self, *args, **kwargs):
        env = {}
        stdout = []
        for dictarg in args:
            env.update(dictarg)
        env.update(kwargs)
        self.execute(stdout, env)
        return ''.join(stdout)
class StplSyntaxError(TemplateError):
    pass
class StplParser(object):
    _re_cache = {}
    _re_tok = _re_inl = r'''((?mx)
        [urbURB]*
        (?:  ''(?!')
            |""(?!")
            |'{6}
            |"{6}
            |'(?:[^\\']|\\.)+?'
            |"(?:[^\\"]|\\.)+?"
            |'{3}(?:[^\\]|\\.|\n)+?'{3}
            |"{3}(?:[^\\]|\\.|\n)+?"{3}
        )
    )'''
    _re_inl = _re_tok.replace(r'|\n', '')
    _re_tok += r'''
        |(\#.*)
        |([\[\{\(])
        |([\]\}\)])
        |^([\ \t]*(?:if|for|while|with|try|def|class)\b)
        |^([\ \t]*(?:elif|else|except|finally)\b)
        |((?:^|;)[\ \t]*end[\ \t]*(?=(?:%(block_close)s[\ \t]*)?\r?$|;|\#))
        |(%(block_close)s[\ \t]*(?=\r?$))
        |(\r?\n)
    '''
    _re_split = r'''(?m)^[ \t]*(\\?)((%(line_start)s)|(%(block_start)s))'''
    _re_inl = r'''%%(inline_start)s((?:%s|[^'"\n]+?)*?)%%(inline_end)s''' % _re_inl
    default_syntax = '<% %> % {{ }}'
    def __init__(self, source, syntax=None, encoding='utf8'):
        self.source, self.encoding = touni(source, encoding), encoding
        self.set_syntax(syntax or self.default_syntax)
        self.code_buffer, self.text_buffer = [], []
        self.lineno, self.offset = 1, 0
        self.indent, self.indent_mod = 0, 0
        self.paren_depth = 0
    def get_syntax(self):
        return self._syntax
    def set_syntax(self, syntax):
        self._syntax = syntax
        self._tokens = syntax.split()
        if not syntax in self._re_cache:
            names = 'block_start block_close line_start inline_start inline_end'
            etokens = map(re.escape, self._tokens)
            pattern_vars = dict(zip(names.split(), etokens))
            patterns = (self._re_split, self._re_tok, self._re_inl)
            patterns = [re.compile(p % pattern_vars) for p in patterns]
            self._re_cache[syntax] = patterns
        self.re_split, self.re_tok, self.re_inl = self._re_cache[syntax]
    syntax = property(get_syntax, set_syntax)
    def translate(self):
        if self.offset: raise RuntimeError('Parser is a one time instance.')
        while True:
            m = self.re_split.search(self.source, pos=self.offset)
            if m:
                text = self.source[self.offset:m.start()]
                self.text_buffer.append(text)
                self.offset = m.end()
                if m.group(1):
                    line, sep, _ = self.source[self.offset:].partition('\n')
                    self.text_buffer.append(self.source[m.start():m.start(1)] + m.group(2) + line + sep)
                    self.offset += len(line + sep)
                    continue
                self.flush_text()
                self.offset += self.read_code(self.source[self.offset:], multiline=bool(m.group(4)))
            else:
                break
        self.text_buffer.append(self.source[self.offset:])
        self.flush_text()
        return ''.join(self.code_buffer)
    def read_code(self, pysource, multiline):
        code_line, comment = '', ''
        offset = 0
        while True:
            m = self.re_tok.search(pysource, pos=offset)
            if not m:
                code_line += pysource[offset:]
                offset = len(pysource)
                self.write_code(code_line.strip(), comment)
                break
            code_line += pysource[offset:m.start()]
            offset = m.end()
            _str, _com, _po, _pc, _blk1, _blk2, _end, _cend, _nl = m.groups()
            if self.paren_depth > 0 and (_blk1 or _blk2):
                code_line += _blk1 or _blk2
                continue
            if _str:
                code_line += _str
            elif _com:
                comment = _com
                if multiline and _com.strip().endswith(self._tokens[1]):
                    multiline = False
            elif _po:
                self.paren_depth += 1
                code_line += _po
            elif _pc:
                if self.paren_depth > 0:
                    self.paren_depth -= 1
                code_line += _pc
            elif _blk1:
                code_line, self.indent_mod = _blk1, -1
                self.indent += 1
            elif _blk2:
                code_line, self.indent_mod = _blk2, -1
            elif _end:
                self.indent -= 1
            elif _cend:
                if multiline: multiline = False
                else: code_line += _cend
            else:
                self.write_code(code_line.strip(), comment)
                self.lineno += 1
                code_line, comment, self.indent_mod = '', '', 0
                if not multiline:
                    break
        return offset
    def flush_text(self):
        text = ''.join(self.text_buffer)
        del self.text_buffer[:]
        if not text: return
        parts, pos, nl = [], 0, '\\\n' + '  ' * self.indent
        for m in self.re_inl.finditer(text):
            prefix, pos = text[pos:m.start()], m.end()
            if prefix:
                parts.append(nl.join(map(repr, prefix.splitlines(True))))
            if prefix.endswith('\n'): parts[-1] += nl
            parts.append(self.process_inline(m.group(1).strip()))
        if pos < len(text):
            prefix = text[pos:]
            lines = prefix.splitlines(True)
            if lines[-1].endswith('\\\\\n'): lines[-1] = lines[-1][:-3]
            elif lines[-1].endswith('\\\\\r\n'): lines[-1] = lines[-1][:-4]
            parts.append(nl.join(map(repr, lines)))
        code = '_printlist((%s,))' % ', '.join(parts)
        self.lineno += code.count('\n') + 1
        self.write_code(code)
    @staticmethod
    def process_inline(chunk):
        if chunk[0] == '!': return '_str(%s)' % chunk[1:]
        return '_escape(%s)' % chunk
    def write_code(self, line, comment=''):
        code = '  ' * (self.indent + self.indent_mod)
        code += line.lstrip() + comment + '\n'
        self.code_buffer.append(code)
def template(*args, **kwargs):
    tpl = args[0] if args else None
    adapter = kwargs.pop('template_adapter', SimpleTemplate)
    lookup = kwargs.pop('template_lookup', TEMPLATE_PATH)
    tplid = (id(lookup), tpl)
    if tplid not in TEMPLATES or DEBUG:
        settings = kwargs.pop('template_settings', {})
        if isinstance(tpl, adapter):
            TEMPLATES[tplid] = tpl
            if settings: TEMPLATES[tplid].prepare(**settings)
        elif "\n" in tpl or "{" in tpl or "%" in tpl or '$' in tpl:
            TEMPLATES[tplid] = adapter(source=tpl, lookup=lookup, **settings)
        else:
            TEMPLATES[tplid] = adapter(name=tpl, lookup=lookup, **settings)
    if not TEMPLATES[tplid]:
        abort(500, 'Template (%s) not found' % tpl)
    for dictarg in args[1:]:
        kwargs.update(dictarg)
    return TEMPLATES[tplid].render(kwargs)
def view(tpl_name, **defaults):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, (dict, DictMixin)):
                tplvars = defaults.copy()
                tplvars.update(result)
                return template(tpl_name, **tplvars)
            elif result is None:
                return template(tpl_name, defaults)
            return result
        return wrapper
    return decorator
TEMPLATE_PATH = ['./', './views/']
TEMPLATES = {}
DEBUG = False
NORUN = False
HTTP_CODES = httplib.responses.copy()
HTTP_CODES[418] = "I'm a teapot"
HTTP_CODES[428] = "Precondition Required"
HTTP_CODES[429] = "Too Many Requests"
HTTP_CODES[431] = "Request Header Fields Too Large"
HTTP_CODES[511] = "Network Authentication Required"
_HTTP_STATUS_LINES = dict((k, '%d %s' % (k, v))
                          for (k, v) in HTTP_CODES.items())
ERROR_PAGE_TEMPLATE = "error"
request = LocalRequest()
response = LocalResponse()
local = threading.local()
app = default_app = AppStack()
app.push()
ext = _ImportRedirect('bottle.ext' if __name__ == '__main__' else
                      __name__ + ".ext", 'bottle_%s').module

#################################################################
####              THE DRAG AND DROP PROGRAM 
#################################################################

TARGET_TYPE_URI_LIST = 80

def serve(path, a):
    @route('/<filename>')
    def static(filename):
        fileN = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1]
        return static_file(base64.b32decode(fileN)+extension, root=os.path.split(path)[0])
    run(host='0.0.0.0', port=8080, debug=True)

def entryChange(widget):
    with open('.raspberrycastIP', 'w+') as f:
        f.write(widget.get_text())

def get_file_path_from_dnd_dropped_uri(uri):
    # get the path to file
    path = ""
    if uri.startswith('file:\\\\\\'): # windows
        path = uri[8:] # 8 is len('file:///')
    elif uri.startswith('file://'): # nautilus, rox
        path = uri[7:] # 7 is len('file://')
    elif uri.startswith('file:'): # xffm
        path = uri[5:] # 5 is len('file:')
    path = urllib.url2pathname(path) # escape special chars
    path = path.strip('\r\n\x00') # remove \r\n and NULL
    return path

def on_drag_data_received(widget, context, x, y, selection, target_type, timestamp):
    if target_type == TARGET_TYPE_URI_LIST:
        uri = selection.get_data().strip('\r\n\x00')
        #print 'uri', uri
        uri_splitted = uri.split() # we may have more than one file dropped
        for uri in uri_splitted:
            path = get_file_path_from_dnd_dropped_uri(uri)
            #print 'path to open', path
            if os.path.isfile(path): # is it file?
                data = file(path).read()
                #print data
            thread.start_new_thread( serve, (path, 1) )
            filename = os.path.splitext(os.path.split(path)[1])[0]
            extension = os.path.splitext(path)[1]
            encoded_string = urllib.quote_plus("http://localhost:8080/"+base64.b32encode(filename)+extension)
            full_url = "http://"+w.entry.get_text()+":2020/stream?url="
            if os.path.isfile(os.path.splitext(path)[0]+".srt"):
                urllib2.urlopen(full_url+encoded_string+"&subtitles="+urllib.quote_plus("http://localhost:8080/"+base64.b32encode(os.path.splitext(os.path.split(path)[1])[0]))+".srt").read()
            else: 
                print "calling "+full_url+encoded_string
                urllib2.urlopen(full_url+encoded_string).read()

w = Gtk.Window(title="RaspberryCast", border_width=10)

vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
w.add(vbox)

w.text = Gtk.Label("Drag and drop a media file\n\nKeep this window open while \nthe media is playing", justify=Gtk.Justification.CENTER)
w.entry = Gtk.Entry()

try:
    with open('.raspberrycastIP', 'r') as f:
        w.entry.set_text(f.read())
except:
    w.entry.set_text("raspberrypi.local")

w.entry.connect("changed", entryChange)
vbox.add(w.text)
vbox.add(w.entry)

w.connect('drag_data_received', on_drag_data_received)
w.connect("destroy", Gtk.main_quit, "WM destroy")

w.drag_dest_set( Gtk.DestDefaults.MOTION|
                  Gtk.DestDefaults.HIGHLIGHT | Gtk.DestDefaults.DROP,
                  [Gtk.TargetEntry.new("text/uri-list", 0, 80)], Gdk.DragAction.COPY)

w.show_all()
Gtk.main()
