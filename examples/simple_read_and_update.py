# Read and parse the existing WireGuard configuration file 'wg0.conf' located in '/etc/wireguard':


import wgconfig

# Create new object instance for file "/etc/wireguard/wg0.conf"
wc = wgconfig.WGConfig('wg0')

# Read the existing file
wc.read_file()

# Dump data
print('INTERFACE DATA:', wc.get_interface())
print('LIST OF PEERS:', wc.get_peers())
print('ALL PEER DATA:', wc.get_peers(keys_only=False))


# Add a new peer with a comment line before the peer section (note: uses example key)
wc.add_peer('801mgm2JhjTOCxfihEknzFJGYxDvi+8oVYBrWe3hOWM=', '# Newly added peer')

# Add an attribute to that peer
wc.add_attr('801mgm2JhjTOCxfihEknzFJGYxDvi+8oVYBrWe3hOWM=', 'Endpoint', 'wg.example.com:51820', '# Added for demonstration purposes')

# Write the changes to disk. Comments that were present when reading the file are preserved
wc.write_file()
