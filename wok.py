# -*- coding: utf-8 -*-

import json
import urllib2
import argparse

api_key = '9a0554259914a86fb9e7eb014e4e5d52'
api_enabled = False
base_url = 'http://wok.io/'


class Wok(object):
    """Handles wok.io API"""

    def __init__(self, key=api_key):
        self.api_key = key

    def getContents(self):
        if api_enabled:
            self.url = self.url + '&api=' + api_key
        response = urllib2.urlopen(self.url)
        data = response.read()
        return data


class List(Wok):
    """Handle list of walls API"""
    def __init__(self, query=''):
        super(List, self).__init__()
        self.query = query
        self.url = self.buildQueryString()
        self.data = self.getContents()

    def buildQueryString(self):
        url = '{base}i/search.json?q={query}'.format(base=base_url,
                                                     query=self.query)
        return url

    def handleData(self):
        json_data = json.loads(self.data)

        print
        print 'List of wok.io walls:'
        print

        for wall in json_data:
            print wall['name']
            if wall['description']:
                print wall['description']
            print base_url + wall['slug']
            print


class Wall(Wok):
    """Handles walls API"""
    def __init__(self, wall, query=''):
        super(Wall, self).__init__()
        self.wall = wall
        self.query = query
        self.url = self.buildQueryString()
        self.data = self.getContents()

    def buildQueryString(self):
        url = '{base}{wall}.json?q={query}'.format(base=base_url,
                                                   wall=self.wall,
                                                   query=self.query)
        return url

    def handleData(self):
        json_data = json.loads(self.data)

        print
        print 'Last links from: {muro}'.format(muro=json_data['wall']['name'])
        print

        for id, link in json_data['items'].iteritems():
            item = link['link']
            print item['title']
            if item['description']:
                print item['description']
            print item['url']
            print

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Wok.io CLI interface')

    opts = parser.add_mutually_exclusive_group(required=True)
    opts.add_argument('--list', action='store_true', default=False,
                      help='List all walls, you can use --query to filter')
    opts.add_argument('--wall', action='store', help='Lists all links from a '
                      'wall')

    parser.add_argument('--query', action='store', default='')

    matrix = parser.parse_args()

    if matrix.list:
        wall_list = List(matrix.query)
        wall_list.handleData()

    if matrix.wall:
        wall_links = Wall(matrix.wall, matrix.query)
        wall_links.handleData()
