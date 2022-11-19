#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# The following imports are for Python2 support only
from __future__ import absolute_import
from __future__ import print_function

import copy
import filecmp
import os
import pprint
import pytest


DIRNAME = os.path.dirname(os.path.realpath(__file__))
TESTFILE1 = os.path.join(DIRNAME, 'wgtest1.conf')
TESTFILE1_SAVED = os.path.join(DIRNAME, 'wgtest1.conf.saved')


@pytest.fixture
def setup_testconfig1(scope='module'):
    import wgconfig
    wc = wgconfig.WGConfig(file=TESTFILE1)
    wc.read_file()
    yield wc
    #with contextlib.suppress(FileNotFoundError): # not used due to availability in newer Python versions only
    if os.path.exists(TESTFILE1_SAVED):
        os.unlink(TESTFILE1_SAVED)

def output_data(wc):
    """Provide output that is helpful for debugging purposes"""
    print('LINES:')
    pprint.pprint(list(enumerate(wc.lines)))
    print('INTERFACE:')
    pprint.pprint(wc.interface)
    print('PEERS:')
    pprint.pprint(wc.peers)

def get_peer_property_without_rawdata(wc):
    """Return the peer property of the provided wgconfig object without providing the _rawdata attribute"""
    result = copy.deepcopy(wc.peers)
    for peer in result.values():
        del peer['_rawdata']
    return result

def get_interface_property_without_rawdata(wc):
    """Return the interface property of the provided wgconfig object without providing the _rawdata attribute"""
    result = copy.deepcopy(wc.interface)
    del result['_rawdata']
    return result

def test_saved_file_is_unchanged(setup_testconfig1):
    wc = setup_testconfig1
    filename_saved = TESTFILE1_SAVED
    wc.write_file(filename_saved)
    assert filecmp.cmp(TESTFILE1, filename_saved, shallow=False), 'file needs to be unchanged on saving'

def test_expected_interface_data(setup_testconfig1):
    wc = setup_testconfig1
    output_data(wc)
    interface = {'Address': 'fe80::1/64',
                 'ListenPort': 51820,
                 'PrivateKey': '6FYKQKEtGFAb5HSwyj5cQl3wgS1E9d6SqVjdVksOn2s=',
                 '_disabled': False,
                 '_index_firstline': 0,
                 '_index_lastline': 6}
    assert get_interface_property_without_rawdata(wc) == interface, 'interface data needs to be correctly parsed'

def test_expected_peer_data(setup_testconfig1):
    wc = setup_testconfig1
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                             '9999::2/128'],
                                                             'Endpoint': '192.168.0.2:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                             '_disabled': False,
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_disabled': False,
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 24},
             'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=': {'AllowedIPs': ['fe80::4/128',
                                                                             '9999::4/128'],
                                                              'Endpoint': '192.168.0.4:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                              '_disabled': True,
                                                              '_index_firstline': 26,
                                                              '_index_lastline': 32}}
    assert get_peer_property_without_rawdata(wc) == peers, 'data of peers needs to be correctly parsed'

def test_initialize_file(setup_testconfig1):
    wc = setup_testconfig1
    wc.initialize_file()
    interface = {'_disabled': False,
                 '_index_firstline': 0,
                 '_index_lastline': 0}
    assert get_interface_property_without_rawdata(wc) == interface
    assert get_peer_property_without_rawdata(wc) == dict()

def test_initialize_file_with_comment(setup_testconfig1):
    wc = setup_testconfig1
    wc.initialize_file('# Leading comment for interface section')
    output_data(wc)
    interface = {'_disabled': False,
                 '_index_firstline': 0,
                 '_index_lastline': 1}
    assert get_interface_property_without_rawdata(wc) == interface
    assert get_peer_property_without_rawdata(wc) == dict()

def test_add_interface_attr(setup_testconfig1):
    wc = setup_testconfig1
    wc.add_attr(None, 'TestAttr', 42)
    output_data(wc)
    interface = {'Address': 'fe80::1/64',
                 'ListenPort': 51820,
                 'PrivateKey': '6FYKQKEtGFAb5HSwyj5cQl3wgS1E9d6SqVjdVksOn2s=',
                 'TestAttr': 42,
                 '_disabled': False,
                 '_index_firstline': 0,
                 '_index_lastline': 7}
    assert get_interface_property_without_rawdata(wc) == interface

