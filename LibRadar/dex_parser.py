#!/usr/bin/env python
#coding:utf-8

# BSD 2-Clause License
#
# Copyright (c) [2016], [guanchao wen], shuwoom.wgc@gmail.com
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import binascii

def byte_to_buma(val):
    binVal = bin(val)[2:].zfill(8)
    if binVal[0:1] == '0':
        return val
    sb = ''
    for i in range(7):
        if binVal[i+1:i+2] == '0':
            sb += '1'
        else:
            sb += '0'

    return -(int(sb, 2) + 1)

def word_to_buma(val):
    binVal = bin(val)[2:].zfill(16)
    if binVal[0:1] == '0':
        return val
    sb = ''
    for i in range(15):
        if binVal[i+1:i+2] == '0':
            sb += '1'
        else:
            sb += '0'

    return -(int(sb, 2) + 1)

"""

# Not Used?  zachary 20170105

def dword_to_buma(val):
    binVal = bin(val)[2:].zfill(32)
    if binVal[0:1] == '0':
        return val
    sb = ''
    for i in range(31):
        if binVal[i+1:i+2] == '0':
            sb += '1'
        else:
            sb += '0'

    return -(int(sb, 2) + 1)
"""
"""
############### OPCODE #################
"""
def getOpCode(opcode):
    """
    参考: dalvik-bytecode
    """
    if opcode == 0x00 : return '10x', 'nop'
    if opcode == 0x01 : return '12x', 'move vA, vB'
    if opcode == 0x02 : return '22x', 'move/from16 vAA, vBBBB'
    if opcode == 0x03 : return '32x', 'move/16 vAAAA, vBBBB'
    if opcode == 0x04 : return '12x', 'move-wide vA, vB'
    if opcode == 0x05 : return '22x', 'move-wide/from16 vAA, vBBBB'
    if opcode == 0x06 : return '32x', 'move-wide/16 vAAAA, vBBBB'
    if opcode == 0x07 : return '12x', 'move-object vA, vB'
    if opcode == 0x08 : return '22x', 'move-object/from16 vAA, vBBBB'
    if opcode == 0x09 : return '32x', 'move-object/16 vAAAA, vBBBB'
    if opcode == 0xa : return '11x', 'move-result vAA'
    if opcode == 0xb : return '11x', 'move-result-wide vAA'
    if opcode == 0xc : return '11x', 'move-result-object vAA'
    if opcode == 0xd : return '11x', 'move-exception vAA'
    if opcode == 0xe : return '10x', 'return-void'
    if opcode == 0xf : return '11x', 'return vAA'
    if opcode == 0x10 : return '11x', 'return-wide'
    if opcode == 0x11 : return '11x', 'return-object vAA'
    if opcode == 0x12 : return '11n', 'const/4 vA, #+B'
    if opcode == 0x13 : return '21s', 'const/16 vAA, #+BBBB'
    if opcode == 0x14 : return '31i', 'const vAA, #+BBBBBBBB'
    if opcode == 0x15 : return '21h', 'const/high16 vAA, #+BBBB0000'
    if opcode == 0x16 : return '21s', 'const-wide/16 vAA, #+BBBB'
    if opcode == 0x17 : return '31i', 'const-wide/32 vAA, #+BBBBBBBB'
    if opcode == 0x18 : return '51l', 'const-wide vAA, #+BBBBBBBBBBBBBBBB'
    if opcode == 0x19 : return '21h', 'const-wide/high16 vAA, #+BBBB000000000000'
    if opcode == 0x1a : return '21c', 'const-string vAA, string@BBBB'
    if opcode == 0x1b : return '31c', 'const-string/jumbo vAA, string@BBBBBBBB'
    if opcode == 0x1c : return '21c', 'const-class vAA, type@BBBB'
    if opcode == 0x1d : return '11x', 'monitor-enter vAA'
    if opcode == 0x1e : return '11x', 'monitor-exit vAA'
    if opcode == 0x1f : return '21c', 'check-cast vAA, type@BBBB'
    if opcode == 0x20 : return '22c', 'instance-of vA, vB, type@CCCC'
    if opcode == 0x21 : return '12x', 'array-length vA, vB'
    if opcode == 0x22 : return '21c', 'new-instance vAA, type@BBBB'
    if opcode == 0x23 : return '22c', 'new-array vA, vB, type@CCCC'
    if opcode == 0x24 : return '35c', 'filled-new-array {vD, vE, vF, vG, vA}, type@CCCC'
    if opcode == 0x25 : return '3rc', 'filled-new-array/range {vCCCC .. vNNNN}, type@BBBB'
    if opcode == 0x26 : return '31t', 'fill-array-data vAA, +BBBBBBBB'
    if opcode == 0x27 : return '11x', 'throw vAA'
    if opcode == 0x28 : return '10t', 'goto +AA'
    if opcode == 0x29 : return '20t', 'goto/16 +AAAA'
    if opcode == 0x2a : return '30t', 'goto/32 +AAAAAAAA'
    if opcode == 0x2b : return '31t', 'packed-switch vAA, +BBBBBBBB'
    if opcode == 0x2c : return '31t', 'sparse-switch vAA, +BBBBBBBB'
    if opcode >= 0x2d and opcode <= 0x31 : return '23x', 'cmpkind vAA, vBB, vCC'
    if opcode >= 0x32 and opcode <= 0x37 : return '22t', 'if-test vA, vB, +CCCC'
    if opcode >= 0x38 and opcode <= 0x3d : return '21t', 'if-testz vAA, +BBBB'
    if opcode >= 0x3e and opcode <= 0x43 : return '10x', 'unused'
    if opcode >= 0x44 and opcode <= 0x51 : return '23x', 'arrayop vAA, vBB, vCC'
    if opcode >= 0x52 and opcode <= 0x5f : return '22c', 'iinstanceop vA, vB, field@CCCC'
    if opcode >= 0x60 and opcode <= 0x6d: return '21c', 'sstaticop vAA, field@BBBB'
    if opcode >= 0x6e and opcode <= 0x72 : return '35c', 'invoke-kind {vD, vE, vF, vG, vA}, meth@CCCC'
    if opcode == 0x73 : return '10x', 'unused'
    if opcode >= 0x74 and opcode <= 0x78 : return '3rc', 'invoke-kind/range {vCCCC .. vNNNN}, meth@BBBB'
    if opcode >= 0x79 and opcode <= 0x7a : return '10x', 'unused'
    if opcode >= 0x7b and opcode <= 0x8f : return '12x', 'unop vA, vB'
    if opcode >= 0x90 and opcode <= 0xaf : return '23x', 'binop vAA, vBB, vCC'
    if opcode >= 0xb0 and opcode <= 0xcf : return '12x', 'binop/2addr vA, vB'
    if opcode >= 0xd0 and opcode <= 0xd7 : return '22s', 'binop/lit16 vA, vB, #+CCCC'
    if opcode >= 0xd8 and opcode <= 0xe2 : return '22b', 'binop/lit8 vAA, vBB, #+CC'
    if opcode >= 0xe3 and opcode <= 0xfe : return '10x', 'unused'
    if opcode == 0x00ff : return '41c', 'const-class/jumbo vAAAA, type@BBBBBBBB'
    if opcode == 0x01ff : return '41c', 'check-cast/jumbo vAAAA, type@BBBBBBBB'
    if opcode == 0x02ff : return '52c', 'instance-of/jumbo vAAAA, vBBBB, type@CCCCCCCC'
    if opcode == 0x03ff : return '41c', 'new-instance/jumbo vAAAA, type@BBBBBBBB'
    if opcode == 0x04ff : return '52c', 'new-array/jumbo vAAAA, vBBBB, type@CCCCCCCC'
    if opcode == 0x05ff : return '52rc', 'filled-new-array/jumbo {vCCCC .. vNNNN}, type@BBBBBBBB'
    if opcode >= 0x06ff and opcode <= 0x13ff: return '52c', 'iinstanceop/jumbo vAAAA, vBBBB, field@CCCCCCCC'
    if opcode >= 0x14ff and opcode <= 0x21ff: return '41c', 'sstaticop/jumbo vAAAA, field@BBBBBBBB'
    if opcode >= 0x22ff and opcode <= 0x26ff: return '5rc', 'invoke-kind/jumbo {vCCCC .. vNNNN}, meth@BBBBBBBB'

"""
############### OPCODE END #################
"""

"""
############### InstrUtils #################
"""
class DecodedInstruction(object):
    """docstring for DecodedInstruction"""
    def __init__(self):
        super(DecodedInstruction, self).__init__()
        self.vA = None
        self.vB = None
        self.vC = None
        self.vD = None
        self.vE = None
        self.vF = None
        self.vG = None
        self.opcode = None
        self.op = None
        self.indexType = None
        self.smaliCode = None
        # DeCode.insns指令集内相对于起始地址的offset
        self.offset = None
        # 代码片段长度
        self.length = None

