#!/usr/bin/python -tt

__author__ = 'Sijis Aviles'

import urllib
import urllib2
import simplejson
import sys
from optparse import OptionParser
import datetime
import pprint

def parse_results(results, data):
    length = len(results)
    pprint.pprint(results[-data['limits']:])
    print 'Records found: %d' % length
    print 'Only showing %d records.' % data['limits']

def main():

    time_now = datetime.datetime.now().replace(second=0, microsecond=0)
    right_now = time_now.isoformat()
    minutes_ago = (time_now - datetime.timedelta(minutes=5)).isoformat()

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
    parser.add_option('-s', '--search',
                      dest='search', metavar='TEXT',
                      default=None,
                      help='Search text against log')
    parser.add_option('-f', '--format',
                      dest='format', metavar='FORMAT',
                      default='json',
                      help='Search results output format')
    parser.add_option('-m', '--timzone',
                      dest='timezone', metavar='TIMEZONE',
                      default='UTC',
                      help='Timezone used in results')
    parser.add_option('-o', '--time-to',
                      dest='timeto', metavar='TIME',
                      default='%s' % right_now,
                      help='End time for search')
    parser.add_option('-i', '--time-from',
                      dest='timefrom', metavar='TIME',
                      default='%s' % minutes_ago,
                      help='Start time for search')
    parser.add_option('-n', '--nodrop',
                      dest='nodrop',
                      action='store_true',
                      default=False,
                      help='Enabling will return all results - DISABLED')
    parser.add_option('-l', '--limits',
                      dest='limits', metavar='NUMBER',
                      default=1000,
                      help='Number of results to return')
    parser.add_option('--url',
                      dest='base_url', metavar='URL',
                      default='https://api.sumologic.com/api/v1/logs/search',
                      help='API URL')
    parser.add_option('-v', '--verbose',
                      dest='verbose',
                      action='store_true',
                      help='Enable verbosity')
    parser.add_option('--debug',
                      dest='debug',
                      default=False, action='store_true',
                      help='Enable debugging mode')

    (options, args) = parser.parse_args()

    data = vars(options)

    data['valid_formats'] = ['json', 'text']

    if data['username'] is None or \
       data['password'] is None:
        print 'Username and Password are required.'
        print 'Exiting....'
        sys.exit(1) 

    if data['search'] is None:
        print 'A search criteria is required.'
        sys.exit(1)

    t_options = []

    t_options.append('q="%s"' % urllib.quote(data['search']))

    if  data['format'] not in data['valid_formats']:
        print 'Invalid and unsupported format specified'
        print 'The valid formats are: %s' % ', '.join(data['valid_formats'])
        sys.exit(3)
    else:
        t_options.append('format=%s' % data['format'])

    data['limits'] = int(data['limits'])

    t_options.append('tz=%s' % data['timezone'])
    t_options.append('from=%s' % data['timefrom'])
    t_options.append('to=%s' % data['timeto'])

    data['options'] = '&'.join(t_options)
    data['url'] = '%s?%s' % (data['base_url'], data['options'])

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
        print 'Issue encountered.'
        print e
        sys.exit(10)

    if data['debug']:
        print '..-:[ debug mode ]:-..'
        print '---- data ------------'
        for opt in data:
            print '%s => %s' % (opt, data[opt])
        print '---- options----------'
        for opt in t_options:
            print '%s' % (opt)

        print '---- other -----------'
        print 'Return Code: %s' % handler.getcode()
        print '----------------------'
        sys.exit(11)

    parse_results(simplejson.load(handler), data)

if __name__ == "__main__":
    main()