def test_add_interface_attr_with_comment(setup_testconfig1):
    wc = setup_testconfig1
    wc.add_attr(None, 'TestAttr', 42, '# Leading comment')
    output_data(wc)
    interface = {'Address': 'fe80::1/64',
                 'ListenPort': 51820,
                 'PrivateKey': '6FYKQKEtGFAb5HSwyj5cQl3wgS1E9d6SqVjdVksOn2s=',
                 'TestAttr': 42,
                 '_disabled': False,
                 '_index_firstline': 0,
                 '_index_lastline': 8}
    assert get_interface_property_without_rawdata(wc) == interface

def test_del_interface_attr1(setup_testconfig1):
    wc = setup_testconfig1
    wc.del_attr(None, 'ListenPort', remove_leading_comments=False)
    output_data(wc)
    interface = {'Address': 'fe80::1/64',
                 'PrivateKey': '6FYKQKEtGFAb5HSwyj5cQl3wgS1E9d6SqVjdVksOn2s=',
                 '_disabled': False,
                 '_index_firstline': 0,
                 '_index_lastline': 5}
    assert get_interface_property_without_rawdata(wc) == interface

def test_del_interface_attr2(setup_testconfig1):
    wc = setup_testconfig1
    wc.del_attr(None, 'ListenPort', 51820, remove_leading_comments=False)
    output_data(wc)
    interface = {'Address': 'fe80::1/64',
                 'PrivateKey': '6FYKQKEtGFAb5HSwyj5cQl3wgS1E9d6SqVjdVksOn2s=',
                 '_disabled': False,
                 '_index_firstline': 0,
                 '_index_lastline': 5}
    assert get_interface_property_without_rawdata(wc) == interface

def test_del_interface_attr_with_comment(setup_testconfig1):
    wc = setup_testconfig1
    wc.del_attr(None, 'ListenPort')
    output_data(wc)
    interface = {'Address': 'fe80::1/64',
                 'PrivateKey': '6FYKQKEtGFAb5HSwyj5cQl3wgS1E9d6SqVjdVksOn2s=',
                 '_disabled': False,
                 '_index_firstline': 0,
                 '_index_lastline': 4}
    assert get_interface_property_without_rawdata(wc) == interface

def test_get_peer(setup_testconfig1):
    wc = setup_testconfig1
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                             '9999::2/128'],
                                                             'Endpoint': '192.168.0.2:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                             '_disabled': False,
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_disabled': False,
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 24},
             'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=': {'AllowedIPs': ['fe80::4/128',
                                                                            '9999::4/128'],
                                                             'Endpoint': '192.168.0.4:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                             '_disabled': True,
                                                             '_index_firstline': 26,
                                                             '_index_lastline': 32}}
    peerdata = wc.get_peer('XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=', include_details = True)
    del peerdata['_rawdata']
    assert peerdata == {'AllowedIPs': ['fe80::2/128',
                                       '9999::2/128'],
                        'Endpoint': '192.168.0.2:51820',
                        'PersistentKeepalive': 25,
                        'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                        '_disabled': False,
                        '_index_firstline': 8,
                        '_index_lastline': 15}
    peerdata = wc.get_peer('XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=', include_details = False)
    assert peerdata == {'AllowedIPs': ['fe80::2/128',
                                       '9999::2/128'],
                        'Endpoint': '192.168.0.2:51820',
                        'PersistentKeepalive': 25,
                        'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA='}

def test_add_peer(setup_testconfig1):
    wc = setup_testconfig1
    wc.add_peer('801mgm2JhjTOCxfihEknzFJGYxDvi+8oVYBrWe3hOWM=')
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                             '9999::2/128'],
                                                             'Endpoint': '192.168.0.2:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                             '_disabled': False,
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_disabled': False,
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 24},
             'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=': {'AllowedIPs': ['fe80::4/128',
                                                                            '9999::4/128'],
                                                             'Endpoint': '192.168.0.4:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                             '_disabled': True,
                                                             '_index_firstline': 26,
                                                             '_index_lastline': 32},
             '801mgm2JhjTOCxfihEknzFJGYxDvi+8oVYBrWe3hOWM=': {'PublicKey': '801mgm2JhjTOCxfihEknzFJGYxDvi+8oVYBrWe3hOWM=',
                                                             '_disabled': False,
                                                             '_index_firstline': 34,
                                                             '_index_lastline': 35}}
    assert get_peer_property_without_rawdata(wc) == peers, 'peer incorrectly added'