def dexDecodeInstruction(dexFile, dexCode, offset):
    byteCounts = offset / 4
    insns = dexCode.insns

    if insns == '':
        return None

    decodedInstruction = DecodedInstruction()
    opcode = int(insns[offset:offset+2], 16)
    formatIns, syntax = getOpCode(opcode)

    decodedInstruction.opcode = opcode

    if formatIns == '10x':
        # Format: 00|op <=> op
        # (1) opcode=00 nop
        if opcode == 0x00:
            decodedInstruction.op = 'nop'
            decodedInstruction.smaliCode = 'nop'
            decodedInstruction.offset = offset
            decodedInstruction.length = 4

        # (2) opcode=0e return-void
        if opcode == 0x0e:
            decodedInstruction.op = 'return-void'
            decodedInstruction.smaliCode = 'return-void'
            decodedInstruction.offset = offset
            decodedInstruction.length = 4

        # (3) opcode=3e..43 unused
        if opcode >= 0x3e and opcode <= 0x43:
            decodedInstruction.op = 'unused'
            decodedInstruction.smaliCode = 'unused'
            decodedInstruction.offset = offset
            decodedInstruction.length = 4

        # (4) opcode=73 unused
        if opcode == 0x73:
            decodedInstruction.op = 'unused'
            decodedInstruction.smaliCode = 'unused'
            decodedInstruction.offset = offset
            decodedInstruction.length = 4

        # (5) opcode=79..7a unused
        if opcode >= 0x79 and opcode <= 0x7a:
            decodedInstruction.op = 'unused'
            decodedInstruction.smaliCode = 'unused'
            decodedInstruction.offset = offset
            decodedInstruction.length = 4

        # (6) opcode=e3..fe unused
        if opcode >= 0xe3 and opcode <= 0xfe:
            decodedInstruction.op = 'unused'
            decodedInstruction.smaliCode = 'unused'
            decodedInstruction.offset = offset
            decodedInstruction.length = 4

    elif formatIns == '12x': # op vA, vB
        # Format: B|A|op <=> op vA, vB
        op = '????'
        # (1) opcode=01 move vA, vB
        if opcode == 0x01:
            op = 'move'
        # (2) opcode=04 move-wide vA, vB
        if opcode == 0x04:
            op = 'move-wide'
        # (3) opcode=07 move-object vA, vB
        if opcode == 0x07:
            op = 'move-object'
        # (4) opcode=21 array-length vA, vB
        if opcode == 0x21:
            op = 'array-length'
        # (5) opcode7b..8f unop vA, vB
        if opcode >= 0x7b and opcode <= 0x8f:
            unop = ['neg-int', 'not-int', 'neg-long', 'not-long', 'neg-float', 'neg-double', 'int-to-long', 'int-to-float', 'int-to-double',
                    'long-to-int', 'long-to-float', 'long-to-double', 'float-to-int', 'float-to-long', 'float-to-double',
                    'double-to-int', 'double-to-long', 'double-to-float', 'int-to-byte', 'int-to-char', 'int-to-short']
            op = unop[opcode - 0x7b]
        # (6) opcode=b0..cf binop/2addr vA, vB
        if opcode >= 0xb0 and opcode <= 0xcf:
            ops = ['add-int/2addr', 'sub-int/2addr', 'mul-int/2addr', 'div-int/2addr', 'rem-int/2addr', 'and-int/2addr', 'or-int/2addr', 'xor-int/2addr', 'shl-int/2addr', 'shr-int/2addr', 'ushr-int/2addr',
                     'add-long/2addr', 'sub-long/2addr', 'mul-long/2addr', 'div-long/2addr', 'rem-long/2addr', 'and-long/2addr', 'or-long/2addr', 'xor-long/2addr', 'shl-long/2addr', 'shr-long/2addr','ushr-long/2addr',
                     'add-float/2addr', 'sub-float/2addr', 'mul-float/2addr', 'div-float/2addr', 'rem-float/2addr',
                     'add-double/2addr', 'sub-double/2addr', 'mul-double/2addr', 'div-double/2addr', 'rem-double/2addr']
            op = ops[opcode - 0xb0]

        B = int(insns[offset + 2:offset + 3], 16)
        A = int(insns[offset + 3:offset + 4], 16)

        decodedInstruction.op = op
        decodedInstruction.vA = A
        decodedInstruction.vB = B
        decodedInstruction.smaliCode = '%s v%d, v%d' % (op, A, B)
        decodedInstruction.offset = offset
        decodedInstruction.length = 4

    elif formatIns == '11n':
        # Format: B|A|op <=> # op vA, #+B
        # (1) opcode=12 const/4 vA, #+B
        B = int(insns[offset+2:offset+3], 16)
        A = int(insns[offset+3:offset+4], 16)

        decodedInstruction.op = 'const/4'
        decodedInstruction.vA = A
        decodedInstruction.B = B
        decodedInstruction.smaliCode = 'const/4 v%d, #+%d' % (A, B)
        decodedInstruction.offset = offset
        decodedInstruction.length = 4

    elif formatIns == '11x':
        # Format: AA|op <=> # op vAA
        op = '????'
        # (1) opcode=0a move-result vAA
        if opcode == 0x0a:
            op = 'move-result'
        # (2) opcode=0b move-result-wide vAA
        if opcode == 0x0b:
            op = 'move-result-wide'
        # (3) opcode=0c move-result-object vAA
        if opcode == 0x0c:
            op = 'move-result-object'
        # (4) opcode=0d move-exception vAA
        if opcode == 0x0d:
            op = 'move-exception'
        # (5) opcode=0f return vAA
        if opcode == 0x0f:
            op = 'return'
        # (6) opcode=10 return-wide vAA
        if opcode == 0x10:
            op = 'return-wide'
        # (7) opcode=11 return-object vAA
        if opcode == 0x11:
            op = 'return-object'
        # (8) opcode=1d monitor-enter vAA
        if opcode == 0x1d:
            op = 'monitor-enter'
        # (9) opcode=1e monitor-exit vAA
        if opcode == 0x1e:
            op = 'monitor-exit'
        # (10) opcode=27 throw vAA
        if opcode == 0x27:
            op = 'throw'

        AA = int(insns[offset + 2:offset + 4], 16)

        decodedInstruction.op = op
        decodedInstruction.vA = AA
        decodedInstruction.smaliCode = '%s v%d' % (op, AA)
        decodedInstruction.offset = offset
        decodedInstruction.length = 4

    elif formatIns == '10t':
        # Format: AA|op <=> # op +AA
        # (1) opcode=28 goto +AA
        AA = int(insns[offset + 2:offset + 4], 16)
        buma = byte_to_buma(AA)

        decodedInstruction.op = 'goto'
        decodedInstruction.vA = AA
        decodedInstruction.smaliCode = 'goto %s //%s' % (hex(offset/4+buma), hex(buma))
        decodedInstruction.offset = offset
        decodedInstruction.length = 4

    elif formatIns == '20t':
        # Format: 00|op AAAA <=> # op +vAAAA
        # (1) opcode=29 goto/16 +AAAA
        if opcode == 0x29:
            AAAA = int(insns[offset + 2:offset + 8], 16)
            buma = word_to_buma(int(insns[offset + 4:offset + 8].decode('hex')[::-1].encode('hex'), 16))

            decodedInstruction.op = 'goto/16'
            decodedInstruction.vA = AAAA
            decodedInstruction.smaliCode = 'goto/16 %s //%s' % (hex(offset/4+buma), hex(buma))
            decodedInstruction.offset = offset
            decodedInstruction.length = 8

    elif formatIns == '20bc':
        # Format: AA|op BBBB <=> op AA, kind@BBBB
        # 无opcode
        pass
    elif formatIns == '22x':
        # Format: AA|op BBBB <=> op vAA, vBBBB
        op = '????'
        # (1) opcode=02 move/from16 vAA, vBBBB
        if opcode == 0x02:
            op = 'move/from16'
        # (2) opcode=05 move-wide/from16 vAA, vBBBB
        if opcode == 0x05:
            op = 'move-wide/from16'
        # (3) opcode=08 move-object/from16 vAA, vBBBB
        if opcode == 0x08:
            op = 'move-object/from16'

        AA = int(insns[offset + 2:offset + 4], 16)
        BBBB = int(insns[offset + 4:offset + 8].decode('hex')[::-1].encode('hex'), 16)

        decodedInstruction.op = op
        decodedInstruction.vA = AA
        decodedInstruction.vB = BBBB
        decodedInstruction.smaliCode = '%s v%d, v%s' % (op, AA, BBBB)
        decodedInstruction.offset = offset
        decodedInstruction.length = 8

    elif formatIns == '21t':
        # Format: AA|op BBBB <=> op vAA, +BBBB
        op = '????'
        # (1) opcode=38..3d if-testz vAA, +BBBB
        if opcode >= 0x38 and opcode <= 0x3d:
            ops = ['if-eqz', 'if-nez', 'if-ltz', 'if-gez', 'if-gtz', 'if-lez']
            op = ops[opcode - 0x38]

        AA = int(insns[offset + 2:offset + 4], 16)
        BBBB = int(insns[offset + 4:offset + 8].decode('hex')[::-1].encode('hex'), 16)

        decodedInstruction.op = op
        decodedInstruction.vA = AA
        decodedInstruction.vB = BBBB
        decodedInstruction.smaliCode = '%s v%d, %s //+%s' % (op, AA, hex(BBBB+offset/4), hex(BBBB))
        decodedInstruction.offset = offset
        decodedInstruction.length = 8

    elif formatIns == '21s':
        # Format: AA|op BBBB <=> op vAA, #+BBBB
        op = '????'
        # (1) opcode=13 const/16 vAA, #_BBBB
        if opcode == 0x13:
            op = 'const/16'
        # (2) opcode=16 const-wide/16 vAA, #+BBBB
        if opcode == 0x16:
            op = 'const-wide/16'

        AA = int(insns[offset + 2:offset + 4], 16)
        BBBB = int(insns[offset + 4:offset + 8].decode('hex')[::-1].encode('hex'), 16)

        decodedInstruction.op = op
        decodedInstruction.vA = AA
        decodedInstruction.vB = BBBB
        decodedInstruction.smaliCode = '%s v%d, #+%s' % (op, AA, BBBB)
        decodedInstruction.offset = offset
        decodedInstruction.length = 8

    elif formatIns == '21h':
        # Format: AA|op BBBB <=> op vAA, #+BBBB0000[00000000]
        AA = int(insns[offset + 2:offset + 4], 16)
        BBBB = insns[offset + 4:offset + 8].decode('hex')[::-1].encode('hex')

        # (1) opcode=15 const/high16 vAA, #+BBBB0000
        if opcode == 0x15:
            op = 'const/high16'

            decodedInstruction.op = op
            decodedInstruction.vA = AA
            decodedInstruction.vB = int(BBBB + '0000', 16)
            decodedInstruction.smaliCode = '%s v%d, #+%s' % (op, AA, int(BBBB + '0000', 16))
            decodedInstruction.offset = offset
            decodedInstruction.length = 8

        # (2) opcode=19 const-wide/high16 vAA, #+BBBB000000000000
        if opcode == 0x19:
            op = 'const-wide/high16'

            decodedInstruction.op = op
            decodedInstruction.vA = AA
            decodedInstruction.vB = int(BBBB + '000000000000', 16)
            decodedInstruction.smaliCode = '%s v%d, #+%s' % (op, AA, int(BBBB + '000000000000', 16))
            decodedInstruction.offset = offset
            decodedInstruction.length = 8

    elif formatIns == '21c':
        # Format: AA|op BBBB <=> op vAA, [type|field|string]@BBBB
        indexType = '????'
        op = '????'
        indexStr = ''

        AA = int(insns[offset + 2:offset + 4], 16)
        BBBB = insns[offset + 4:offset + 8].decode('hex')[::-1].encode('hex')

        # (1) opcode=1a const-string vAA, string@BBBB
        if opcode == 0x1a:
            op = 'const-string'
            indexType = 'string'
            indexStr = dexFile.getDexStringId(int(BBBB, 16))
        # (2) opcode=1c const-class vAA, type@BBBB
        if opcode == 0x1c:
            op = 'const-class'
            indexType = 'type'
            indexStr = dexFile.getDexTypeId(int(BBBB, 16))
        # (3) opcode=1f check-cast vAA, type@BBBB
        if opcode == 0x1f:
            op = 'check-cast'
            indexType = 'type'
            indexStr = dexFile.getDexTypeId(int(BBBB, 16))
        # (4) opcode=22 new-instance vAA, type@BBBB
        if opcode == 0x22:
            op = 'new-instance'
            indexType = 'type'
            indexStr = dexFile.getDexTypeId(int(BBBB, 16))
        # (5) opcode=60..6d sstaticop vAA, field@BBBB
        if opcode >= 0x60 and opcode <=0x6d:
            sstaticop = ['sget', 'sget-wide', 'sget-object', 'sget-boolean', 'sget-byte', 'sget-char',
                         'sget-char', 'sget-short', 'sput', 'sput-wide', 'sput-object', 'sput-boolean',
                         'sput-byte', 'sput-char', 'sput-short']
            op = sstaticop[opcode - 0x60]
            indexType = 'field'
            dexFieldIdObj = dexFile.DexFieldIdList[int(BBBB, 16)]
            indexStr = dexFieldIdObj.toString(dexFile)

        decodedInstruction.op = op
        decodedInstruction.vA = AA
        decodedInstruction.vB = int(BBBB, 16)
        decodedInstruction.indexType = indexType
        decodedInstruction.smaliCode = '%s v%d, %s@%s //%s' % (op, AA, indexType, BBBB, indexStr)
        decodedInstruction.offset = offset
        decodedInstruction.length = 8

    elif formatIns == '23x':
        # Format: AA|op CC|BB <=> op vAA, vBB, vCC
        op = '????'
        # (1) opcode=2d..31 cmpkind vAA, vBB, vCC
        if opcode >= 0x2d and opcode <= 0x31:
            cmpkind = ['cmpl-float', 'cmpg-float', 'cmpl-double', 'cmpg-double', 'cmp-long']
            op =cmpkind[opcode - 0x2d]
        # (2) opcode=44..51 arrayop vAA, vBB, vCC
        if opcode >= 0x44 and opcode <= 0x51:
            arrayop = ['aget', 'aget-wide', 'aget-object', 'aget-boolean', 'aget-byte', 'aget-char', 'aget-short',
                       'aput', 'aput-wide', 'aput-object', 'aput-boolean', 'aput-byte', 'aput-char', 'aput-short']
            op = arrayop[opcode - 0x44]
        # (3) opcode=90..af binop vAA, vBB, vCC
        if opcode >= 0x90 and opcode <= 0xaf:
            binop = ['add-int', 'sub-int', 'mul-int', 'div-int', 'rem-int', 'and-int', 'or-int', 'xor-int', 'shl-int', 'shr-int', 'ushr-int',
                     'add-long', 'sub-long', 'mul-long', 'div-long', 'rem-long', 'and-long', 'or-long', 'xor-long', 'shl-long', 'shr-long', 'ushr-long',
                     'add-float', 'sub-float', 'mul-float', 'div-float', 'rem-float',
                     'add-double', 'sub-double', 'mul-double', 'div-double', 'rem-double']
            op = binop[opcode - 0x90]

        AA = int(insns[offset + 2:offset + 4], 16)
        BB = int(insns[offset + 4:offset + 6], 16)
        CC = int(insns[offset + 6:offset + 8], 16)

        decodedInstruction.op = op
        decodedInstruction.vA = AA
        decodedInstruction.vB = BB
        decodedInstruction.vC = CC
        decodedInstruction.smaliCode = '%s v%d, v%d, v%d' % (op, AA, BB, CC)
        decodedInstruction.offset = offset
        decodedInstruction.length = 8

    elif formatIns == '22b':
        # Format: AA|op CC|BB <=> op vAA, vBB, #+CC
        # (1) opcode=d8..e2 binop/lit8 vAA, vBB, #+CC
        if opcode >= 0xd8 and opcode <= 0xe2:
            ops = ['add-int/lit8', 'rsub-int/lit8', 'mul-int/lit8', 'div-int/lit8', 'rem-int/lit8', 'and-int/lit8',
                   'or-int/lit8', 'xor-int/lit8', 'shl-int/lit8', 'shr-int/lit8', 'ushr-int/lit8']
            op = ops[opcode - 0xd8]

        AA = int(insns[offset + 2:offset + 4], 16)
        BB = int(insns[offset + 4:offset + 6], 16)
        CC = int(insns[offset + 6:offset + 8], 16)

        decodedInstruction.op = op
        decodedInstruction.vA = AA
        decodedInstruction.vB = BB
        decodedInstruction.vC = CC
        decodedInstruction.smaliCode = '%s v%d, v%d, #+v%d' % (op, AA, BB, CC)
        decodedInstruction.offset = offset
        decodedInstruction.length = 8

    elif formatIns == '22t':
        # Format: B|A|op CCCC <=> op vA, vB, +CCCC
        op = '????'
        # (1) opcode=32..37 if-test vA, vB, +CCCC
        if opcode >=0x32 and opcode <= 0x37:
            ops = ['if-eq', 'if-ne', 'if-lt', 'if-ge', 'if-gt', 'if-le']
            op = ops[opcode - 0x32]
        B = int(insns[offset + 2: offset + 3], 16)
        A = int(insns[offset + 3: offset + 4], 16)
        CCCC = insns[offset+4:offset+8].decode('hex')[::-1].encode('hex')

        decodedInstruction.op = op
        decodedInstruction.vA = A
        decodedInstruction.vB = B
        decodedInstruction.vC = CCCC
        decodedInstruction.smaliCode = '%s v%d, v%d, %s // +%s' % (op, A, B, hex(offset/4+int(CCCC, 16)), CCCC)
        decodedInstruction.offset = offset
        decodedInstruction.length = 8

    elif formatIns == '22s':
        # Format: B|A|op CCCC <=> op vA, vB, #+CCCC
        op = '????'
        # (1) opcode=d0..d7 binop/lit16 vA, vB, #+CCCC
        if opcode >= 0xd0 and opcode <= 0xd7:
            ops = ['add-int/lit16', 'rsub-int', 'mul-int/lit16', 'div-int/lit16', 'rem-int/lit16', 'and-int/lit16', 'or-int/lit16', 'xor-int/lit16']
            op = ops[opcode - 0xd0]

        B = int(insns[offset + 2: offset + 3], 16)
        A = int(insns[offset + 3: offset + 4], 16)
        CCCC = insns[offset + 4:offset + 8].decode('hex')[::-1].encode('hex')

        decodedInstruction.op = op
        decodedInstruction.vA = A
        decodedInstruction.vB = B
        decodedInstruction.vC = int(CCCC, 16)
        decodedInstruction.smaliCode = '%s v%d, v%d, #+%s' % (op, A, B, CCCC)
        decodedInstruction.offset = offset
        decodedInstruction.length = 8

    elif formatIns == '22c':
        # Format: B|A|op CCCC <=> op vA, vB, [type|field]@CCCC
        op = '????'
        indexType = '????'
        indexStr = ''

        B = int(insns[offset + 2:offset + 3], 16)
        A = int(insns[offset + 3:offset + 4], 16)
        CCCC = insns[offset + 4:offset + 8].decode('hex')[::-1].encode('hex')

        # (1) opcode=20 instance-of vA, vB, type@CCCC
        if opcode == 0x20:
            op = 'instance-of'
            indexType = 'type'
            indexStr = dexFile.DexTypeIdList[int(CCCC, 16)]
        # (2) opcode=23 new-array vA, vB, type@CCCC
        if opcode == 0x23:
            op = 'new-array'
            indexType = 'type'
            indexStr = dexFile.DexTypeIdList[int(CCCC, 16)]
        # (3) opcode=52..5f iinstanceop vA, vB, field@CCCC
        if opcode >= 0x52 and opcode <= 0x5f:
            iinstanceop = ['iget', 'iget-wide', 'iget-object', 'iget-boolean', 'iget-byte', 'iget-char', 'iget-short',
                           'iput', 'iput-wide', 'iput-object', 'iput-boolean', 'iput-byte', 'iput-char', 'put-short']
            op = iinstanceop[opcode - 0x52]
            indexType = 'field'
            dexFieldIdObj = dexFile.DexFieldIdList[int(CCCC, 16)]
            indexStr = dexFieldIdObj.toString(dexFile)

        decodedInstruction.op = op
        decodedInstruction.vA = A
        decodedInstruction.vB = B
        decodedInstruction.vC = int(CCCC, 16)
        decodedInstruction.indexType = indexType
        decodedInstruction.smaliCode = '%s v%d, v%d %s@%s //%s' % (op, A, B, indexType, CCCC, indexStr)
        decodedInstruction.offset = offset
        decodedInstruction.length = 8

    elif formatIns == '22cs':
        # Format: B|A|op CCCC <=> op vA, vB, fieldoff@CCCC
        # 无opcode
        pass
    elif formatIns == '30t':
        # Format: ØØ|op AAAAlo AAAAhi <=> op +AAAAAAAA
        # (1) opcode=2a goto/32 +AAAAAAAA
        if opcode == 0x2a:
            AAAAAAAA = insns[offset + 2:offset + 12].decode('hex')[::-1].encode('hex')
            buma = word_to_buma(int(insns[offset + 4:offset + 12].decode('hex')[::-1].encode('hex'), 16))

            decodedInstruction.op = 'goto/32'
            decodedInstruction.vA = int(AAAAAAAA, 16)
            decodedInstruction.smaliCode = 'goto/32 %s //%s' % (hex(offset/4+buma), hex(buma))
            decodedInstruction.offset = offset
            decodedInstruction.length = 12

    elif formatIns == '32x':
        # Format: ØØ|op AAAA BBBB <=> op vAAAA, vBBBB
        op = '????'
        # (1) opcode=03 move/16 vAAAA, vBBBB
        # (2) opcode=06 move-wide/16 vAAAA, vBBBB
        # (3) opcode=09 move-object/16 vAAAA, vBBBB
        if opcode == 0x03:
            op = 'move/16'
        if opcode == 0x06:
            op = 'move-wide/16'
        if opcode == 0x09:
            op = 'move-object/16'
        AAAA = insns[offset + 2:offset + 6].decode('hex')[::-1].encode('hex')
        BBBB = insns[offset + 6:offset + 10].decode('hex')[::-1].encode('hex')

        decodedInstruction.op = op
        decodedInstruction.vA = int(AAAA, 16)
        decodedInstruction.vB = int(BBBB, 16)
        decodedInstruction.smaliCode = '%s v%s, v%s' % (op, AAAA, BBBB)
        decodedInstruction.offset = offset
        decodedInstruction.length = 10

    elif formatIns == '31i':
        # Format: AA|op BBBBlo BBBBhi <=> op vAA, #+BBBBBBBB
        op = '????'
        # (1) opcode=14 const vAA, #+BBBBBBBB
        if opcode == 0x14:
            op = 'const'
        # (2) opcode=17 const-wide/32 vAA, #+BBBBBBBB
        if opcode == 0x17:
            op = 'const-wide/32'

        AA = int(insns[offset + 2:offset + 4], 16)
        BBBBBBBB = insns[offset + 4:offset + 12].decode('hex')[::-1].encode('hex')

        decodedInstruction.op = op
        decodedInstruction.vA = AA
        decodedInstruction.vB = int(BBBBBBBB, 16)
        decodedInstruction.smaliCode = '%s v%d, #+%s' % (op, AA, BBBBBBBB)
        decodedInstruction.offset = offset
        decodedInstruction.length = 12

    elif formatIns == '31t':
        # Format: AA|op BBBBlo BBBBhi <=> op vAA, +BBBBBBBB
        op = '????'
        # (1) opcode=26 fill-array-data vAA, +BBBBBBBB
        # (2) opcode=2b packed-switch vAA, +BBBBBBBB
        # (3) opcode=2c sparse-switch vAA, +BBBBBBBB
        if opcode == 0x26:
            op = 'fill-array-data'
        if opcode == 0x2b:
            op = 'packed-switch'
        if opcode == 0x2c:
            op = 'sparse-switch'

        AA = int(insns[offset + 2:offset + 4], 16)
        BBBBBBBB = insns[offset + 4:offset + 12].decode('hex')[::-1].encode('hex')
        pseudo_instructions_offset = int(BBBBBBBB, 16) + byteCounts
        retVal = parsePseudoInstruction(byteCounts, insns, pseudo_instructions_offset * 4)

        decodedInstruction.op = op
        decodedInstruction.vA = AA
        decodedInstruction.vB = int(BBBBBBBB, 16)
        decodedInstruction.smaliCode = '%s v%d, %08x // +%s, %s' % (op, AA, pseudo_instructions_offset, BBBBBBBB, retVal)
        decodedInstruction.offset = offset
        decodedInstruction.length = 12

    elif formatIns == '31c':
        # Format: AA|op BBBBlo BBBBhi <=> op vAA, thing@BBBBBBBB
        op = '????'
        indexStr = ''

        AA = int(insns[offset + 2:offset + 4], 16)
        BBBBBBBB = insns[offset + 4:offset + 12].decode('hex')[::-1].encode('hex')

        # (1) opcode=1b const-string/jumbo vAA, string@BBBBBBBB
        if opcode == 0x1b:
            op = 'const-string/jumbo'
            indexStr = dexFile.DexStringIdList[int(BBBBBBBB, 16)]

            decodedInstruction.op = op
            decodedInstruction.vA = AA
            decodedInstruction.vB = BBBBBBBB
            decodedInstruction.smaliCode = '%s v%d, string@%s //%s' % (op, AA, BBBBBBBB, indexStr)
            decodedInstruction.offset = offset
            decodedInstruction.length = 12

    elif formatIns == '35c':
        # Format: A|G|op BBBB F|E|D|C
        indexType = '????'
        op = '????'
        indexStr = ''

        A = int(insns[offset + 2:offset + 3], 16)
        G = int(insns[offset + 3:offset + 4], 16)
        BBBB = insns[offset + 4:offset + 8].decode('hex')[::-1].encode('hex')

        registerStr = insns[offset + 8:offset + 12].decode('hex')[::-1].encode('hex')
        F = int(registerStr[:1], 16)
        E = int(registerStr[1:2], 16)
        D = int(registerStr[2:3], 16)
        C = int(registerStr[3:4], 16)

        # (1) opcode=24 filled-new-array {vC, vD, vE, vF, vG}, type@BBBB
        if opcode == 0x24:
            op = 'filled-new-array'
            indexType = 'type'
            indexStr = dexFile.DexTypeIdList[int(BBBB, 16)]
        # (2) opcode=62..72 invoke-kind {vC, vD, vE, vF, vG}, method@BBBB
        if opcode >= 0x6e and opcode <= 0x72:
            invoke_kind = ['invoke-virtual', 'invoke-super', 'invoke-direct', 'invoke-static', 'invoke-interface']
            op = invoke_kind[opcode-0x6e]
            indexType = 'method'
            dexMethodIdObj = dexFile.DexMethodIdList[int(BBBB, 16)]
            indexStr = dexMethodIdObj.toString(dexFile)
            decodedInstruction.getApi = dexMethodIdObj.toApi(dexFile)

        registers = None
        if A == 0:  # [A=0] op {}, kind@BBBB
            decodedInstruction.op = op
            decodedInstruction.vA = A
            decodedInstruction.vB = int(BBBB, 16)
            decodedInstruction.indexType = indexType
            decodedInstruction.smaliCode = '%s {}, %s@%s //%s' % (op, indexType, BBBB, indexStr)
            decodedInstruction.offset = offset
            decodedInstruction.length = 12

        elif A == 1:  # [A=1] op {vC}, kind@BBBB
            decodedInstruction.op = op
            decodedInstruction.vA = A
            decodedInstruction.vB = int(BBBB, 16)
            decodedInstruction.vC = C
            decodedInstruction.indexType = indexType
            decodedInstruction.smaliCode = '%s {v%d}, %s@%s //%s' % (op, C, indexType, BBBB, indexStr)
            decodedInstruction.offset = offset
            decodedInstruction.length = 12

        elif A == 2:  # [A=2] op {vC, vD}, kind@BBBB
            decodedInstruction.op = op
            decodedInstruction.vA = A
            decodedInstruction.vB = int(BBBB, 16)
            decodedInstruction.vC = C
            decodedInstruction.vD = D
            decodedInstruction.indexType = indexType
            decodedInstruction.smaliCode = '%s {v%d, v%d}, %s@%s //%s' % (op, C, D, indexType, BBBB, indexStr)
            decodedInstruction.offset = offset
            decodedInstruction.length = 12

        elif A == 3:  # [A=3] op {vC, vD, vE}, kind@BBBB
            decodedInstruction.op = op
            decodedInstruction.vA = A
            decodedInstruction.vB = int(BBBB, 16)
            decodedInstruction.vC = C
            decodedInstruction.vD = D
            decodedInstruction.vE = E
            decodedInstruction.indexType = indexType
            decodedInstruction.smaliCode = '%s {v%d, v%d, v%d}, %s@%s //%s' % (op, C, D, E, indexType, BBBB, indexStr)
            decodedInstruction.offset = offset
            decodedInstruction.length = 12

        elif A == 4:  # [A=4] op {vC, vD, vE, vF}, kind@BBBB
            decodedInstruction.op = op
            decodedInstruction.vA = A
            decodedInstruction.vB = int(BBBB, 16)
            decodedInstruction.vC = C
            decodedInstruction.vD = D
            decodedInstruction.vE = E
            decodedInstruction.vF = F
            decodedInstruction.indexType = indexType
            decodedInstruction.smaliCode = '%s {v%d, v%d, v%d, v%d}, %s@%s //%s' % (op, C, D, E, F, indexType, BBBB, indexStr)
            decodedInstruction.offset = offset
            decodedInstruction.length = 12

        elif A == 5:  # [A=5] op {vC, vD, vE, vF, vG}, type@BBBB
            decodedInstruction.op = op
            decodedInstruction.vA = A
            decodedInstruction.vB = int(BBBB, 16)
            decodedInstruction.vC = C
            decodedInstruction.vD = D
            decodedInstruction.vE = E
            decodedInstruction.vF = F
            decodedInstruction.vG = G
            decodedInstruction.indexType = indexType
            decodedInstruction.smaliCode = '%s {v%d, v%d, v%d, v%d, %d}, %s@%s //%s' % (op, C, D, E, F, G, indexType, BBBB, indexStr)
            decodedInstruction.offset = offset
            decodedInstruction.length = 12

    elif formatIns == '35ms':
        # Format: A|G|op BBBB F|E|D|C
        # 无opcode
        pass

    elif formatIns == '35mi':
        # Format: A|G|op BBBB F|E|D|C
        # 无opcode
        pass

    elif formatIns == '3rc':
        # Format: AA|op BBBB CCCC <=> op {vCCCC .. vNNNN} [method|type]@BBBB
        op = '????'
        indexType = '????'
        indexStr = ''

        AA = int(insns[offset + 2:offset + 4], 16)
        BBBB = insns[offset + 4:offset + 8].decode('hex')[::-1].encode('hex')
        CCCC = int(insns[offset + 8:offset + 12].decode('hex')[::-1].encode('hex'), 16)
        N = AA + CCCC - 1

        # (1) opcode=25 filled-new-array/range {vCCCC .. vNNNN}, type@BBBB
        if opcode == 0x25:
            op = 'fiiled-new-array/range'
            indexType = 'type'
            indexStr = dexFile.DexTypeIdList[int(BBBB, 16)]
        # (2) opcode=74..78 invoke-kind/range {vCCCC .. vNNNN}, method@BBBB
        if opcode >= 0x74 and opcode <= 0x78:
            ops = ['invoke-virtual/range', 'invoke-super/range', 'invoke-direct/range', 'invoke-static/range', 'invoke-intenrface/range']
            op = ops[opcode - 0x74]
            indexType = 'method'
            dexMethodIdObj = dexFile.DexMethodIdList[int(BBBB, 16)]
            indexStr = dexMethodIdObj.toString(dexFile)

        registers = ''
        for i in range(N):
            registers += 'v' + str(CCCC + i) + ','

        decodedInstruction.op = op
        decodedInstruction.vA = AA
        decodedInstruction.vB = int(BBBB, 16)
        decodedInstruction.vC = CCCC
        decodedInstruction.indexType = indexType
        decodedInstruction.smaliCode = '%s {%s} %s@%s //%s' % (op, registers, indexType, BBBB, indexStr)
        decodedInstruction.offset = offset
        decodedInstruction.length = 12

    elif formatIns == '3rms':
        # Format: AA|op BBBB CCCC <=> op {vCCCC .. vNNNN}, vtaboff@BBBB
        # 无opcode
        pass
    elif formatIns == '3rmi':
        # Format: AA|op BBBB CCCC <=> op {vCCCC .. vNNNN}, inline@BBBB
        # 无opcode
        pass
    elif formatIns == '51l':
        # Format: AA|op BBBBlo BBBB BBBB BBBBhi <=>op vAA,#+BBBBBBBBBBBBBBBB
        # (1) opcode=18 const-wide vAA, #+BBBBBBBBBBBBBBBB
        if opcode == 0x18:
            AA = int(insns[offset+2:offset+4], 16)
            BBBBBBBBBBBBBBBB = insns[offset+4:offset+20].decode('hex')[::-1].encode('hex')

            decodedInstruction.op = 'const-wide'
            decodedInstruction.vA = AA
            decodedInstruction.vB = int(BBBBBBBBBBBBBBBB, 16)
            decodedInstruction.smaliCode = 'const-wide v%d, #+%s' % (AA, BBBBBBBBBBBBBBBB)
            decodedInstruction.offset = offset
            decodedInstruction.length = 20


    elif formatIns == '33x':
        # Format: exop BB|AA CCCC <=> exop vAA, vBB, vCCCC
        # 无opcode
        pass
    elif formatIns == '32s':
        # Format: exop BB|AA CCCC <=> exop vAA, vBB, #+CCCC
        # 无opcode
        pass
    elif formatIns == '40sc':
        # Format: exop BBBBlo BBBBhi AAAA <=> exop AAAA, kind@BBBBBBBB
        # 无opcode
        pass

    '''
    expaneded opcode
    opcode为ff，表示后面还有二级opcode
    '''
    if opcode == 0xff:
        expanded_opcode = int(insns[offset:offset + 4].decode('hex')[::-1].encode('hex'), 16)
        formatIns, _ = getOpCode(expanded_opcode)

    if formatIns == '41c':
        expanded_opcode = int(insns[offset:offset + 4].decode('hex')[::-1].encode('hex'), 16)
        # Format: exop BBBBlo BBBBhi AAAA <=> exop vAAAA, [field|type]@BBBBBBBB
        indexType = '????'
        op = '????'
        # (1) expanded_opcode=00ff const-class/jumbo vAAAA, type@BBBBBBBB
        if expanded_opcode == 0x00ff:
            op = 'const-class/jumbo'
            indexType = 'type'
        # (2) expanded_opcode=01ff check-cast/jumbo vAAAA, type@BBBBBBBB
        elif expanded_opcode == 0x01ff:
            op = 'check-cast/jumbo'
            indexType = 'type'
        # (3) expanded_opcode=03ff new-instance/jumbo vAAAA, type@BBBBBBBB
        elif expanded_opcode == 0x03ff:
            op = 'new-instance/jumbo'
            indexType = 'type'
        # (4) expanded_opcode=14ff..21ff sstaticop/jumbo vAAAA, field@BBBBBBBB
        elif expanded_opcode >= 0x14ff and expanded_opcode <= 0x21ff:
            ops = ['sget/jumbo', 'sget-wide/jumbo', 'sget-object/jumbo', 'sget-boolean/jumbo', 'sget-byte/jumbo',
                   'sget-char/jumbo', 'sget-short/jumbo', 'sput/jumbo', 'sput-wide/jumbo', 'sput-object/jumbo',
                   'sput-boolean/jumbo', 'sput-byte/jumbo', 'sput-char/jumbo', 'sput-short/jumbo']
            op = ops[expanded_opcode - 0x14ff]
            indexType = 'field'

        BBBBBBBB = int(insns[offset + 4:offset + 12].decode('hex')[::-1].encode('hex'), 16)
        AAAA = int(insns[offset + 12:offset + 16].decode('hex')[::-1].encode('hex'), 16)

        decodedInstruction.op = op
        decodedInstruction.vA = AAAA
        decodedInstruction.vB = BBBBBBBB
        decodedInstruction.indexType = indexType
        decodedInstruction.smaliCode = '%s v%d, %s@%s' % (op, AAAA, indexType, hex(BBBBBBBB)[2:])
        decodedInstruction.offset = offset
        decodedInstruction.length = 16

    elif formatIns == '52c':
        expanded_opcode = int(insns[offset:offset + 4].decode('hex')[::-1].encode('hex'), 16)
        indexType = '????'
        op = '????'
        # Format: exop CCCClo CCCChi AAAA BBBB <=> exop vAAAA, vBBBB, [field|type]@CCCCCCCC
        # (1) expanded_opcode=02ff instance-of/jumbo vAAAA, vBBBB, type@CCCCCCCC
        if expanded_opcode == 0x02ff:
            op = 'instance-of/jumbo'
            indexType = 'type'
        # (2) expanded_opcode=04ff new-array/jumbo vAAAA, vBBBB, type@CCCCCCCC
        if expanded_opcode == 0x02ff:
            op = 'new-array/jumbo'
            indexType = 'type'
        # (3) expanded_opcode=06ff..13ff 	iinstanceop/jumbo vAAAA, vBBBB, field@CCCCCCCC
        if expanded_opcode >= 0x06ff and expanded_opcode <= 0x13ff:
            ops = ['iget/jumbo', 'iget-wide/jumbo', 'iget-object/jumbo', 'iget-boolean/jumbo', 'iget-byte/jumbo',
                   'iget-char/jumbo', 'iget-short/jumbo', 'iput/jumbo', 'iput-wide/jumbo', 'iput-object/jumbo',
                   'iput-boolean/jumbo', 'iput-byte/jumbo', 'iput-char/jumbo', 'iput-short/jumbo']
            op = ops[expanded_opcode - 0x06ff]
            indexType = 'field'
        CCCCCCCC = int(insns[offset + 4:offset + 12].decode('hex')[::-1].encode('hex'), 16)
        AAAA = int(insns[offset + 12:offset + 16].decode('hex')[::-1].encode('hex'), 16)
        BBBB = int(insns[offset + 16:offset + 20].decode('hex')[::-1].encode('hex'), 16)

        decodedInstruction.op = op
        decodedInstruction.vA = AAAA
        decodedInstruction.vB = BBBB
        decodedInstruction.vC = CCCCCCCC
        decodedInstruction.indexType = indexType
        decodedInstruction.smaliCode = '%s v%d, v%d %s@%s' % (op, AAAA, BBBB, indexType, hex(CCCCCCCC)[2:])
        decodedInstruction.offset = offset
        decodedInstruction.length = 20

    elif formatIns == '5rc':
        expanded_opcode = int(insns[offset:offset + 4].decode('hex')[::-1].encode('hex'), 16)
        indexType = '????'
        op = '????'
        # Format: exop BBBBlo BBBBhi AAAA CCCC <=> exop {vCCCC .. vNNNN}, [method|type]@BBBBBBBB
        # (1) expanded_opcode=05ff filled-new-array/jumbo {vCCCC .. vNNNN}, type@BBBBBBBB
        if expanded_opcode == 0x05ff:
            op = 'filled-new-array/jumbo'
            indexType = 'type'
        # (2) expanded_opcode=22ff..26ff invoke-kind/jumbo {vCCCC .. vNNNN}, method@BBBBBBBB
        if expanded_opcode >= 0x22ff and expanded_opcode <= 0x26ff:
            ops= ['invoke-virtual/jumbo', 'invoke-super/jumbo', 'invoke-direct/jumbo',
                  'invoke-static/jumbo', 'invoke-interface/jumbo']
            op = ops[expanded_opcode - 0x22ff]
            indexType = 'method'
        BBBBBBBB = int(insns[offset + 4:offset + 12].decode('hex')[::-1].encode('hex'), 16)
        AAAA = int(insns[offset + 12:offset + 16].decode('hex')[::-1].encode('hex'), 16)
        CCCC = int(insns[offset + 16:offset + 20].decode('hex')[::-1].encode('hex'), 16)
        N = AAAA + CCCC - 1

        registers = ''
        for i in range(N):
            registers += 'v' + str(CCCC + i) + ','

        decodedInstruction.op = op
        decodedInstruction.vA = AAAA
        decodedInstruction.vB = BBBBBBBB
        decodedInstruction.vC = CCCC
        decodedInstruction.indexType = indexType
        decodedInstruction.smaliCode = '%s {%s} %s@%s' % (op, registers, indexType, hex(BBBBBBBB)[2:])
        decodedInstruction.offset = offset
        decodedInstruction.length = 20

    return decodedInstruction

