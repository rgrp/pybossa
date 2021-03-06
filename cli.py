#!/usr/bin/env python
import os
import sys
import optparse
import inspect

import pybossa.model as model
import pybossa.web as web

def db_create():
    '''Create the db'''
    dburi = web.app.config['SQLALCHEMY_DATABASE_URI']
    engine = model.create_engine(dburi)
    model.Base.metadata.create_all(bind=engine)

def db_rebuild():
    '''Rebuild the db'''
    dburi = web.app.config['SQLALCHEMY_DATABASE_URI']
    engine = model.create_engine(dburi)
    model.Base.metadata.drop_all(bind=engine)
    model.Base.metadata.create_all(bind=engine)

def fixtures():
    '''Not yet implemented!'''
    dburi = web.app.config['SQLALCHEMY_DATABASE_URI']
    engine = model.create_engine(dburi)
    model.set_engine(engine)
    user = model.User(
        name=u'tester',
        email_addr=u'tester@tester.org'
        )
    model.Session.add(user)
    model.Session.commit()
    

## ==================================================
## Misc stuff for setting up a command line interface

def _module_functions(functions):
    local_functions = dict(functions)
    for k,v in local_functions.items():
        if not inspect.isfunction(v) or k.startswith('_'):
            del local_functions[k]
    return local_functions

def _main(functions_or_object):
    isobject = inspect.isclass(functions_or_object)
    if isobject:
        _methods = _object_methods(functions_or_object)
    else:
        _methods = _module_functions(functions_or_object)

    usage = '''%prog {action}

Actions:
    '''
    usage += '\n    '.join(
        [ '%s: %s' % (name, m.__doc__.split('\n')[0] if m.__doc__ else '') for (name,m)
        in sorted(_methods.items()) ])
    parser = optparse.OptionParser(usage)
    # Optional: for a config file
    # parser.add_option('-c', '--config', dest='config',
    #         help='Config file to use.')
    options, args = parser.parse_args()

    if not args or not args[0] in _methods:
        parser.print_help()
        sys.exit(1)

    method = args[0]
    if isobject:
        getattr(functions_or_object(), method)(*args[1:])
    else:
        _methods[method](*args[1:])

__all__ = [ '_main' ]

if __name__ == '__main__':
    _main(locals())