def test_add_peer_with_comment(setup_testconfig1):
    wc = setup_testconfig1
    wc.add_peer('801mgm2JhjTOCxfihEknzFJGYxDvi+8oVYBrWe3hOWM=', '# Newly added peer')
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                             '9999::2/128'],
                                                             'Endpoint': '192.168.0.2:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                             '_disabled': False,
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_disabled': False,
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 24},
             'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=': {'AllowedIPs': ['fe80::4/128',
                                                                            '9999::4/128'],
                                                             'Endpoint': '192.168.0.4:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                             '_disabled': True,
                                                             '_index_firstline': 26,
                                                             '_index_lastline': 32},
             '801mgm2JhjTOCxfihEknzFJGYxDvi+8oVYBrWe3hOWM=': {'PublicKey': '801mgm2JhjTOCxfihEknzFJGYxDvi+8oVYBrWe3hOWM=',
                                                             '_disabled': False,
                                                             '_index_firstline': 34,
                                                             '_index_lastline': 36}}
    assert get_peer_property_without_rawdata(wc) == peers, 'peer (with comment) incorrectly added'

def test_del_peer1(setup_testconfig1):
    wc = setup_testconfig1
    wc.del_peer('XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=')
    output_data(wc)
    peers = {'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_disabled': False,
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=': {'AllowedIPs': ['fe80::4/128',
                                                                             '9999::4/128'],
                                                              'Endpoint': '192.168.0.4:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                              '_disabled': True,
                                                              '_index_firstline': 17,
                                                              '_index_lastline': 23}}
    assert get_peer_property_without_rawdata(wc) == peers, 'first peer incorrectly deleted'
    interface = {'Address': 'fe80::1/64',
                 'ListenPort': 51820,
                 'PrivateKey': '6FYKQKEtGFAb5HSwyj5cQl3wgS1E9d6SqVjdVksOn2s=',
                 '_disabled': False,
                 '_index_firstline': 0,
                 '_index_lastline': 6}
    assert get_interface_property_without_rawdata(wc) == interface, 'first peer incorrectly deleted'

def test_del_peer2(setup_testconfig1):
    wc = setup_testconfig1
    wc.del_peer('eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=')
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                             '9999::2/128'],
                                                             'Endpoint': '192.168.0.2:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                             '_disabled': False,
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=': {'AllowedIPs': ['fe80::4/128',
                                                                             '9999::4/128'],
                                                              'Endpoint': '192.168.0.4:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                              '_disabled': True,
                                                              '_index_firstline': 17,
                                                              '_index_lastline': 23}}
    assert get_peer_property_without_rawdata(wc) == peers, 'second peer incorrectly deleted'
    interface = {'Address': 'fe80::1/64',
                 'ListenPort': 51820,
                 'PrivateKey': '6FYKQKEtGFAb5HSwyj5cQl3wgS1E9d6SqVjdVksOn2s=',
                 '_disabled': False,
                 '_index_firstline': 0,
                 '_index_lastline': 6}
    assert get_interface_property_without_rawdata(wc) == interface, 'second peer incorrectly deleted'

def test_add_attr1(setup_testconfig1):
    """add_attr to existing attr with value list"""
    wc = setup_testconfig1
    wc.add_attr('XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=', 'AllowedIPs', '10.0.0.1/16')
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                             '9999::2/128',
                                                                             '10.0.0.1/16'],
                                                             'Endpoint': '192.168.0.2:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                             '_disabled': False,
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_disabled': False,
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 24},
             'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=': {'AllowedIPs': ['fe80::4/128',
                                                                             '9999::4/128'],
                                                              'Endpoint': '192.168.0.4:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                              '_disabled': True,
                                                              '_index_firstline': 26,
                                                              '_index_lastline': 32}}
    assert get_peer_property_without_rawdata(wc) == peers