def parsePseudoInstruction(opcode_address, insns, offset):
    ident = insns[offset:offset+4].decode('hex')[::-1].encode('hex')
    # packed-switch-payload Format
    if ident == '0100':
        size = int(insns[offset + 4:offset + 8].decode('hex')[::-1].encode('hex'), 16)
        first_key = int(insns[offset+8:offset+16].decode('hex')[::-1].encode('hex'), 16)
        targets = []
        sb = ''
        for i in range(size):
            _v = int(insns[offset+16+8*i:offset+16+8*(i+1)].decode('hex')[::-1].encode('hex'), 16)
            targets.append(_v)
            sb += '    \t%-16scase %d: goto %s\n' % ('', first_key+i, hex(_v + opcode_address))
        return '\n'+sb
    # sparse-switch-payload Format
    if ident == '0200':
        size = int(insns[offset + 4:offset + 8].decode('hex')[::-1].encode('hex'), 16)
        keys = []
        targets = []
        sb = ''
        for i in range(size):
            keys.append(int(insns[offset+8+8*i:offset+8+8*(i+1)].decode('hex')[::-1].encode('hex'), 16))
            _v = int(insns[(offset+8+8*i)+size*8:(offset+8+8*(i+1))+size*8].decode('hex')[::-1].encode('hex'), 16)

            hexNum = _v + opcode_address
            if hexNum > (0xffffffff+1):
                hexNum -= 0xffffffff+1
                tmp = hex(hexNum)
                if tmp.endswith('L'):
                    tmp = tmp[:-1]
                targets.append(tmp)
            else:
                targets.append(hex(hexNum))
            sb += '    \t%-16scase %d: goto %s\n' % ('', keys[i], targets[i])
        return '\n'+sb
    # fill-array-data-payload Format
    if ident == '0300':
        element_width = int(insns[offset + 4:offset + 8].decode('hex')[::-1].encode('hex'), 16)
        size = int(insns[offset + 8:offset + 16].decode('hex')[::-1].encode('hex'), 16)
        data = []

        dataStr = '['
        for i in range(size):
            val = insns[offset + 16 + 2*element_width*i:offset + 16 + 2*element_width*(i+1)]
            data.append(val)
            dataStr += val + ','
        dataStr += ']'
        return dataStr


