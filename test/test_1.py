#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import with_statement
from __future__ import absolute_import
from __future__ import print_function
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
    # python2 compatibility
    #   - no FileNotFoundError 
    #   - no contextlib.suppres()
    # import contextlib
    # with contextlib.suppress(FileNotFoundError):
    if os.path.exists(TESTFILE1_SAVED):
        os.unlink(TESTFILE1_SAVED)

def output_data(wc):
    print('LINES:')
    pprint.pprint(list(enumerate(wc.lines)))
    print('INTERFACE:')
    pprint.pprint(wc.interface)
    print('PEERS:')
    pprint.pprint(wc.peers)

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
                 '_index_firstline': 0,
                 '_index_lastline': 6}
    del wc.interface['_rawdata']
    assert wc.interface == interface, 'interface data needs to be correctly parsed'
    
def test_expected_peer_data(setup_testconfig1):
    wc = setup_testconfig1
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                             '9999::2/128'],
                                                             'Endpoint': '192.168.0.2:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 24}}
    for peer in list(wc.peers.values()):
        del peer['_rawdata']
    assert wc.peers == peers, 'data of peers needs to be correctly parsed'

def test_initialize_file(setup_testconfig1):
    wc = setup_testconfig1
    wc.initialize_file()
    interface = {'_index_firstline': 0,
                 '_index_lastline': 0}
    del wc.interface['_rawdata']
    assert wc.interface == interface
    for peer in list(wc.peers.values()):
        del peer['_rawdata']
    assert wc.peers == dict()

def test_initialize_file_with_comment(setup_testconfig1):
    wc = setup_testconfig1
    wc.initialize_file('# Leading comment for interface section')
    output_data(wc)
    interface = {'_index_firstline': 0,
                 '_index_lastline': 1}
    del wc.interface['_rawdata']
    assert wc.interface == interface
    for peer in list(wc.peers.values()):
        del peer['_rawdata']
    assert wc.peers == dict()

def test_add_interface_attr(setup_testconfig1):
    wc = setup_testconfig1
    wc.add_attr(None, 'TestAttr', 42)
    output_data(wc)
    interface = {'Address': 'fe80::1/64',
                 'ListenPort': 51820,
                 'PrivateKey': '6FYKQKEtGFAb5HSwyj5cQl3wgS1E9d6SqVjdVksOn2s=',
                 'TestAttr': 42,
                 '_index_firstline': 0,
                 '_index_lastline': 7}
    del wc.interface['_rawdata']
    assert wc.interface == interface

def test_add_interface_attr_with_comment(setup_testconfig1):
    wc = setup_testconfig1
    wc.add_attr(None, 'TestAttr', 42, '# Leading comment')
    output_data(wc)
    interface = {'Address': 'fe80::1/64',
                 'ListenPort': 51820,
                 'PrivateKey': '6FYKQKEtGFAb5HSwyj5cQl3wgS1E9d6SqVjdVksOn2s=',
                 'TestAttr': 42,
                 '_index_firstline': 0,
                 '_index_lastline': 8}
    del wc.interface['_rawdata']
    assert wc.interface == interface

def test_del_interface_attr1(setup_testconfig1):
    wc = setup_testconfig1
    wc.del_attr(None, 'ListenPort', remove_leading_comments=False)
    output_data(wc)
    interface = {'Address': 'fe80::1/64',
                 'PrivateKey': '6FYKQKEtGFAb5HSwyj5cQl3wgS1E9d6SqVjdVksOn2s=',
                 '_index_firstline': 0,
                 '_index_lastline': 5}
    del wc.interface['_rawdata']
    assert wc.interface == interface

def test_del_interface_attr2(setup_testconfig1):
    wc = setup_testconfig1
    wc.del_attr(None, 'ListenPort', 51820, remove_leading_comments=False)
    output_data(wc)
    interface = {'Address': 'fe80::1/64',
                 'PrivateKey': '6FYKQKEtGFAb5HSwyj5cQl3wgS1E9d6SqVjdVksOn2s=',
                 '_index_firstline': 0,
                 '_index_lastline': 5}
    del wc.interface['_rawdata']
    assert wc.interface == interface

def test_del_interface_attr_with_comment(setup_testconfig1):
    wc = setup_testconfig1
    wc.del_attr(None, 'ListenPort')
    output_data(wc)
    interface = {'Address': 'fe80::1/64',
                 'PrivateKey': '6FYKQKEtGFAb5HSwyj5cQl3wgS1E9d6SqVjdVksOn2s=',
                 '_index_firstline': 0,
                 '_index_lastline': 4}
    del wc.interface['_rawdata']
    assert wc.interface == interface

def test_add_peer(setup_testconfig1):
    wc = setup_testconfig1
    wc.add_peer('801mgm2JhjTOCxfihEknzFJGYxDvi+8oVYBrWe3hOWM=')
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                             '9999::2/128'],
                                                             'Endpoint': '192.168.0.2:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 24},
             '801mgm2JhjTOCxfihEknzFJGYxDvi+8oVYBrWe3hOWM=': {'PublicKey': '801mgm2JhjTOCxfihEknzFJGYxDvi+8oVYBrWe3hOWM=',
                                                             '_index_firstline': 26,
                                                             '_index_lastline': 27}}
    for peer in list(wc.peers.values()):
        del peer['_rawdata']
    assert wc.peers == peers, 'peer incorrectly added'

