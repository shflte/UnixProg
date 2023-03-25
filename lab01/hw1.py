#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import hashlib
import time
from pwn import *

def solve_pow(r):
    prefix = r.recvline().decode().split("'")[1]
    print(time.time(), "solving pow ...")
    solved = b''
    for i in range(1000000000):
        h = hashlib.sha1((prefix + str(i)).encode()).hexdigest()
        if h[:6] == '000000':
            solved = str(i).encode()
            print("solved =", solved)
            break;
    print(time.time(), "done.")

    r.sendlineafter(b'string S: ', base64.b64encode(solved))

if __name__ == '__main__':
    r = remote('up23.zoolab.org', 10363)
    # solve pow
    solve_pow(r)
    print(r.recvuntil(b'the ', drop=True))
    print(r.recvuntil(b'the ', drop=True))
    nums = int(r.recvuntil(b' ', drop = True))
    print(nums)

    for i in range(nums):
        r.recvuntil(b':', drop=True)
        problem = r.recvuntil(b'=', drop=True)
        s = problem.decode('UTF-8')
        res = eval(s)
        res = int(res)
        byte_string = res.to_bytes((res.bit_length() + 7) // 8, byteorder='little')
        r.sendlineafter(b'?', base64.b64encode(byte_string))
    print(r.recvline())   

    r.close()

# vim: set tabstop=4 expandtab shiftwidth=4 softtabstop=4 number cindent fileencoding=utf-8 :