MAP_ITEM_TYPE_CODES = {
    0x0000 : "kDexTypeHeaderItem",
    0x0001 : "kDexTypeStringIdItem",
    0x0002 : "kDexTypeTypeIdItem",
    0x0003 : "kDexTypeProtoIdItem",
    0x0004 : "kDexTypeFieldIdItem",
    0x0005 : "kDexTypeMethodIdItem",
    0x0006 : "kDexTypeClassDefItem",
    0x1000 : "kDexTypeMapList",
    0x1001 : "kDexTypeTypeList",
    0x1002 : "kDexTypeAnnotationSetRefList",
    0x1003 : "kDexTypeAnnotationSetItem",
    0x2000 : "kDexTypeClassDataItem",
    0x2001 : "kDexTypeCodeItem",
    0x2002 : "kDexTypeStringDataItem",
    0x2003 : "kDexTypeDebugInfoItem",
    0x2004 : "kDexTypeAnnotationItem",
    0x2005 : "kDexTypeEncodedArrayItem",
    0x2006 : "kDexTypeAnnotationsDirectoryItem",
}


class DexFile(object):
    """docstring for DexFile"""
    def __init__(self, filepath):
        super(DexFile, self).__init__()
        self.filepath = filepath
        # Dex文件头部
        self.DexHeader = DexHeader()
        # 字符串索引区
        self.DexStringIdList = []
        # 类型索引区
        self.DexTypeIdList = []
        # 字段索引区
        self.DexFieldIdList = []
        # 原型索引区
        self.DexProtoIdList = []
        # 方法索引区
        self.DexMethodIdList = []
        # 类定义区
        self.dexClassDefList = []

        self.init_header(self.filepath) # 初始化dex header
        self.init_DexStringId() # 初始化 DexStringId index table
        self.init_DexTypeId() # 初始化DexTypeId index table
        self.init_DexProtoId() # 初始化DexProtoId index table
        self.int_DexFieldId() # 初始化DexFieldId index table
        self.init_DexMethodId() # 初始化DexMethodId index table
        self.init_DexClassDef() # 初始化DexClassDef类定义区


    def init_header(self, filepath):
        f = open(filepath, "rb")
        self.DexHeader.f = f

        f.seek(0x0, 0)
        self.DexHeader.magic = binascii.b2a_hex(f.read(8))

        f.seek(0x8, 0)
        self.DexHeader.checksum = binascii.b2a_hex(f.read(4)).decode('hex')[::-1].encode('hex')

        f.seek(0xc, 0)
        self.DexHeader.signature = binascii.b2a_hex(f.read(20))

        f.seek(0x20, 0)
        self.DexHeader.file_size = binascii.b2a_hex(f.read(4)).decode('hex')[::-1].encode('hex')

        f.seek(0x24, 0)
        self.DexHeader.header_size = binascii.b2a_hex(f.read(4)).decode('hex')[::-1].encode('hex')

        f.seek(0x28, 0)
        self.DexHeader.endian_tag = binascii.b2a_hex(f.read(4)).decode('hex')[::-1].encode('hex')

        f.seek(0x2c, 0)
        self.DexHeader.link_size = binascii.b2a_hex(f.read(4)).decode('hex')[::-1].encode('hex')

        f.seek(0x30, 0)
        self.DexHeader.link_off = binascii.b2a_hex(f.read(4)).decode('hex')[::-1].encode('hex')

        f.seek(0x34, 0)
        self.DexHeader.map_off = binascii.b2a_hex(f.read(4)).decode('hex')[::-1].encode('hex')

        f.seek(0x38, 0)
        self.DexHeader.string_ids_size = binascii.b2a_hex(f.read(4)).decode('hex')[::-1].encode('hex')

        f.seek(0x3c, 0)
        self.DexHeader.string_ids_off = binascii.b2a_hex(f.read(4)).decode('hex')[::-1].encode('hex')

        f.seek(0x40, 0)
        self.DexHeader.type_ids_size = binascii.b2a_hex(f.read(4)).decode('hex')[::-1].encode('hex')

        f.seek(0x44, 0)
        self.DexHeader.type_ids_off = binascii.b2a_hex(f.read(4)).decode('hex')[::-1].encode('hex')

        f.seek(0x48, 0)
        self.DexHeader.proto_ids_size = binascii.b2a_hex(f.read(4)).decode('hex')[::-1].encode('hex')

        f.seek(0x4c, 0)
        self.DexHeader.proto_ids_off = binascii.b2a_hex(f.read(4)).decode('hex')[::-1].encode('hex')

        f.seek(0x50, 0)
        self.DexHeader.field_ids_size = binascii.b2a_hex(f.read(4)).decode('hex')[::-1].encode('hex')

        f.seek(0x54, 0)
        self.DexHeader.field_ids_off = binascii.b2a_hex(f.read(4)).decode('hex')[::-1].encode('hex')

        f.seek(0x58, 0)
        self.DexHeader.method_ids_size = binascii.b2a_hex(f.read(4)).decode('hex')[::-1].encode('hex')

        f.seek(0x5c, 0)
        self.DexHeader.method_ids_off = binascii.b2a_hex(f.read(4)).decode('hex')[::-1].encode('hex')

        f.seek(0x60, 0)
        self.DexHeader.class_defs_size = binascii.b2a_hex(f.read(4)).decode('hex')[::-1].encode('hex')

        f.seek(0x64, 0)
        self.DexHeader.class_defs_off = binascii.b2a_hex(f.read(4)).decode('hex')[::-1].encode('hex')

        f.seek(0x68, 0)
        self.DexHeader.data_size = binascii.b2a_hex(f.read(4)).decode('hex')[::-1].encode('hex')

        f.seek(0x6c, 0)
        self.DexHeader.data_off = binascii.b2a_hex(f.read(4)).decode('hex')[::-1].encode('hex')

    def print_header(self):
        print '[+] magic:\t0x' + self.DexHeader.magic
        print '[+] checksum:\t0x' + self.DexHeader.checksum
        print '[+] signature:\t' + self.DexHeader.signature
        print '[+] file_size:\t0x' + self.DexHeader.file_size
        print '[+] header_size:\t0x' + self.DexHeader.header_size
        print '[+] endian_tag:\t0x' + self.DexHeader.endian_tag
        print '[+] link_size:\t0x' + self.DexHeader.link_size
        print '[+] link_off:\t0x' + self.DexHeader.link_off
        print '[+] map_off:\t0x' + self.DexHeader.map_off
        print '[+] string_ids_size:\t0x' + self.DexHeader.string_ids_size
        print '[+] string_ids_off:\t0x' + self.DexHeader.string_ids_off
        print '[+] type_ids_size:\t0x' + self.DexHeader.type_ids_size
        print '[+] type_ids_off:\t0x' + self.DexHeader.type_ids_off
        print '[+] proto_ids_size:\t0x' + self.DexHeader.proto_ids_size
        print '[+] proto_ids_off:\t0x' + self.DexHeader.proto_ids_off
        print '[+] field_ids_size:\t0x' + self.DexHeader.field_ids_size
        print '[+] field_ids_off:\t0x' + self.DexHeader.field_ids_off
        print '[+] method_ids_size:\t0x' + self.DexHeader.method_ids_size
        print '[+] method_ids_off:\t0x' + self.DexHeader.method_ids_off
        print '[+] class_defs_size:\t0x' + self.DexHeader.class_defs_size
        print '[+] class_defs_off:\t0x' + self.DexHeader.class_defs_off
        print '[+] data_size:\t0x' + self.DexHeader.data_size
        print '[+] data_off:\t0x' + self.DexHeader.data_off

    def print_DexMapList(self):
        """
        typedef struct DexMapList {
            u4  size;               /* #of entries in list */
            DexMapItem list[1];     /* entries */
        } DexMapList;
        """
        map_off_int = int(self.DexHeader.map_off, 16)

        #u4 size
        self.DexHeader.f.seek(map_off_int, 0)
        size_hex = binascii.b2a_hex(self.DexHeader.f.read(4)).decode('hex')[::-1].encode('hex')
        size = int(size_hex, 16)

        for index in range(size):
            # DexMapItem list[]
            self.print_DexMapItem(map_off_int+4, index)

    def print_DexMapItem(self, map_off, index):
        """
        typedef struct DexMapItem {
            u2  type;              /* type code (see kDexType* above) */
            u2  unused;
            u4  size;              /* count of items of the indicated type */
            u4  offset;            /* file offset to the start of data */
        } DexMapItem;
        """
        #u2 type
        self.DexHeader.f.seek(map_off + index*12, 0)
        dexType = binascii.b2a_hex(self.DexHeader.f.read(2)).decode('hex')[::-1].encode('hex')

        #u2 unused
        self.DexHeader.f.seek(map_off + index*12 + 2, 0)
        unused = binascii.b2a_hex(self.DexHeader.f.read(2)).decode('hex')[::-1].encode('hex')

        #u4 size
        self.DexHeader.f.seek(map_off + index*12 + 4, 0)
        size = binascii.b2a_hex(self.DexHeader.f.read(4)).decode('hex')[::-1].encode('hex')

        #u4 offset
        self.DexHeader.f.seek(map_off + index*12 + 8, 0)
        offset = binascii.b2a_hex(self.DexHeader.f.read(4)).decode('hex')[::-1].encode('hex')

        print '\n'
        print '[+] #%d DexMapItem:\t' % index
        print '    u2 dexType\t%s #%s' % (dexType, MAP_ITEM_TYPE_CODES[int(dexType, 16)])
        print '    u2 unused\t' + unused
        print '    u4 size\t' + size
        print '    u4 offset\t' + offset

    def init_DexStringId(self):
        """
        typedef struct DexStringId {
            u4  stringDataOff;      /* file offset to string_data_item */
        } DexStringId;
        """
        string_ids_off_int = int(self.DexHeader.string_ids_off, 16)
        string_ids_size_int = int(self.DexHeader.string_ids_size, 16)

        for index in range(string_ids_size_int):
            # string offset
            self.DexHeader.f.seek(string_ids_off_int + index*4, 0)
            try:
                string_data_off = int(binascii.b2a_hex(self.DexHeader.f.read(4)).decode('hex')[::-1].encode('hex'), 16)
            except:
                print binascii.b2a_hex(self.DexHeader.f.read(4)).decode('hex')[::-1].encode('hex')
            self.DexHeader.f.seek(string_data_off, 0)

            # length of str
            self.DexHeader.f.read(1)

            length = 0
            try:
                while int(binascii.b2a_hex(self.DexHeader.f.read(1)).decode('hex')[::-1].encode('hex'),16) != 0:
                    length += 1
            except:
                print binascii.b2a_hex(self.DexHeader.f.read(1)).decode('hex')[::-1].encode('hex')
            self.DexHeader.f.seek(string_data_off + 1,0)
            dex_str = self.DexHeader.f.read(length)
            self.DexHeader.f.read(1) # remove \x00
            string_data_off += (length + 2) # + \0 + size bit

            # self.DexStringIdList.append(dex_str.decode('utf-8'))
            self.DexStringIdList.append(dex_str)

    def print_DexStringId(self):

        print '\n'
        print '[+] DexStringId:'
        for index in range(len(self.DexStringIdList)):
            print '    #%s %s' % (hex(index), self.DexStringIdList[index])

    def init_DexTypeId(self):
        type_ids_off_int = int(self.DexHeader.type_ids_off, 16)
        type_ids_size_int = int(self.DexHeader.type_ids_size, 16)

        self.DexHeader.f.seek(type_ids_off_int, 0)

        for index in range(type_ids_size_int):
            descriptorIdx_hex = binascii.b2a_hex(self.DexHeader.f.read(4)).decode('hex')[::-1].encode('hex')
            descriptorIdx_int = int(descriptorIdx_hex, 16)

            self.DexTypeIdList.append(descriptorIdx_int)

    def print_DexTypeId(self):
        print '\n'
        print '[+] DexTypeId:'
        for index in range(len(self.DexTypeIdList)):
            print '    #%s #%s' % (hex(index), self.getDexTypeId(index))

    def init_DexProtoId(self):
        proto_ids_size_int = int(self.DexHeader.proto_ids_size, 16)
        proto_ids_off_int = int(self.DexHeader.proto_ids_off, 16)

        for index in range(proto_ids_size_int):
            self.DexHeader.f.seek(proto_ids_off_int+index*12, 0)
            dexProtoIdObj = DexProtoId()
            # u4 shortyIdx
            shortyIdx_hex = binascii.b2a_hex(self.DexHeader.f.read(4)).decode('hex')[::-1].encode('hex')
            shortyIdx = int(shortyIdx_hex, 16)
            # u4 returnTypeIdx
            returnTypeIdx_hex = binascii.b2a_hex(self.DexHeader.f.read(4)).decode('hex')[::-1].encode('hex')
            returnTypeIdx = int(returnTypeIdx_hex, 16)
            # u4 parametersOff
            parametersOff_hex = binascii.b2a_hex(self.DexHeader.f.read(4)).decode('hex')[::-1].encode('hex')
            parametersOff = int(parametersOff_hex, 16)

            dexProtoIdObj.shortyIdx = shortyIdx
            dexProtoIdObj.returnTypeIdx = returnTypeIdx
            dexProtoIdObj.parameterOff = parametersOff
            dexProtoIdObj.offset = proto_ids_off_int + index * 12
            dexProtoIdObj.length = 12

            if parametersOff == 0:
                dexProtoIdObj.dexTypeList = None
                self.DexProtoIdList.append(dexProtoIdObj)

                continue
            self.DexHeader.f.seek(parametersOff, 0)

            parameter_str = ""
            # Struct DexTypeList
            # u4 size
            dexTypeItemSize_hex = binascii.b2a_hex(self.DexHeader.f.read(4)).decode('hex')[::-1].encode('hex')
            dexTypeItemSize = int(dexTypeItemSize_hex, 16)

            dexTypeListObj = DexTypeList()
            dexTypeListObj.size = dexTypeItemSize

            # DexTypeItem list[]
            for i in range(dexTypeItemSize):
                # Struct DexTypeItem
                # u2 typeIdx
                typeIdx_hex = binascii.b2a_hex(self.DexHeader.f.read(2)).decode('hex')[::-1].encode('hex')
                typeIdx = int(typeIdx_hex, 16)
                dexTypeListObj.list.append(typeIdx)

            dexProtoIdObj.dexTypeList = dexTypeListObj
            self.DexProtoIdList.append(dexProtoIdObj)

    def getDexStringId(self, shortyIdx):
        return self.DexStringIdList[shortyIdx]

    def getDexTypeId(self, returnTypeIdx):
        return self.DexStringIdList[self.DexTypeIdList[returnTypeIdx]]

    def print_DexProtoId(self):
        proto_ids_off_int = int(self.DexHeader.proto_ids_off, 16)
        self.DexHeader.f.seek(proto_ids_off_int, 0)
        print '\n'
        print '[+] DexProtoId:'
        for index in range(len(self.DexProtoIdList)):
            dexProtoidObj = self.DexProtoIdList[index]

            shortyIdxStr = self.getDexStringId(dexProtoidObj.shortyIdx)
            returnTypeIdxStr = self.getDexStringId(dexProtoidObj.returnTypeIdx)

            print '    #%s (%s~%s)' % (hex(index), hex(dexProtoidObj.offset), hex(dexProtoidObj.offset + dexProtoidObj.length))
            print '    DexProtoId[%d]->shortyIdx= %s\t#%s' % (index,hex(dexProtoidObj.shortyIdx), shortyIdxStr)
            print '    DexProtoId[%d]->returnTypeIdx= %s\t#%s' % (index, hex(dexProtoidObj.returnTypeIdx), returnTypeIdxStr)
            print '    DexProtoId[%d]->parametersOff= %s' % (index, hex(dexProtoidObj.parameterOff))
            if dexProtoidObj.dexTypeList:
                print '      DexTypeList->size= %s' % hex(dexProtoidObj.dexTypeList.size)
                for k in range(dexProtoidObj.dexTypeList.size):
                    print '      DexTypeList->list[%d]= %s\t#%s' % (k, hex(dexProtoidObj.dexTypeList.list[k]), self.getDexTypeId(dexProtoidObj.dexTypeList.list[k]))
            print ''

    def int_DexFieldId(self):
        field_ids_off = int(self.DexHeader.field_ids_off, 16)
        field_ids_size = int(self.DexHeader.field_ids_size, 16)

        self.DexHeader.f.seek(field_ids_off, 0)

        for index in range(field_ids_size):
            # DexFieldId
            dexFieldIdObj = DexFieldId()
            # u2 classIdx
            classIdx_hex = binascii.b2a_hex(self.DexHeader.f.read(2)).decode('hex')[::-1].encode('hex')
            classIdx = int(classIdx_hex, 16)
            # u2 typeIdx
            typeIdx_hex = binascii.b2a_hex(self.DexHeader.f.read(2)).decode('hex')[::-1].encode('hex')
            typeIdx = int(typeIdx_hex, 16)
            # u4 nameIdx
            nameIdx_hex = binascii.b2a_hex(self.DexHeader.f.read(4)).decode('hex')[::-1].encode('hex')
            nameIdx = int(nameIdx_hex, 16)

            dexFieldIdObj.classIdx = classIdx
            dexFieldIdObj.typeIdx = typeIdx
            dexFieldIdObj.nameIdx = nameIdx
            dexFieldIdObj.offset = field_ids_off + index * 8
            dexFieldIdObj.length = 8

            self.DexFieldIdList.append(dexFieldIdObj)

    def print_DexFieldId(self):
        print '[+] DexFieldId:'
        for index in range(len(self.DexFieldIdList)):
            self.DexHeader.f.seek(self.DexFieldIdList[index].offset, 0)
            # DexFieldId
            # u2 classIdx
            classIdx = self.DexFieldIdList[index].classIdx
            # u2 typeIdx
            typeIdx = self.DexFieldIdList[index].typeIdx
            # u4 nameIdx
            nameIdx = self.DexFieldIdList[index].nameIdx

            print '    #%s (%s~%s)' % (hex(index), hex(self.DexFieldIdList[index].offset), hex(self.DexFieldIdList[index].offset + self.DexFieldIdList[index].length))
            print '    DexFieldId[%d]->classIdx=%s\t#%s' % (index, hex(classIdx), self.getDexStringId(classIdx))
            print '    DexFieldId[%d]->typeIdx=%s\t#%s' % (index, hex(typeIdx), self.getDexStringId(typeIdx))
            print '    DexFieldId[%d]->nameIdx=%s\t#%s' % (index, hex(nameIdx), self.getDexStringId(nameIdx))
            print ''

    def init_DexMethodId(self):
        method_ids_off = int(self.DexHeader.method_ids_off, 16)
        method_ids_size = int(self.DexHeader.method_ids_size, 16)

        self.DexHeader.f.seek(method_ids_off, 0)

        for index in range(method_ids_size):
            # DexMethodId
            dexMethodIdObj = DexMethodId()
            # u2 classIdx
            classIdx_hex = binascii.b2a_hex(self.DexHeader.f.read(2)).decode('hex')[::-1].encode('hex')
            classIdx = int(classIdx_hex, 16)
            # u2 protoIdx
            protoIdx_hex = binascii.b2a_hex(self.DexHeader.f.read(2)).decode('hex')[::-1].encode('hex')
            protoIdx = int(protoIdx_hex, 16)
            # u4 nameIdx
            nameIdx_hex = binascii.b2a_hex(self.DexHeader.f.read(4)).decode('hex')[::-1].encode('hex')
            nameIdx = int(nameIdx_hex, 16)

            dexMethodIdObj.classIdx = classIdx
            dexMethodIdObj.protoIdx = protoIdx
            dexMethodIdObj.nameIdx = nameIdx
            dexMethodIdObj.offset = method_ids_off + index * 8
            dexMethodIdObj.length = 8

            self.DexMethodIdList.append(dexMethodIdObj)

    def print_DexMethodId(self):
        print '\n'
        print '[+] DexMethodId:'
        for index in range(len(self.DexMethodIdList)):
            # DexMethodId
            # u2 classIdx
            classIdx = self.DexMethodIdList[index].classIdx
            # u2 protoIdx
            protoIdx = self.DexMethodIdList[index].protoIdx
            # u4 nameIdx
            nameIdx = self.DexMethodIdList[index].nameIdx

            print '    #%s (%s~%s)' % (hex(index), hex(self.DexMethodIdList[index].offset), hex(self.DexMethodIdList[index].offset + self.DexMethodIdList[index].length))
            print '    DexMethodId[%d]->classIdx=%s\t#%s' % (index, hex(classIdx), self.getDexTypeId(classIdx))
            print '    DexMethodId[%d]->protoIdx=%s\t#%s' % (index, hex(protoIdx), self.DexProtoIdList[protoIdx].toString(self))
            print '    DexMethodId[%d]->nameIdx =%s\t#%s' % (index, hex(nameIdx), self.DexStringIdList[nameIdx])
            print ''

    def init_DexClassDef(self):
        class_defs_size_int = int(self.DexHeader.class_defs_size, 16)
        class_defs_off_int = int(self.DexHeader.class_defs_off, 16)

        for index in range(class_defs_size_int):
            dexClassDefObj = DexClassDef()
            self.dexClassDefList.append(dexClassDefObj)

            #u4 classIdx
            self.DexHeader.f.seek(class_defs_off_int + index*32, 0)
            classIdx_hex = binascii.b2a_hex(self.DexHeader.f.read(4)).decode('hex')[::-1].encode('hex')
            classIdx = int(classIdx_hex, 16)

            #u4 accessFlags
            self.DexHeader.f.seek(class_defs_off_int + index*32 + 4, 0)
            accessFlags_hex = binascii.b2a_hex(self.DexHeader.f.read(4)).decode('hex')[::-1].encode('hex')
            accessFlags = int(accessFlags_hex, 16)

            #u4 superclassIdx
            self.DexHeader.f.seek(class_defs_off_int + index*32 + 8, 0)
            superclassIdx_hex = binascii.b2a_hex(self.DexHeader.f.read(4)).decode('hex')[::-1].encode('hex')
            superclassIdx = int(superclassIdx_hex, 16)

            #u4 interfaceOff
            self.DexHeader.f.seek(class_defs_off_int + index*32 + 12, 0)
            interfaceOff_hex = binascii.b2a_hex(self.DexHeader.f.read(4)).decode('hex')[::-1].encode('hex')
            interfaceOff = int(interfaceOff_hex, 16)

            #u4 sourceFieldIdx
            self.DexHeader.f.seek(class_defs_off_int + index*32 + 16, 0)
            sourceFieldIdx_hex = binascii.b2a_hex(self.DexHeader.f.read(4)).decode('hex')[::-1].encode('hex')
            sourceFieldIdx = int(sourceFieldIdx_hex, 16)

            #u4 annotationsOff
            self.DexHeader.f.seek(class_defs_off_int + index*32 + 20, 0)
            annotationsOff_hex = binascii.b2a_hex(self.DexHeader.f.read(4)).decode('hex')[::-1].encode('hex')
            annotationsOff = int(annotationsOff_hex, 16)

            #u4 classDataOff
            self.DexHeader.f.seek(class_defs_off_int + index*32 + 24, 0)
            classDataOff_hex = binascii.b2a_hex(self.DexHeader.f.read(4)).decode('hex')[::-1].encode('hex')
            classDataOff = int(classDataOff_hex, 16)

            #u4 staticValueOff
            self.DexHeader.f.seek(class_defs_off_int + index * 32 + 28, 0)
            staticValueOff_hex = binascii.b2a_hex(self.DexHeader.f.read(4)).decode('hex')[::-1].encode('hex')
            staticValueOff = int(staticValueOff_hex, 16)

            dexClassDefObj.classIdx = classIdx
            dexClassDefObj.accessFlags = accessFlags
            dexClassDefObj.superclassIdx = superclassIdx
            dexClassDefObj.interfaceOff = interfaceOff
            dexClassDefObj.sourceFieldIdx = sourceFieldIdx
            dexClassDefObj.annotationsOff = annotationsOff
            dexClassDefObj.classDataOff = classDataOff
            dexClassDefObj.staticValueOff = staticValueOff
            dexClassDefObj.offset = class_defs_off_int + index * 32
            dexClassDefObj.length = 32

            if classDataOff == 0:
                continue

            # 获取DexClassData结构
            ######################################################
            dexClassDataHeaderOffset = classDataOff
            dexClassDataHeaderLength = 0

            # 解析DexClassData结构体中header成员
            self.DexHeader.f.seek(classDataOff, 0)
            dexClassDataHeader = []
            for i in range(4):
                cur_bytes_hex = binascii.b2a_hex(self.DexHeader.f.read(1))
                dexClassDataHeaderLength += 1
                cur_bytes = int(cur_bytes_hex, 16)
                value = cur_bytes_hex

                while cur_bytes > 0x7f:
                    cur_bytes_hex = binascii.b2a_hex(self.DexHeader.f.read(1))
                    dexClassDataHeaderLength += 1
                    value += cur_bytes_hex
                    cur_bytes = int(cur_bytes_hex, 16)
                dexClassDataHeader.append(value)
            staticFieldsSize = self.readUnsignedLeb128(dexClassDataHeader[0])
            instanceFieldsSize = self.readUnsignedLeb128(dexClassDataHeader[1])
            directMethodsSize = self.readUnsignedLeb128(dexClassDataHeader[2])
            virtualMethodsSize = self.readUnsignedLeb128(dexClassDataHeader[3])

            dexClassDataHeader = DexClassDataHeader()
            dexClassDataHeader.staticFieldsSize = staticFieldsSize
            dexClassDataHeader.instanceFieldsSize = instanceFieldsSize
            dexClassDataHeader.directMethodsSize = directMethodsSize
            dexClassDataHeader.virtualMethodsSize = virtualMethodsSize
            dexClassDataHeader.offset = classDataOff
            dexClassDataHeader.length = dexClassDataHeaderLength

            dexClassDefObj.header = dexClassDataHeader

            # 解析DexClassData结构体中staticFields、instanceFields、directMethods和virtualMethods成员
            offset = dexClassDataHeader.offset + dexClassDataHeader.length
            # (1)解析DexField* staticFields成员
            """
            struct DexField{
                u4 fieldIdx;
                u4 accessFlags;
            }
            """
            for i in range(staticFieldsSize):
                array = []
                length = 0
                for j in range(2):
                    cur_bytes_hex = binascii.b2a_hex(self.DexHeader.f.read(1))
                    length += 1

                    cur_bytes = int(cur_bytes_hex, 16)
                    value = cur_bytes_hex

                    while cur_bytes > 0x7f:
                        cur_bytes_hex = binascii.b2a_hex(self.DexHeader.f.read(1))
                        length += 1

                        cur_bytes = int(cur_bytes_hex, 16)
                        value += cur_bytes_hex

                    array.append(value)

                dexField = DexField()
                dexField.fieldIdx = self.readUnsignedLeb128(array[0])
                dexField.accessFlags = self.readUnsignedLeb128(array[1])
                dexField.offset = offset
                dexField.length = length

                offset += length

                dexClassDefObj.staticFields.append(dexField)

            # (2)解析DexField* instanceFields成员
            for i in range(instanceFieldsSize):
                array = []
                length = 0
                for j in range(2):
                    cur_bytes_hex = binascii.b2a_hex(self.DexHeader.f.read(1))
                    length += 1

                    cur_bytes = int(cur_bytes_hex, 16)
                    value = cur_bytes_hex

                    while cur_bytes > 0x7f:
                        cur_bytes_hex = binascii.b2a_hex(self.DexHeader.f.read(1))
                        length += 1

                        cur_bytes = int(cur_bytes_hex, 16)
                        value += cur_bytes_hex

                    array.append(value)

                dexField = DexField()
                dexField.fieldIdx = self.readUnsignedLeb128(array[0])
                dexField.accessFlags = self.readUnsignedLeb128(array[1])
                dexField.offset = offset
                dexField.length = length

                offset += length

                dexClassDefObj.instanceFields.append(dexField)

            # (3)解析DexMethod* directMethods成员
            for i in range(directMethodsSize):
                array = []
                length = 0
                for j in range(3):
                    cur_bytes_hex = binascii.b2a_hex(self.DexHeader.f.read(1))
                    length += 1

                    cur_bytes = int(cur_bytes_hex, 16)
                    value = cur_bytes_hex

                    while cur_bytes > 0x7f:
                        cur_bytes_hex = binascii.b2a_hex(self.DexHeader.f.read(1))
                        length += 1

                        cur_bytes = int(cur_bytes_hex, 16)
                        value += cur_bytes_hex

                    array.append(value)

                dexMethod = DexMethod()
                dexMethod.methodIdx = self.readUnsignedLeb128(array[0])
                dexMethod.accessFlags = self.readUnsignedLeb128(array[1])
                dexMethod.codeOff = self.readUnsignedLeb128(array[2])
                dexMethod.offset = offset
                dexMethod.length = length

                offset += length

                dexClassDefObj.directMethods.append(dexMethod)

            # (4)解析DexMethod* virtualMethods成员
            for i in range(virtualMethodsSize):
                array = []
                length = 0
                for j in range(3):
                    cur_bytes_hex = binascii.b2a_hex(self.DexHeader.f.read(1))
                    length += 1

                    cur_bytes = int(cur_bytes_hex, 16)
                    value = cur_bytes_hex

                    while cur_bytes > 0x7f:
                        cur_bytes_hex = binascii.b2a_hex(self.DexHeader.f.read(1))
                        length += 1

                        cur_bytes = int(cur_bytes_hex, 16)
                        value += cur_bytes_hex

                    array.append(value)

                dexMethod = DexMethod()
                dexMethod.methodIdx = self.readUnsignedLeb128(array[0])
                dexMethod.accessFlags = self.readUnsignedLeb128(array[1])
                dexMethod.codeOff = self.readUnsignedLeb128(array[2])
                dexMethod.offset = offset
                dexMethod.length = length

                offset += length

                dexClassDefObj.virtualMethods.append(dexMethod)
            ######################################################

            # 解析DexCode
            for dexMethod in dexClassDefObj.directMethods:
                # 跳转到指向DexCode的偏移处
                if dexMethod.codeOff != 0x0:
                    dexCode = self.parseDexCode(dexMethod.codeOff)
                    dexMethod.dexCode = dexCode
                else:
                    dexMethod.dexCode = None

            for dexMethod in dexClassDefObj.virtualMethods:
                # 跳转到指向DexCode的偏移处
                if dexMethod.codeOff != 0x0:
                    dexCode = self.parseDexCode(dexMethod.codeOff)
                    dexMethod.dexCode = dexCode
                else:
                    dexMethod.dexCode = None

    def print_DexClassDef(self):
        print '\n'
        print '[+] DexClassDef:'

        for index in range(len(self.dexClassDefList)):
            dexClassDefObj = self.dexClassDefList[index]
            print '    #%s~%s' % (hex(dexClassDefObj.offset), hex(dexClassDefObj.offset + dexClassDefObj.length))
            print '    DexClassDef[%d]:\t' % index
            print '    DexClassDef[%d]->classIdx\t= %s\t#%s' % (index, hex(dexClassDefObj.classIdx), self.getDexTypeId(dexClassDefObj.classIdx))
            print '    DexClassDef[%d]->accessFlags\t= %s' % (index, hex(dexClassDefObj.accessFlags) )
            print '    DexClassDef[%d]->superclassIdx\t= %s\t#%s' % (index, hex(dexClassDefObj.superclassIdx), self.getDexTypeId(dexClassDefObj.superclassIdx))
            print '    DexClassDef[%d]->interfaceOff\t= %s' % (index, hex(dexClassDefObj.interfaceOff))
            if dexClassDefObj.sourceFieldIdx == 0xffffffff:
                print '    DexClassDef[%d]->sourceFieldIdx\t= %s\t#UNKNOWN' % (index, hex(dexClassDefObj.sourceFieldIdx))
            else:
                print '    DexClassDef[%d]->sourceFieldIdx\t= %s\t#%s' % (index, hex(dexClassDefObj.sourceFieldIdx), self.DexStringIdList[dexClassDefObj.sourceFieldIdx])
            print '    DexClassDef[%d]->annotationsOff\t= %s' % (index, hex(dexClassDefObj.annotationsOff))
            print '    DexClassDef[%d]->classDataOff\t= %s' % (index, hex(dexClassDefObj.classDataOff))
            print '    DexClassDef[%d]->staticValueOff\t= %s' % (index, hex(dexClassDefObj.staticValueOff))
            if dexClassDefObj.classDataOff == 0:
                continue
            print '    ------------------------------------------------------------------------'
            print '    # %s~%s' % (hex(dexClassDefObj.header.offset), hex(dexClassDefObj.header.offset + dexClassDefObj.header.length))
            print '    DexClassDef[%d]->DexClassData->DexClassDataHeader->staticFieldsSize \t= %s' % (index, hex(dexClassDefObj.header.staticFieldsSize))
            print '    DexClassDef[%d]->DexClassData->DexClassDataHeader->instanceFieldsSize \t= %s' % (index, hex(dexClassDefObj.header.instanceFieldsSize))
            print '    DexClassDef[%d]->DexClassData->DexClassDataHeader->directMethodsSize \t= %s' % (index, hex(dexClassDefObj.header.directMethodsSize))
            print '    DexClassDef[%d]->DexClassData->DexClassDataHeader->virtualMethodsSize \t= %s' % (index, hex(dexClassDefObj.header.virtualMethodsSize))
            if len(dexClassDefObj.staticFields) > 0:
                print '    ------------------------------------------------------------------------'
                print '    # %s~%s' % (hex(dexClassDefObj.staticFields[0].offset), hex(dexClassDefObj.staticFields[-1].offset + dexClassDefObj.staticFields[-1].length))
            if len(dexClassDefObj.staticFields) < 0 and len(dexClassDefObj.instanceFields) > 0:
                print '    ------------------------------------------------------------------------'
                print '    # %s~%s' % (hex(dexClassDefObj.instanceFields[0].offset), hex(
                    dexClassDefObj.instanceFields[-1].offset + dexClassDefObj.instanceFields[-1].length))
            lastFieldIdx = 0
            for k in range(len(dexClassDefObj.staticFields)):
                currFieldIdx = lastFieldIdx + dexClassDefObj.staticFields[k].fieldIdx
                fieldName = self.getDexStringId(self.DexFieldIdList[currFieldIdx].nameIdx)
                lastFieldIdx = currFieldIdx
                print '    DexClassDef[%d]->DexClassData->staticFields[%d]\t= %s\t#%s' % (index, k, fieldName, dexClassDefObj.staticFields[k])

            lastFieldIdx = 0
            for k in range(len(dexClassDefObj.instanceFields)):
                currFieldIdx = lastFieldIdx + dexClassDefObj.instanceFields[k].fieldIdx
                fieldName = self.getDexStringId(self.DexFieldIdList[currFieldIdx].nameIdx)
                lastFieldIdx = currFieldIdx
                print '    DexClassDef[%d]->DexClassData->instanceFields[%d]\t= %s\t#%s' % (index, k, fieldName, dexClassDefObj.instanceFields[k])

            if len(dexClassDefObj.staticFields) + len(dexClassDefObj.instanceFields) > 0:
                print '    ------------------------------------------------------------------------'

            lastMethodIdx = 0
            for k in range(len(dexClassDefObj.directMethods)):
                currMethodIdx = lastMethodIdx + dexClassDefObj.directMethods[k].methodIdx
                dexMethodIdObj = self.DexMethodIdList[currMethodIdx]
                lastMethodIdx = currMethodIdx
                print '    # %s~%s' % (hex(dexClassDefObj.directMethods[k].offset), hex(dexClassDefObj.directMethods[k].offset + dexClassDefObj.directMethods[k].length))
                print '    DexClassDef[%d]->DexClassData->directMethods[%d]\t= %s\t#%s' % (index, k, dexMethodIdObj.toString(self), dexClassDefObj.directMethods[k])
                self.dumpDexCode(dexClassDefObj.directMethods[k])
                print '    ------------------------------------------------------------------------'

            lastMethodIdx = 0
            for k in range(len(dexClassDefObj.virtualMethods)):
                currMethodIdx = lastMethodIdx + dexClassDefObj.virtualMethods[k].methodIdx
                dexMethodIdObj = self.DexMethodIdList[currMethodIdx]
                lastMethodIdx = currMethodIdx
                print '    # %s~%s' % (hex(dexClassDefObj.virtualMethods[k].offset), hex(dexClassDefObj.virtualMethods[k].offset + dexClassDefObj.virtualMethods[k].length))
                print '    DexClassDef[%d]->DexClassData->virtualMethods[%d]\t= %s\t#%s' % (index, k, dexMethodIdObj.toString(self), dexClassDefObj.virtualMethods[k])
                self.dumpDexCode(dexClassDefObj.virtualMethods[k])
                print '    ------------------------------------------------------------------------'
            print '\n'

    def dumpDexCode(self, dexMethod):
        if dexMethod.dexCode == None:
            return
        print '    # %s~%s' % (hex(dexMethod.dexCode.offset), hex(dexMethod.dexCode.offset + dexMethod.dexCode.length))
        print '    DexCode=%s' % dexMethod.dexCode
        offset = 0
        insnsSize = dexMethod.dexCode.insnsSize * 4

        while offset < insnsSize:
            opcode = int(dexMethod.dexCode.insns[offset:offset + 2], 16)
            formatIns, _ = getOpCode(opcode)

            decodedInstruction = dexDecodeInstruction(self, dexMethod.dexCode, offset)

            smaliCode = decodedInstruction.smaliCode
            if smaliCode == None:
                continue

            insns = dexMethod.dexCode.insns[decodedInstruction.offset:decodedInstruction.offset + decodedInstruction.length]
            print '    \t%-16s|%04x: %s' % (insns, offset/4, smaliCode)
            offset += len(insns)

            if smaliCode == 'nop':
                break

    def parseDexCode(self, codeOff):
        self.DexHeader.f.seek(codeOff, 0)

        registersSize_hex = binascii.b2a_hex(self.DexHeader.f.read(2)).decode('hex')[::-1].encode('hex')
        registersSize = int(registersSize_hex, 16)

        insSize_hex = binascii.b2a_hex(self.DexHeader.f.read(2)).decode('hex')[::-1].encode('hex')
        insSize = int(insSize_hex, 16)

        outsSize_hex = binascii.b2a_hex(self.DexHeader.f.read(2)).decode('hex')[::-1].encode('hex')
        outsSize = int(outsSize_hex, 16)

        triesSize_hex = binascii.b2a_hex(self.DexHeader.f.read(2)).decode('hex')[::-1].encode('hex')
        triesSize = int(triesSize_hex, 16)

        debugInfoOff_hex = binascii.b2a_hex(self.DexHeader.f.read(4)).decode('hex')[::-1].encode('hex')
        debugInfoOff = int(debugInfoOff_hex, 16)

        insnsSize_hex = binascii.b2a_hex(self.DexHeader.f.read(4)).decode('hex')[::-1].encode('hex')
        insnsSize = int(insnsSize_hex, 16)

        if insnsSize == 0:
            insns = ''
        else:
            if insnsSize*2 > sys.maxint:
                size = insnsSize*2
                insns = ''
                while size > sys.maxint:
                    insns += binascii.b2a_hex(self.DexHeader.f.read(sys.maxint))
                    size -= sys.maxint
            else:
                insns = binascii.b2a_hex(self.DexHeader.f.read(insnsSize*2))

        dexCode = DexCode()
        dexCode.registersSize = registersSize
        dexCode.insSize = insSize
        dexCode.outsSize = outsSize
        dexCode.triesSize = triesSize
        dexCode.debugInfoOff = debugInfoOff
        dexCode.insnsSize = insnsSize
        dexCode.insns = insns

        dexCode.offset = codeOff
        dexCode.length = 16 + len(insns)/2

        return dexCode

    def readUnsignedLeb128(self, hex_value):
        byte_counts = len(hex_value)/2

        #找出第一个不是0的byte位置
        index = 0
        for i in range(byte_counts):
            v1 = int(hex_value[i*2:i*2+2], 16)
            if v1 > 0:
                index = i
                break

        hex_value = hex_value[index*2:]
        byte_counts = len(hex_value)/2

        result = 0
        for i in range(byte_counts):
            cur = int(hex_value[i*2:i*2+2], 16)
            if cur > 0x7f:
                result = result | ((cur & 0x7f) << (7*i))
            else:
                result = result | ((cur & 0x7f) << (7*i))
                break
        return result