def test_add_attr2(setup_testconfig1):
    """add_attr with leading comment to existing attr with value list"""
    wc = setup_testconfig1
    wc.add_attr('XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=', 'AllowedIPs', '10.0.0.1/16', '# TEST')
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                             '9999::2/128',
                                                                             '10.0.0.1/16'],
                                                             'Endpoint': '192.168.0.2:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                             '_disabled': False,
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 16},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_disabled': False,
                                                             '_index_firstline': 18,
                                                             '_index_lastline': 25},
             'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=': {'AllowedIPs': ['fe80::4/128',
                                                                             '9999::4/128'],
                                                              'Endpoint': '192.168.0.4:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                              '_disabled': True,
                                                              '_index_firstline': 27,
                                                              '_index_lastline': 33}}
    assert get_peer_property_without_rawdata(wc) == peers

def test_add_attr3(setup_testconfig1):
    """add_attr to existing attr with existing value(s) as new line"""
    wc = setup_testconfig1
    wc.add_attr('eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=', 'AllowedIPs', '10.0.0.1/16', append_as_line=True)
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                             '9999::2/128'],
                                                             'Endpoint': '192.168.0.2:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                             '_disabled': False,
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128',
                                                                             '10.0.0.1/16'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_disabled': False,
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 25},
             'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=': {'AllowedIPs': ['fe80::4/128',
                                                                             '9999::4/128'],
                                                              'Endpoint': '192.168.0.4:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                              '_disabled': True,
                                                              '_index_firstline': 27,
                                                              '_index_lastline': 33}}
    assert get_peer_property_without_rawdata(wc) == peers

def test_add_attr4(setup_testconfig1):
    """add_attr with leading comment to existing attr with existing value(s) as new line"""
    wc = setup_testconfig1
    wc.add_attr('eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=', 'AllowedIPs', '10.0.0.1/16', '# TEST', append_as_line=True)
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                             '9999::2/128'],
                                                             'Endpoint': '192.168.0.2:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                             '_disabled': False,
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128',
                                                                             '10.0.0.1/16'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_disabled': False,
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 26},
             'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=': {'AllowedIPs': ['fe80::4/128',
                                                                             '9999::4/128'],
                                                              'Endpoint': '192.168.0.4:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                              '_disabled': True,
                                                              '_index_firstline': 28,
                                                              '_index_lastline': 34}}
    assert get_peer_property_without_rawdata(wc) == peers

def test_add_attr5(setup_testconfig1):
    """add_attr for a not yet present attr (at the end)"""
    wc = setup_testconfig1
    wc.add_attr('eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=', 'TestAttr', 42)
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                             '9999::2/128'],
                                                             'Endpoint': '192.168.0.2:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                             '_disabled': False,
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             'TestAttr': 42,
                                                             '_disabled': False,
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 25},
             'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=': {'AllowedIPs': ['fe80::4/128',
                                                                             '9999::4/128'],
                                                              'Endpoint': '192.168.0.4:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                              '_disabled': True,
                                                              '_index_firstline': 27,
                                                              '_index_lastline': 33}}
    assert get_peer_property_without_rawdata(wc) == peers

def test_add_attr6(setup_testconfig1):
    """add_attr with leading comment for a not yet present attr (at the end)"""
    wc = setup_testconfig1
    wc.add_attr('eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=', 'TestAttr', 42, '# TEST')
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                             '9999::2/128'],
                                                             'Endpoint': '192.168.0.2:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                             '_disabled': False,
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             'TestAttr': 42,
                                                             '_disabled': False,
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 26},
             'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=': {'AllowedIPs': ['fe80::4/128',
                                                                             '9999::4/128'],
                                                              'Endpoint': '192.168.0.4:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                              '_disabled': True,
                                                              '_index_firstline': 28,
                                                              '_index_lastline': 34}}
    assert get_peer_property_without_rawdata(wc) == peers

def test_del_attr1(setup_testconfig1):
    """del_attr: all attribute occurences where just once present"""
    wc = setup_testconfig1
    wc.del_attr('XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=', 'AllowedIPs')
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'Endpoint': '192.168.0.2:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                             '_disabled': False,
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 14},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_disabled': False,
                                                             '_index_firstline': 16,
                                                             '_index_lastline': 23},
             'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=': {'AllowedIPs': ['fe80::4/128',
                                                                             '9999::4/128'],
                                                              'Endpoint': '192.168.0.4:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                              '_disabled': True,
                                                              '_index_firstline': 25,
                                                              '_index_lastline': 31}}
    assert get_peer_property_without_rawdata(wc) == peers

