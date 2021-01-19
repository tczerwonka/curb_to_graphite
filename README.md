# curb_to_graphite
Parse local http output of curb energy hub and shove the data in graphite

The CURB energy gadget doesn't have any useful API and I'd like to have the data available locally to compare
with other values in grafana.

There is data available via http locally, let's try to do something with it.

wget 192.168.1.28

Use some crap in python to parse out the values for each clamp and shove it into
graphite.  Code could probably be more efficient but it works so whatever.
