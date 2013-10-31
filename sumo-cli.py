#!/usr/bin/python -tt

__author__ = 'Sijis Aviles'

import sys
from optparse import OptionParser
import datetime
import pprint
import sumologic.client
import sumologic.search

def parse_results(results, data):
    pprint.pprint(results[-data['limits']:])
    print 'Records found: %d' % len(results)
    print 'Only showing %d records.' % data['limits']

def main():

    time_now = datetime.datetime.now().replace(second=0, microsecond=0)
    right_now = time_now.isoformat()
    minutes_ago = (time_now - datetime.timedelta(minutes=5)).isoformat()

    parser = OptionParser(version='%prog 0.2',
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

    t_options = {}

    if  data['format'] not in data['valid_formats']:
        print 'Invalid and unsupported format specified'
        print 'The valid formats are: %s' % ', '.join(data['valid_formats'])
        sys.exit(3)
    else:
        t_options['format'] = data['format']

    data['limits'] = int(data['limits'])

    t_options['tz'] = data['timezone']
    t_options['from'] = data['timefrom']
    t_options['to'] = data['timeto']

    client = sumologic.client.Client(auth=(data['username'], data['password']), debug=data['debug'], **t_options)
    search = sumologic.search.Search(client)
    results = search.query(data['search'])
    client.debug()

    try:
        results['data'][0]
    except KeyError:
        print 'An issue was encountered.'
        print '%s: %s' % (results['response'], results['reason'])
        sys.exit(10)
    except IndexError:
        print 'No records found.'
        sys.exit(3)

    parse_results(results['data'], data)

if __name__ == "__main__":
    main()