def test_del_attr2(setup_testconfig1):
    """del_attr: all attribute occurences where two lines present"""
    wc = setup_testconfig1
    wc.del_attr('eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=', 'AllowedIPs')
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                             '9999::2/128'],
                                                             'Endpoint': '192.168.0.2:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                             '_disabled': False,
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_disabled': False,
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 22},
             'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=': {'AllowedIPs': ['fe80::4/128',
                                                                             '9999::4/128'],
                                                              'Endpoint': '192.168.0.4:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                              '_disabled': True,
                                                              '_index_firstline': 24,
                                                              '_index_lastline': 30}}
    assert get_peer_property_without_rawdata(wc) == peers

def test_del_attr3(setup_testconfig1):
    """del_attr: all attribute occurences with leading comment"""
    wc = setup_testconfig1
    wc.del_attr('eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=', 'Endpoint', remove_leading_comments=True)
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                             '9999::2/128'],
                                                             'Endpoint': '192.168.0.2:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                             '_disabled': False,
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_disabled': False,
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 22},
             'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=': {'AllowedIPs': ['fe80::4/128',
                                                                             '9999::4/128'],
                                                              'Endpoint': '192.168.0.4:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                              '_disabled': True,
                                                              '_index_firstline': 24,
                                                              '_index_lastline': 30}}
    assert get_peer_property_without_rawdata(wc) == peers

def test_del_attr4(setup_testconfig1):
    """del_attr: all attribute occurences keeping leading comment"""
    wc = setup_testconfig1
    wc.del_attr('eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=', 'Endpoint', remove_leading_comments=False)
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                             '9999::2/128'],
                                                             'Endpoint': '192.168.0.2:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                             '_disabled': False,
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_disabled': False,
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 23},
             'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=': {'AllowedIPs': ['fe80::4/128',
                                                                             '9999::4/128'],
                                                              'Endpoint': '192.168.0.4:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                              '_disabled': True,
                                                              '_index_firstline': 25,
                                                              '_index_lastline': 31}}
    assert get_peer_property_without_rawdata(wc) == peers

def test_del_attr5(setup_testconfig1):
    """del_attr: delete a single value from an attribute where two values are present in a single line"""
    wc = setup_testconfig1
    wc.del_attr('XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=', 'AllowedIPs', 'fe80::2/128')
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': '9999::2/128',
                                                             'Endpoint': '192.168.0.2:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                             '_disabled': False,
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_disabled': False,
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 24},
             'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=': {'AllowedIPs': ['fe80::4/128',
                                                                             '9999::4/128'],
                                                              'Endpoint': '192.168.0.4:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                              '_disabled': True,
                                                              '_index_firstline': 26,
                                                              '_index_lastline': 32}}
    assert get_peer_property_without_rawdata(wc) == peers

def test_del_attr6(setup_testconfig1):
    """del_attr: delete a single value from an attribute where two values are present on separate lines (first line)"""
    wc = setup_testconfig1
    wc.del_attr('eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=', 'AllowedIPs', 'fe80::3/128')
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                             '9999::2/128'],
                                                             'Endpoint': '192.168.0.2:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                             '_disabled': False,
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': '9999::3/128',
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_disabled': False,
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 23},
             'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=': {'AllowedIPs': ['fe80::4/128',
                                                                             '9999::4/128'],
                                                              'Endpoint': '192.168.0.4:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                              '_disabled': True,
                                                              '_index_firstline': 25,
                                                              '_index_lastline': 31}}
    assert get_peer_property_without_rawdata(wc) == peers

def test_del_attr7(setup_testconfig1):
    """del_attr: delete a single value from an attribute where two values are present on separate lines (second line)"""
    wc = setup_testconfig1
    wc.del_attr('eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=', 'AllowedIPs', '9999::3/128')
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                             '9999::2/128'],
                                                             'Endpoint': '192.168.0.2:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                             '_disabled': False,
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': 'fe80::3/128',
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_disabled': False,
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 23},
             'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=': {'AllowedIPs': ['fe80::4/128',
                                                                             '9999::4/128'],
                                                              'Endpoint': '192.168.0.4:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                              '_disabled': True,
                                                              '_index_firstline': 25,
                                                              '_index_lastline': 31}}
    assert get_peer_property_without_rawdata(wc) == peers