class DexHeader(object):
    def __init__(self, ):
        super(DexHeader, self).__init__()
        self.f = None
        self.magic = None
        self.checksum = None
        self.signature = None
        self.file_size = None
        self.header_size = None
        self.endian_tag = None
        self.link_size = None
        self.link_off = None
        self.map_off = None
        self.string_ids_size = None
        self.string_ids_off = None
        self.type_ids_size = None
        self.type_ids_off = None
        self.proto_ids_size = None
        self.proto_ids_off = None
        self.field_ids_size = None
        self.field_ids_off = None
        self.method_ids_size = None
        self.method_ids_off = None
        self.class_defs_size = None
        self.class_defs_off = None
        self.data_size = None
        self.data_off = None


class DexProtoId(object):
    def __init__(self, ):
        super(DexProtoId, self).__init__()
        self.shortyIdx = None
        self.returnTypeIdx = None
        self.parameterOff = None
        self.dexTypeList = None

        # Address index
        self.offset = None
        self.length = 0

    def toString(self, dexFile):
        if self.dexTypeList:
            return '%s%s' % (self.dexTypeList.toString(dexFile),  dexFile.getDexTypeId(self.returnTypeIdx))
        else:
            return '()%s' % dexFile.getDexTypeId(self.returnTypeIdx)

