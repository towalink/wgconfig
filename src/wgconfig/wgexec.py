# -*- coding: utf-8 -*-

"""Simple wrapper around WireGuard commands"""

import logging
import shlex
import subprocess


logger = logging.getLogger(__name__);


def execute(command, input=None, suppressoutput=False, suppresserrors=False):
    """Execute a command"""
    args = shlex.split(command)
    stdin = None if input is None else subprocess.PIPE
    input = None if input is None else input.encode('utf-8')
    nsp = subprocess.Popen(args, stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = nsp.communicate(input=input)
    if err is not None:
        err = err.decode('utf8')
        if not suppresserrors and (len(err) > 0):
            logger.error(err)
    out = out.decode('utf8')
    if not suppressoutput and (len(out) > 0):
        print(out)
    nsp.wait()
    return out, err, nsp.returncode
    
def generate_privatekey():
    """Generates a WireGuard private key"""
    out, err, returncode = execute('wg genkey', suppressoutput=True)
    if (returncode != 0) or (len(err) > 0):
        return None
    out = out.strip() # remove trailing newline
    return out
    
def get_publickey(wg_private):
    """Gets the public key belonging to the given WireGuard private key"""
    if wg_private is None:
        return None
    out, err, returncode = execute('wg pubkey', input=wg_private, suppressoutput=True)
    if (returncode != 0) or (len(err) > 0):
        return None
    out = out.strip() # remove trailing newline
    return out

def generate_keypair():
    """Generates a WireGuard key pair (returns tuple of private key and public key)"""
    wg_private = generate_privatekey()
    wg_public = get_publickey(wg_private)
    return wg_private, wg_public

def generate_presharedkey():
    """Generates a WireGuard preshared key"""
    out, err, returncode = execute('wg genpsk', suppressoutput=True)
    if (returncode != 0) or (len(err) > 0):
        return None
    out = out.strip() # remove trailing newline
    return out
