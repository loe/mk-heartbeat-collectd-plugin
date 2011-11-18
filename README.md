mk-heartbeat-collectd-plugin
=====================

A [mk-heartbeat](http://www.maatkit.org/doc/mk-heartbeat.html) plugin for [collectd](http://collectd.org) using collectd's [Python plugin](http://collectd.org/documentation/manpages/collectd-python.5.shtml).

Captures slave lag over the default frames:

 * Current
 * 1 minute average
 * 5 minute average
 * 15 minute average  

Install
-------
 1. Place heartbeat_info.py in /usr/lib/collectd/python (assuming you have collectd installed to /usr).
 2. Configure the plugin (see below).
 3. Restart collectd.

Configuration
-------------
Add the following to your collectd config **or** use the included redis.conf.

    <LoadPlugin python>
      Globals true
    </LoadPlugin>

    <Plugin python>
      ModulePath "/usr/lib/collectd/python"
      Import "heartbeat_info"

      <Module heartbeat_info>
        Path "/tmp/mk-heartbeat"
        Verbose false
      </Module>
    </Plugin>

Requirements
------------
 * collectd 4.9+