class DexTypeList(object):
    def __init__(self, ):
        super(DexTypeList, self).__init__()
        self.size = None
        self.list = []

    def toString(self, dexFile):
        parametersStr = ''
        if self.size:
            for idx in self.list:
                parametersStr += dexFile.getDexTypeId(idx) + ','
        return '(%s)' % parametersStr

class DexMethodId(object):
    def __init__(self, ):
        super(DexMethodId, self).__init__()
        self.classIdx = None
        self.protoIdx = None
        self.nameIdx = None

        # Address index
        self.offset = None
        self.length = 0

    def toString(self, dexFile):
        if (self.classIdx != None) and (self.protoIdx != None) and (self.nameIdx != None):
            return '%s.%s:%s' % (dexFile.getDexTypeId(self.classIdx),
                                 dexFile.getDexStringId(self.nameIdx),
                                 dexFile.DexProtoIdList[self.protoIdx].toString(dexFile))
        else:
            return None

    def toApi(self, dexFile):
        if (self.classIdx != None) and (self.protoIdx != None) and (self.nameIdx != None):
            return '%s->%s' % (dexFile.getDexTypeId(self.classIdx),
                                 dexFile.getDexStringId(self.nameIdx))
        else:
            return None

class DexFieldId(object):
    def __init__(self, ):
        super(DexFieldId, self).__init__()
        self.classIdx = None
        self.typeIdx = None
        self.nameIdx = None

        # Address index
        self.offset = None
        self.length = 0

    def toString(self, dexFile):
        if (self.classIdx != None) and (self.typeIdx != None) and (self.nameIdx != None):
            return '%s.%s:%s' % (dexFile.getDexTypeId(self.classIdx),
                                 dexFile.getDexStringId(self.nameIdx),
                                 dexFile.getDexTypeId(self.typeIdx))
        else:
            return None