def test_disable_peer1(setup_testconfig1):
    wc = setup_testconfig1
    assert wc.get_peer_enabled('XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=')
    wc.disable_peer('XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=')
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                 '9999::2/128'],
                                                  'Endpoint': '192.168.0.2:51820',
                                                  'PersistentKeepalive': 25,
                                                  'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                  '_disabled': True,
                                                  '_index_firstline': 8,
                                                  '_index_lastline': 15,
                                                  '_rawdata': ['#! # This is a third comment',
                                                               '#! [Peer]',
                                                               '#! Endpoint = 192.168.0.2:51820',
                                                               '#! # PrivateKey = cKqe3xDFsKlMwlQfVJAnbNhiGFV57FnfLykiBtrnumY=',
                                                               '#! PublicKey = XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                               '#! AllowedIPs = fe80::2/128, 9999::2/128',
                                                               '#! PersistentKeepalive = 25',
                                                               '#! # This is a forth comment']},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                              'Endpoint': '192.168.0.3:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                              '_disabled': False,
                                                              '_index_firstline': 17,
                                                              '_index_lastline': 24,
                                                              '_rawdata': ['[Peer]',
                                                                           '# This is a fifth comment',
                                                                           'Endpoint = 192.168.0.3:51820',
                                                                           '# PrivateKey = iJQkwzeB2+/lGyGPTM23Wes5Kg0n+LgXMqK8XAwWt14=',
                                                                           'PublicKey = eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                                           'AllowedIPs = fe80::3/128',
                                                                           'AllowedIPs = 9999::3/128',
                                                                           'PersistentKeepalive = 25']},
             'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=': {'AllowedIPs': ['fe80::4/128',
                                                                             '9999::4/128'],
                                                              'Endpoint': '192.168.0.4:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                              '_disabled': True,
                                                              '_index_firstline': 26,
                                                              '_index_lastline': 32,
                                                              '_rawdata': ['#! [Peer]',
                                                                           '#! Endpoint = 192.168.0.4:51820',
                                                                           '#! # PrivateKey = iAgWkT6/FnO+kcNcD65SKpjcAweLmcppVE4IEHxa73o=',
                                                                           '#! PublicKey = ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                                           '#! AllowedIPs = fe80::4/128',
                                                                           '#! AllowedIPs = 9999::4/128',
                                                                           '#! PersistentKeepalive = 25']}}
    assert wc.peers == peers
    assert not wc.get_peer_enabled('XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=')

def test_disable_peer2(setup_testconfig1):
    wc = setup_testconfig1    
    assert wc.get_peer_enabled('eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=')
    wc.disable_peer('eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=')
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                 '9999::2/128'],
                                                  'Endpoint': '192.168.0.2:51820',
                                                  'PersistentKeepalive': 25,
                                                  'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                  '_disabled': False,
                                                  '_index_firstline': 8,
                                                  '_index_lastline': 15,
                                                  '_rawdata': ['# This is a third comment',
                                                               '[Peer]',
                                                               'Endpoint = 192.168.0.2:51820',
                                                               '# PrivateKey = cKqe3xDFsKlMwlQfVJAnbNhiGFV57FnfLykiBtrnumY=',
                                                               'PublicKey = XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                               'AllowedIPs = fe80::2/128, 9999::2/128',
                                                               'PersistentKeepalive = 25',
                                                               '# This is a forth comment']},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                              'Endpoint': '192.168.0.3:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                              '_disabled': True,
                                                              '_index_firstline': 17,
                                                              '_index_lastline': 24,
                                                              '_rawdata': ['#! [Peer]',
                                                                           '#! # This is a fifth comment',
                                                                           '#! Endpoint = 192.168.0.3:51820',
                                                                           '#! # PrivateKey = iJQkwzeB2+/lGyGPTM23Wes5Kg0n+LgXMqK8XAwWt14=',
                                                                           '#! PublicKey = eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                                           '#! AllowedIPs = fe80::3/128',
                                                                           '#! AllowedIPs = 9999::3/128',
                                                                           '#! PersistentKeepalive = 25']},
             'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=': {'AllowedIPs': ['fe80::4/128',
                                                                             '9999::4/128'],
                                                              'Endpoint': '192.168.0.4:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                              '_disabled': True,
                                                              '_index_firstline': 26,
                                                              '_index_lastline': 32,
                                                              '_rawdata': ['#! [Peer]',
                                                                           '#! Endpoint = 192.168.0.4:51820',
                                                                           '#! # PrivateKey = iAgWkT6/FnO+kcNcD65SKpjcAweLmcppVE4IEHxa73o=',
                                                                           '#! PublicKey = ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                                           '#! AllowedIPs = fe80::4/128',
                                                                           '#! AllowedIPs = 9999::4/128',
                                                                           '#! PersistentKeepalive = 25']}}
    assert wc.peers == peers
    assert not wc.get_peer_enabled('eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=')

