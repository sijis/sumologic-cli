#!/usr/bin/python -tt

import urllib2
import simplejson
import sys
from optparse import OptionParser

def main():

    parser = OptionParser(version='%prog 0.1',
                          description='Sumologic cli to query data through API')
    parser.add_option('-u', '--username',
                      dest='username', metavar='USERNAME',
                      default=None,
                      help='Username of API login')
    parser.add_option('-p', '--password',
                      dest='password', metavar='PASSWORD',
                      default=None,
                      help='Password of API login')
    parser.add_option('-v', '--verbose',
                      dest='verbose',
                      action='store_true',
                      help='enable verbosity')
    parser.add_option('--debug',
                      dest='debug',
                      default=False, action='store_true',
                      help='Enable debugging mode')

    (options, args) = parser.parse_args()

    data = vars(options)

    if not data.has_key('username') or \
       not data.has_key('password'):
        print 'username and password are required.'
        print 'Exiting....'
        sys.exit(1) 

    t_url = 'https://api.sumologic.com/api/v1/logs/search?q=error&from=2013-08-22T13:01:02&to=2013-08-22T13:01:32'

    data['url'] = t_url

    headers = {
        'Content-type': 'application/json',
    }

    req = urllib2.Request(data['url'], None, headers)

    password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, data['url'], data['username'],
                                    data['password'])
    auth_manager = urllib2.HTTPBasicAuthHandler(password_manager)
    opener = urllib2.build_opener(auth_manager)
    urllib2.install_opener(opener)
     
    try:
        handler = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        print e
        print 'Authentication Error. Please validate username or password.'
        sys.exit(10)

    if data['debug']:
        print '..-:[ debug mode ]:-..'
        for opt in data:
            print '%s => %s' % (opt, data[opt])
        print 'Return Code: %s' % handler.getcode()
        print '----------------------'

    results = simplejson.load(handler)

if __name__ == "__main__":
    main()