def test_add_peer_with_comment(setup_testconfig1):
    wc = setup_testconfig1
    wc.add_peer('801mgm2JhjTOCxfihEknzFJGYxDvi+8oVYBrWe3hOWM=', '# Newly added peer')
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                             '9999::2/128'],
                                                             'Endpoint': '192.168.0.2:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 24},
             '801mgm2JhjTOCxfihEknzFJGYxDvi+8oVYBrWe3hOWM=': {'PublicKey': '801mgm2JhjTOCxfihEknzFJGYxDvi+8oVYBrWe3hOWM=',
                                                             '_index_firstline': 26,
                                                             '_index_lastline': 28}}
    for peer in list(wc.peers.values()):
        del peer['_rawdata']
    assert wc.peers == peers, 'peer (with comment) incorrectly added'

def test_del_peer1(setup_testconfig1):
    wc = setup_testconfig1
    wc.del_peer('XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=')
    output_data(wc)
    peers = {'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15}}
    for peer in list(wc.peers.values()):
        del peer['_rawdata']
    assert wc.peers == peers, 'first peer incorrectly deleted'
    interface = {'Address': 'fe80::1/64',
                 'ListenPort': 51820,
                 'PrivateKey': '6FYKQKEtGFAb5HSwyj5cQl3wgS1E9d6SqVjdVksOn2s=',
                 '_index_firstline': 0,
                 '_index_lastline': 6}
    del wc.interface['_rawdata']
    assert wc.interface == interface, 'first peer incorrectly deleted'

def test_del_peer2(setup_testconfig1):
    wc = setup_testconfig1
    wc.del_peer('eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=')
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': ['fe80::2/128',
                                                                             '9999::2/128'],
                                                             'Endpoint': '192.168.0.2:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15}}
    for peer in list(wc.peers.values()):
        del peer['_rawdata']
    assert wc.peers == peers, 'second peer incorrectly deleted'
    interface = {'Address': 'fe80::1/64',
                 'ListenPort': 51820,
                 'PrivateKey': '6FYKQKEtGFAb5HSwyj5cQl3wgS1E9d6SqVjdVksOn2s=',
                 '_index_firstline': 0,
                 '_index_lastline': 6}
    del wc.interface['_rawdata']
    assert wc.interface == interface, 'second peer incorrectly deleted'

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
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 24}}
    for peer in list(wc.peers.values()):
        del peer['_rawdata']
    assert wc.peers == peers

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
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 16},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_index_firstline': 18,
                                                             '_index_lastline': 25}}
    for peer in list(wc.peers.values()):
        del peer['_rawdata']
    assert wc.peers == peers

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
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128',
                                                                             '10.0.0.1/16'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 25}}
    for peer in list(wc.peers.values()):
        del peer['_rawdata']
    assert wc.peers == peers

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
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128',
                                                                             '10.0.0.1/16'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 26}}
    for peer in list(wc.peers.values()):
        del peer['_rawdata']
    assert wc.peers == peers

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
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             'TestAttr': 42,
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 25}}
    for peer in list(wc.peers.values()):
        del peer['_rawdata']
    assert wc.peers == peers

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
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             'TestAttr': 42,
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 26}}
    for peer in list(wc.peers.values()):
        del peer['_rawdata']
    assert wc.peers == peers

def test_del_attr1(setup_testconfig1):
    """del_attr: all attribute occurences where just once present"""
    wc = setup_testconfig1
    wc.del_attr('XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=', 'AllowedIPs')
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'Endpoint': '192.168.0.2:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 14},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_index_firstline': 16,
                                                             '_index_lastline': 23}}
    for peer in list(wc.peers.values()):
        del peer['_rawdata']
    assert wc.peers == peers

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
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 22}}
    for peer in list(wc.peers.values()):
        del peer['_rawdata']
    assert wc.peers == peers

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
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 22}}
    for peer in list(wc.peers.values()):
        del peer['_rawdata']
    assert wc.peers == peers

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
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 23}}
    for peer in list(wc.peers.values()):
        del peer['_rawdata']
    assert wc.peers == peers

def test_del_attr5(setup_testconfig1):
    """del_attr: delete a single value from an attribute where two values are present in a single line"""
    wc = setup_testconfig1
    wc.del_attr('XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=', 'AllowedIPs', 'fe80::2/128')
    output_data(wc)
    peers = {'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=': {'AllowedIPs': '9999::2/128',
                                                             'Endpoint': '192.168.0.2:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'XWItB4SR1qwGbGn59oRE6TBlTYHQF0pDy1x63dlr5nA=',
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': ['fe80::3/128',
                                                                             '9999::3/128'],
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 24}}
    for peer in list(wc.peers.values()):
        del peer['_rawdata']
    assert wc.peers == peers
    
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
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': '9999::3/128',
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 23}}
    for peer in list(wc.peers.values()):
        del peer['_rawdata']
    assert wc.peers == peers
    
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
                                                             '_index_firstline': 8,
                                                             '_index_lastline': 15},
             'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=': {'AllowedIPs': 'fe80::3/128',
                                                             'Endpoint': '192.168.0.3:51820',
                                                             'PersistentKeepalive': 25,
                                                             'PublicKey': 'eBvBVLo6wH0XkBfIjeLPf8ydBTfU/gMqJOH4nmVXcDE=',
                                                             '_index_firstline': 17,
                                                             '_index_lastline': 23}}
    for peer in list(wc.peers.values()):
        del peer['_rawdata']
    assert wc.peers == peers