def test_disable_twice_peer2(setup_testconfig1):
    """Check that an already disabled peer can be disabled once more without any consequences"""
    wc = setup_testconfig1
    assert wc.get_peer_enabled('eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=')    
    wc.disable_peer('eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=')
    assert not wc.get_peer_enabled('eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=')    
    wc.disable_peer('eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=')    
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                 '9999::2/128'],
                                                  'Endpoint': '192.168.0.2:51820',
                                                  'PersistentKeepalive': 25,
                                                  'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                  '_disabled': False,
                                                  '_index_firstline': 8,
                                                  '_index_lastline': 15,
                                                  '_rawdata': ['# This is a third comment',
                                                               '[Peer]',
                                                               'Endpoint = 192.168.0.2:51820',
                                                               '# PrivateKey = cKqe3xDFsKlMwlQfVJAnbNhiGFV57FnfLykiBtrnumY=',
                                                               'PublicKey = XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                               'AllowedIPs = fe80::2/128, 9999::2/128',
                                                               'PersistentKeepalive = 25',
                                                               '# This is a forth comment']},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                              'Endpoint': '192.168.0.3:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                              '_disabled': True,
                                                              '_index_firstline': 17,
                                                              '_index_lastline': 24,
                                                              '_rawdata': ['#! [Peer]',
                                                                           '#! # This is a fifth comment',
                                                                           '#! Endpoint = 192.168.0.3:51820',
                                                                           '#! # PrivateKey = iJQkwzeB2+/lGyGPTM23Wes5Kg0n+LgXMqK8XAwWt14=',
                                                                           '#! PublicKey = eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                                           '#! AllowedIPs = fe80::3/128',
                                                                           '#! AllowedIPs = 9999::3/128',
                                                                           '#! PersistentKeepalive = 25']},
             'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=': {'AllowedIPs': ['fe80::4/128',
                                                                             '9999::4/128'],
                                                              'Endpoint': '192.168.0.4:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                              '_disabled': True,
                                                              '_index_firstline': 26,
                                                              '_index_lastline': 32,
                                                              '_rawdata': ['#! [Peer]',
                                                                           '#! Endpoint = 192.168.0.4:51820',
                                                                           '#! # PrivateKey = iAgWkT6/FnO+kcNcD65SKpjcAweLmcppVE4IEHxa73o=',
                                                                           '#! PublicKey = ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                                           '#! AllowedIPs = fe80::4/128',
                                                                           '#! AllowedIPs = 9999::4/128',
                                                                           '#! PersistentKeepalive = 25']}}
    assert wc.peers == peers
    assert not wc.get_peer_enabled('eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=')

