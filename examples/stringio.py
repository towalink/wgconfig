# Example for using StringIO with wgconfig

# Approach: use write_to_fileobj and read_from_fileobj with StringIO instances


import io, wgconfig


# Create new file object
conf_f = io.StringIO()

# Create new WireGuard config and write to file object
wc = wgconfig.WGConfig()
wc.add_attr(None, 'PrivateKey', '6FYKQKEtGFAb5HSwyj5cQl3wgS1E9d6SqVjdVksOn2s=')  # just an example key
wc.write_to_fileobj(conf_f)

# Read from file object to check
conf_f.seek(0)
print(conf_f.read())

# Read from file object into new wgconfig instance and write to a regular file
wc = wgconfig.WGConfig()
conf_f.seek(0)
wc.read_from_fileobj(conf_f)
wc.write_file('/tmp/wgtest.conf')
