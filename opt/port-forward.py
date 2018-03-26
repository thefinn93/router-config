#!/usr/bin/env python3
import json
import sys

rules = {
    "filter": ["-A INPUT -i lo -j ACCEPT", "-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT"],
    "nat": []
}

with open(sys.argv[1]) as f:
    config = json.load(f)
    public_if = config["public-if"]
    for extport, dest in config['port-forwards'].items():
        rules['nat'].append("-A PREROUTING -i {} -p tcp -m tcp --dport {} -j DNAT --to-destination {}".format(public_if, extport, dest))
        rules['nat'].append("-A PREROUTING -i {} -p udp -m udp --dport {} -j DNAT --to-destination {}".format(public_if, extport, dest))
        rules['filter'].append("-A FORWARD -i {} -p tcp -m tcp --dport {} -m state --state NEW -j ACCEPT".format(public_if, extport))
        rules['filter'].append("-A FORWARD -i {} -p udp -m udp --dport {} -m state --state NEW -j ACCEPT".format(public_if, extport))
    rules['nat'].append("-A POSTROUTING -o {} -j MASQUERADE".format(public_if))
    rules['filter'].append("-A INPUT -i enp5s0 -j DROP")

for t in ['filter', 'nat']:
    print("*{}".format(t))
    print("\n".join(rules[t]))
    print("COMMIT")