def test_enable_peer3(setup_testconfig1):
    wc = setup_testconfig1
    assert not wc.get_peer_enabled('ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=')    
    wc.enable_peer('ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=')
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                 '9999::2/128'],
                                                  'Endpoint': '192.168.0.2:51820',
                                                  'PersistentKeepalive': 25,
                                                  'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                  '_disabled': False,
                                                  '_index_firstline': 8,
                                                  '_index_lastline': 15,
                                                  '_rawdata': ['# This is a third comment',
                                                               '[Peer]',
                                                               'Endpoint = 192.168.0.2:51820',
                                                               '# PrivateKey = cKqe3xDFsKlMwlQfVJAnbNhiGFV57FnfLykiBtrnumY=',
                                                               'PublicKey = XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                               'AllowedIPs = fe80::2/128, 9999::2/128',
                                                               'PersistentKeepalive = 25',
                                                               '# This is a forth comment']},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                              'Endpoint': '192.168.0.3:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                              '_disabled': False,
                                                              '_index_firstline': 17,
                                                              '_index_lastline': 24,
                                                              '_rawdata': ['[Peer]',
                                                                           '# This is a fifth comment',
                                                                           'Endpoint = 192.168.0.3:51820',
                                                                           '# PrivateKey = iJQkwzeB2+/lGyGPTM23Wes5Kg0n+LgXMqK8XAwWt14=',
                                                                           'PublicKey = eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                                           'AllowedIPs = fe80::3/128',
                                                                           'AllowedIPs = 9999::3/128',
                                                                           'PersistentKeepalive = 25']},
             'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=': {'AllowedIPs': ['fe80::4/128',
                                                                             '9999::4/128'],
                                                              'Endpoint': '192.168.0.4:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                              '_disabled': False,
                                                              '_index_firstline': 26,
                                                              '_index_lastline': 32,
                                                              '_rawdata': ['[Peer]',
                                                                           'Endpoint = 192.168.0.4:51820',
                                                                           '# PrivateKey = iAgWkT6/FnO+kcNcD65SKpjcAweLmcppVE4IEHxa73o=',
                                                                           'PublicKey = ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                                           'AllowedIPs = fe80::4/128',
                                                                           'AllowedIPs = 9999::4/128',
                                                                           'PersistentKeepalive = 25']}}
    assert wc.peers == peers
    assert wc.get_peer_enabled('ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=')        

def test_enable_twice_peer3(setup_testconfig1):
    """Check that an already enabled peer can be enabled again without any consequences"""
    wc = setup_testconfig1
    assert not wc.get_peer_enabled('ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=')        
    wc.enable_peer('ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=')
    assert wc.get_peer_enabled('ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=')        
    wc.enable_peer('ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=')
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                 '9999::2/128'],
                                                  'Endpoint': '192.168.0.2:51820',
                                                  'PersistentKeepalive': 25,
                                                  'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                  '_disabled': False,
                                                  '_index_firstline': 8,
                                                  '_index_lastline': 15,
                                                  '_rawdata': ['# This is a third comment',
                                                               '[Peer]',
                                                               'Endpoint = 192.168.0.2:51820',
                                                               '# PrivateKey = cKqe3xDFsKlMwlQfVJAnbNhiGFV57FnfLykiBtrnumY=',
                                                               'PublicKey = XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                               'AllowedIPs = fe80::2/128, 9999::2/128',
                                                               'PersistentKeepalive = 25',
                                                               '# This is a forth comment']},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                              'Endpoint': '192.168.0.3:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                              '_disabled': False,
                                                              '_index_firstline': 17,
                                                              '_index_lastline': 24,
                                                              '_rawdata': ['[Peer]',
                                                                           '# This is a fifth comment',
                                                                           'Endpoint = 192.168.0.3:51820',
                                                                           '# PrivateKey = iJQkwzeB2+/lGyGPTM23Wes5Kg0n+LgXMqK8XAwWt14=',
                                                                           'PublicKey = eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                                           'AllowedIPs = fe80::3/128',
                                                                           'AllowedIPs = 9999::3/128',
                                                                           'PersistentKeepalive = 25']},
             'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=': {'AllowedIPs': ['fe80::4/128',
                                                                             '9999::4/128'],
                                                              'Endpoint': '192.168.0.4:51820',
                                                              'PersistentKeepalive': 25,
                                                              'PublicKey': 'ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                              '_disabled': False,
                                                              '_index_firstline': 26,
                                                              '_index_lastline': 32,
                                                              '_rawdata': ['[Peer]',
                                                                           'Endpoint = 192.168.0.4:51820',
                                                                           '# PrivateKey = iAgWkT6/FnO+kcNcD65SKpjcAweLmcppVE4IEHxa73o=',
                                                                           'PublicKey = ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=',
                                                                           'AllowedIPs = fe80::4/128',
                                                                           'AllowedIPs = 9999::4/128',
                                                                           'PersistentKeepalive = 25']}}
    assert wc.peers == peers
    assert wc.get_peer_enabled('ivBDO+pT2m4W5bl7ApNaC3BybEtYa1fvNpA4h+tHyy8=')        
