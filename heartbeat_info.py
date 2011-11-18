# mk-heartbeat-collectd-plugin - hearbeat_info.py
#
# Author: W. Andrew Loe III (http://andrewloe.com/)
# Description: This plugin uses collectd's Python plugin to parse mk-heartbeat slave lag.
#
# Loosely based on Garret Heaton's "redis-collectd-plugin"
#   https://github.com/powdahound/redis-collectd-plugin


import collectd
import re

NAME = 'heartbeat_info'
# Override in config by specifing 'Path'
HEARTBEAT_PATH = '/tmp/mk-heartbeat'
# Override in config by specifying 'Verbose'.
VERBOSE_LOGGING = False


# Parse the heartbeat file for the slave lag.
def get_stats():
    stats = {}

    with open(HEARTBEAT_PATH, 'r') as f:
        data = f.read()

    m = re.findall(r'\d+\.\d+', data)
    # Convert all of these values from seconds to milliseconds, they'll be cast to int by the read_callback()
    stats['current'] = float(m[0]) * 100
    stats['1m'] = float(m[1]) * 100
    stats['5m'] = float(m[2]) * 100
    stats['15m'] = float(m[3]) * 100

    # Verbose output
    logger('verb', '[heartbeat] Current: %i, 1m: %i, 5m: %i, 15m %i' % (stats['current'], stats['1m'], stats['5m'], stats['15m']))

    return stats


# Config data from collectd
def configure_callback(conf):
    global HEARTBEAT_PATH, VERBOSE_LOGGING
    for node in conf.children:
        if node.key == 'Path':
            HEARTBEAT_PATH = node.values[0]
        elif node.key == 'Verbose':
            VERBOSE_LOGGING = bool(node.values[0])
        else:
            logger('warn', 'Unknown config key: %s' % node.key)


# Send info to collectd
def read_callback():
    logger('verb', 'read_callback')
    info = get_stats()

    if not info:
        logger('err', 'No information received - very bad.')
        return

    logger('verb', 'About to trigger the dispatch..')

    # send values
    for key in info:
        logger('verb', 'Dispatching %s : %i' % (key, info[key]))
        val = collectd.Values(plugin=NAME)
        val.type = 'gauge'
        val.type_instance = key
        val.values = [int(info[key])]
        val.dispatch()


# Send log messages (via collectd) 
def logger(t, msg):
    if t == 'err':
        collectd.error('%s: %s' % (NAME, msg))
    if t == 'warn':
        collectd.warning('%s: %s' % (NAME, msg))
    elif t == 'verb' and VERBOSE_LOGGING == True:
        collectd.info('%s: %s' % (NAME, msg))


# Runtime
collectd.register_config(configure_callback)
collectd.warning('Initializing heartbeat_info')
collectd.register_read(read_callback)