class DexClassDef(object):
    def __init__(self,):
        super(DexClassDef, self).__init__()
        self.classIdx = None
        self.accessFlags = None
        self.superclassIdx = None
        self.interfaceOff = None
        self.sourceFieldIdx = None
        self.annotationsOff = None
        self.classDataOff = None
        self.staticValueOff = None

        self.header = None
        self.staticFields = []
        self.instanceFields = []
        self.directMethods = []
        self.virtualMethods = []

        # Address index
        self.offset = None
        self.length = 0

class DexClassDataHeader(object):
    """docstring for ClassName"""
    def __init__(self):
        super(DexClassDataHeader, self).__init__()
        self.staticFieldsSize = None
        self.instanceFieldsSize = None
        self.directMethodsSize = None
        self.virtualMethodsSize = None

        # Address index
        self.offset = None
        self.length = 0

class DexField(object):
    """docstring for DexField"""
    def __init__(self):
        super(DexField, self).__init__()
        self.fieldIdx = None
        self.accessFlags = None

        # Address index
        self.offset = None
        self.length = 0

    def __str__(self):
        return '[fieldIdx = %s, accessFlags = %s]' % (hex(self.fieldIdx), hex(self.accessFlags))


class DexMethod(object):
    """docstring for DexMethod"""
    def __init__(self):
        super(DexMethod, self).__init__()
        self.methodIdx = None
        self.accessFlags = None
        self.codeOff = None

        # Address index
        self.offset = None
        self.length = 0

        self.dexCode = DexCode()

    def __str__(self):
        return '[methodIdx = %s, accessFlags = %s, codeOff = %s]' % (hex(self.methodIdx), hex(self.accessFlags), hex(self.codeOff))

class DexCode(object):
    """docstring for DexCode"""
    def __init__(self):
        super(DexCode, self).__init__()
        self.registersSize = None
        self.insSize = None
        self.outsSize = None
        self.triesSize = None
        self.debugInfoOff = None
        self.insnsSize = None
        self.insns = None

        # Address index
        self.offset = None
        self.length = 0

    def __str__(self):
        return '[registersSize = %s, insSize = %s, outsSize = %s, triesSize = %s, debugInfoOff = %s, insnsSize = %s, insns = %s]' % \
                (self.registersSize, self.insSize, self.outsSize, self.triesSize, hex(self.debugInfoOff), self.insnsSize, self.insns)


def main():
    dex = DexFile(sys.argv[1])
    dex.print_header()
    dex.print_DexMapList()
    dex.print_DexStringId()
    dex.print_DexTypeId()
    dex.print_DexProtoId()
    dex.print_DexFieldId()
    dex.print_DexMethodId()
    dex.print_DexClassDef()

if __name__ == '__main__':
    main()
