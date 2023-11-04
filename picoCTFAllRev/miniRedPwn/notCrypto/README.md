
# not crypto #

## Overview ##

200 points

Category: [picoMini by redpwn](../)

Tags: `picoMini by redpwn` `Reverse Engineering`

## Description ##

there's crypto in here but the challenge is not crypto... 🤔

Download [not crypto](https://artifacts.picoctf.net/picoMini+by+redpwn/Reverse+Engineering/not-crypto/not-crypto)


## Solution ##

When running the program we are prompted for a 64 characters long input.

```
[danielj@daniel notCrypto]$ ./not-crypto
I heard you wanted to bargain for a flag... whatcha got?
1234567890123456789012345678901234567890123456789012345678901234
Nope, come back later
[danielj@daniel notCrypto]$
```

We can try reversing the program in Ghidra, but it looks incredibly messy
and hard to understand.

```c
bool main(void)
{
  undefined auVar1 [16];
  undefined auVar2 [16];
  undefined auVar3 [16];
  undefined auVar4 [16];
  undefined auVar5 [16];
  undefined auVar6 [16];
  undefined auVar7 [16];
  byte bVar8;
  byte bVar9;
  byte bVar10;
  byte bVar11;
  byte bVar12;
  byte bVar13;
  byte bVar14;
  byte bVar15;
  byte bVar16;
  byte bVar17;
  undefined auVar18 [16];
  int iVar19;
  undefined4 uVar20;
  undefined4 uVar21;
  byte *pbVar22;
  byte bVar23;
  byte bVar24;
  byte bVar25;
  byte bVar26;
  long lVar27;
  byte bVar28;
  byte bVar29;
  byte bVar30;
  ulong uVar31;
  byte bVar32;
  uint uVar33;
  ulong uVar34;
  byte bVar35;
  byte bVar36;
  byte bVar37;
  byte bVar38;
  byte bVar39;
  byte bVar40;
  byte bVar41;
  byte bVar42;
  byte *pbVar43;
  long in_FS_OFFSET;
  byte local_1fe;
  byte local_1fd;
  undefined4 local_1fc;
  undefined4 local_1f8;
  byte local_1f4;
  byte local_1f3;
  byte local_1f2;
  byte local_1f1;
  byte local_1f0;
  byte local_1ef;
  byte local_1ee;
  byte local_1ed;
  byte local_1ec;
  byte *local_1e8;
  undefined input [64];
  undefined local_158 [16];
  byte local_148 [144];
  byte local_b8;
  byte local_b7;
  byte local_b6;
  byte local_b5;
  byte local_b4;
  byte local_b3;
  byte local_b2;
  byte local_b1;
  byte local_b0;
  byte local_af;
  byte local_ae;
  byte local_ad;
  byte local_ac;
  byte local_ab;
  byte local_aa;
  byte local_a9;
  undefined local_a8 [9];
  undefined uStack_9f;
  undefined uStack_9e;
  undefined uStack_9d;
  undefined4 uStack_9c;
  undefined local_98 [16];
  undefined local_88 [16];
  undefined local_78 [16];
  undefined local_68 [16];
  undefined local_58 [16];
  byte local_48 [8];
  long local_40;
  
  local_40 = *(long *)(in_FS_OFFSET + 0x28);
  puts("I heard you wanted to bargain for a flag... whatcha got?");
  bVar37 = 0x98;
  bVar29 = 0x32;
  bVar23 = 0x6c;
  bVar25 = 0x1c;
  local_158 = _DAT_001021a0;
  uVar34 = 4;
  pbVar22 = local_158;
  do {
    if ((uVar34 & 3) == 0) {
      uVar31 = (ulong)bVar29;
      bVar29 = (&DAT_001020a0)[bVar23];
      bVar23 = (&DAT_001020a0)[bVar25];
      bVar25 = (&DAT_001020a0)[bVar37];
      bVar37 = (&DAT_001020a0)[uVar31] ^ (&DAT_00102080)[uVar34 >> 2];
    }
    bVar37 = bVar37 ^ *pbVar22;
    uVar33 = (int)uVar34 + 1;
    uVar34 = (ulong)uVar33;
    bVar29 = bVar29 ^ pbVar22[1];
    bVar23 = bVar23 ^ pbVar22[2];
    bVar25 = bVar25 ^ pbVar22[3];
    pbVar22[0x10] = bVar37;
    pbVar22[0x11] = bVar29;
    pbVar22[0x12] = bVar23;
    pbVar22[0x13] = bVar25;
    pbVar22 = pbVar22 + 4;
  } while (uVar33 != 0x2c);
  _local_a8 = _DAT_001021b0;
  fread(input,1,0x40,_stdin);
  local_88 = _DAT_001021c0;
  local_78 = _DAT_001021d0;
  local_68 = _DAT_001021e0;
  local_58 = _DAT_001021f0;
  iVar19 = 0x10;
  local_1e8 = local_88;
  do {
    auVar18 = _local_a8;
    if (iVar19 == 0x10) {
      uVar20 = vpextrb_avx(_local_a8,4);
      bVar37 = local_a8[8];
      local_1ee = (&DAT_001020a0)[local_158[8] ^ local_a8[8]];
      uVar21 = vpextrb_avx(_local_a8,0xc);
      local_1ef = (&DAT_001020a0)[(byte)((byte)uVar21 ^ local_158[12])];
      uVar21 = vpextrb_avx(_local_a8,1);
      local_1f4 = (&DAT_001020a0)[(byte)((byte)uVar21 ^ local_158[1])];
      uVar21 = vpextrb_avx(_local_a8,5);
      local_1fd = (&DAT_001020a0)[(byte)((byte)uVar21 ^ local_158[5])];
      uVar21 = vpextrb_avx(_local_a8,9);
      local_1fe = (&DAT_001020a0)[(byte)((byte)uVar21 ^ local_158[9])];
      uVar21 = vpextrb_avx(_local_a8,0xd);
      local_1f0 = (&DAT_001020a0)[(byte)((byte)uVar21 ^ local_158[13])];
      uVar21 = vpextrb_avx(_local_a8,2);
      bVar29 = (&DAT_001020a0)[(byte)((byte)uVar21 ^ local_158[2])];
      uVar21 = vpextrb_avx(_local_a8,6);
      local_1ec = (&DAT_001020a0)[(byte)((byte)uVar21 ^ local_158[6])];
      uVar21 = vpextrb_avx(_local_a8,10);
      local_1f1 = (&DAT_001020a0)[(byte)((byte)uVar21 ^ local_158[10])];
      uVar21 = vpextrb_avx(_local_a8,0xe);
      local_1f2 = (&DAT_001020a0)[(byte)((byte)uVar21 ^ local_158[14])];
      uVar21 = vpextrb_avx(_local_a8,3);
      local_1ed = (&DAT_001020a0)[(byte)((byte)uVar21 ^ local_158[3])];
      uVar21 = vpextrb_avx(_local_a8,7);
      bVar23 = (&DAT_001020a0)[(byte)((byte)uVar21 ^ local_158[7])];
      uVar21 = vpextrb_avx(_local_a8,0xb);
      bVar25 = (&DAT_001020a0)[(byte)((byte)uVar21 ^ local_158[11])];
      uVar21 = vpextrb_avx(_local_a8,0xf);
      local_1f3 = (&DAT_001020a0)[(byte)((byte)uVar21 ^ local_158[15])];
      pbVar22 = local_148;
      local_1f8._0_1_ = (&DAT_001020a0)[local_158[0] ^ local_a8[0]];
      local_1fc._0_1_ = (&DAT_001020a0)[(byte)((byte)uVar20 ^ local_158[4])];
      do {
        bVar24 = local_1fd ^ (byte)local_1f8;
        bVar28 = local_1f3 ^ local_1f1;
        bVar39 = bVar24 ^ bVar28;
        bVar42 = local_1f3 ^ (byte)local_1f8;
        bVar32 = local_1fe ^ (byte)local_1fc;
        bVar35 = local_1ed ^ local_1f2;
        bVar36 = bVar32 ^ bVar35;
        bVar40 = local_1ed ^ (byte)local_1fc;
        bVar11 = bVar23 ^ bVar29;
        bVar9 = local_1f0 ^ local_1ee;
        bVar12 = local_1ee ^ bVar23;
        bVar38 = bVar9 ^ bVar11;
        bVar13 = local_1ec ^ bVar25;
        bVar8 = local_1ec ^ local_1f4;
        bVar10 = local_1f4 ^ local_1ef;
        bVar14 = local_1ef ^ bVar25;
        bVar15 = bVar10 ^ bVar13;
        bVar41 = pbVar22[7] ^ bVar36 ^ local_1ed;
        bVar16 = bVar29 ^ bVar38 ^ pbVar22[10];
        bVar30 = pbVar22[0xd] ^ bVar15 ^ local_1f4;
        bVar26 = pbVar22[0xe] ^ bVar15 ^ local_1ec;
        bVar17 = bVar25 ^ pbVar22[0xf] ^ bVar15;
        local_1f8._0_1_ =
             (&DAT_001020a0)
             [(byte)((byte)local_1f8 ^ *pbVar22 ^ bVar39 ^
                    ((char)bVar24 >> 7) * -0x1b ^ bVar24 * '\x02')];
        bVar24 = pbVar22[4] ^ bVar36 ^ (byte)local_1fc;
        local_1ee = (&DAT_001020a0)
                    [(byte)(pbVar22[8] ^ bVar38 ^ local_1ee ^
                           ((char)bVar9 >> 7) * -0x1b ^ bVar9 * '\x02')];
        local_1ef = (&DAT_001020a0)
                    [(byte)(bVar15 ^ pbVar22[0xc] ^ local_1ef ^
                           bVar10 * '\x02' ^ ((char)bVar10 >> 7) * -0x1b)];
        local_1f4 = (&DAT_001020a0)
                    [(byte)(pbVar22[1] ^ bVar39 ^ local_1fd ^
                           ((char)(local_1f1 ^ local_1fd) >> 7) * -0x1b ^
                           (local_1f1 ^ local_1fd) * '\x02')];
        local_1fd = (&DAT_001020a0)
                    [(byte)(pbVar22[5] ^ bVar36 ^ local_1fe ^
                           (local_1f2 ^ local_1fe) * '\x02' ^
                           ((char)(local_1f2 ^ local_1fe) >> 7) * -0x1b)];
        local_1fe = (&DAT_001020a0)
                    [(byte)(local_1f0 ^ bVar38 ^ pbVar22[9] ^
                           (local_1f0 ^ bVar29) * '\x02' ^ ((char)(local_1f0 ^ bVar29) >> 7) * -0x1b
                           )];
        local_1f0 = (&DAT_001020a0)
                    [((uint)(bVar8 >> 7) * 0x1b ^ (uint)bVar8 + (uint)bVar8 ^ (uint)bVar30) & 0xff];
        pbVar43 = pbVar22 + 0x10;
        bVar29 = (&DAT_001020a0)
                 [(byte)(pbVar22[2] ^ bVar39 ^ local_1f1 ^
                        ((char)bVar28 >> 7) * -0x1b ^ bVar28 * '\x02')];
        local_1ec = (&DAT_001020a0)
                    [(byte)(local_1f2 ^ pbVar22[6] ^ bVar36 ^
                           bVar35 * '\x02' ^ ((char)bVar35 >> 7) * -0x1b)];
        local_1f1 = (&DAT_001020a0)
                    [((uint)bVar11 * 2 ^ (uint)(bVar11 >> 7) * 0x1b ^ (uint)bVar16) & 0xff];
        local_1f2 = (&DAT_001020a0)
                    [((uint)bVar13 * 2 ^ (uint)(bVar13 >> 7) * 0x1b ^ (uint)bVar26) & 0xff];
        bVar25 = (&DAT_001020a0)
                 [((uint)(bVar12 >> 7) * 0x1b ^ (uint)bVar12 * 2 ^
                  (uint)(byte)(bVar23 ^ bVar38 ^ pbVar22[0xb])) & 0xff];
        local_1ed = (&DAT_001020a0)
                    [(byte)(pbVar22[3] ^ bVar39 ^ local_1f3 ^
                           bVar42 * '\x02' ^ ((char)bVar42 >> 7) * -0x1b)];
        bVar23 = (&DAT_001020a0)[(byte)(bVar41 ^ ((char)bVar40 >> 7) * -0x1b ^ bVar40 * '\x02')];
        local_1f3 = (&DAT_001020a0)
                    [((uint)(bVar14 >> 7) * 0x1b ^ (uint)bVar14 * 2 ^ (uint)bVar17) & 0xff];
        pbVar22 = pbVar43;
        local_1fc._0_1_ =
             (&DAT_001020a0)[(byte)(bVar24 ^ ((char)bVar32 >> 7) * -0x1b ^ bVar32 * '\x02')];
      } while (&local_b8 != pbVar43);
      local_1f8 = CONCAT31(local_1f8._1_3_,(byte)local_1f8 ^ local_b8);
      auVar1 = vmovd_avx((uint)(bVar29 ^ local_ae));
      local_1fc = CONCAT31(local_1fc._1_3_,local_1f2 ^ local_b2);
      auVar2 = vmovd_avx((uint)(local_1ec ^ local_aa));
      auVar3 = vmovd_avx((uint)(local_1f1 ^ local_b6));
      auVar7 = vpinsrb_avx(auVar1,(uint)(local_ad ^ bVar23),1);
      auVar1 = vmovd_avx((uint)((&DAT_001020a0)
                                [(byte)(bVar24 ^ ((char)bVar32 >> 7) * -0x1b ^ bVar32 * '\x02')] ^
                               local_b4));
      lVar27 = 0xf;
      auVar4 = vmovd_avx((uint)(local_1ee ^ local_b0));
      auVar5 = vmovd_avx(local_1f8);
      auVar6 = vmovd_avx(local_1fc);
      auVar3 = vpinsrb_avx(auVar3,(uint)(local_1f3 ^ local_b5),1);
      auVar5 = vpinsrb_avx(auVar5,(uint)(local_1fd ^ local_b7),1);
      auVar4 = vpinsrb_avx(auVar4,(uint)(local_1f0 ^ local_af),1);
      auVar5 = vpunpcklwd_avx(auVar5,auVar3);
      auVar1 = vpinsrb_avx(auVar1,(uint)(local_1fe ^ local_b3),1);
      auVar3 = vpinsrb_avx(auVar6,(uint)(local_1ed ^ local_b1),1);
      auVar4 = vpunpcklwd_avx(auVar4,auVar7);
      auVar3 = vpunpcklwd_avx(auVar1,auVar3);
      auVar1 = vmovd_avx((uint)(local_1ef ^ local_ac));
      auVar3 = vpunpckldq_avx(auVar5,auVar3);
      auVar1 = vpinsrb_avx(auVar1,(uint)(local_1f4 ^ local_ab),1);
      auVar2 = vpinsrb_avx(auVar2,(uint)(bVar25 ^ local_a9),1);
      auVar1 = vpunpcklwd_avx(auVar1,auVar2);
      auVar1 = vpunpckldq_avx(auVar4,auVar1);
      local_98 = vpunpcklqdq_avx(auVar3,auVar1);
      bVar29 = uStack_9c._3_1_;
      if (uStack_9c._3_1_ == 0xff) {
        bVar29 = uStack_9c._2_1_;
        uStack_9c._3_1_ = 0;
        lVar27 = 0xe;
        if (bVar29 == 0xff) {
          uStack_9c._1_1_ = auVar18[13];
          bVar29 = uStack_9c._1_1_;
          _local_a8 = auVar18._0_14_;
          uStack_9c._2_2_ = 0;
          lVar27 = 0xd;
          if (bVar29 == 0xff) {
            uStack_9c._0_1_ = auVar18[12];
            bVar29 = (byte)uStack_9c;
            _local_a8 = auVar18._0_13_;
            uStack_9c._1_3_ = 0;
            lVar27 = 0xc;
            if (bVar29 == 0xff) {
              uStack_9d = auVar18[11];
              bVar29 = uStack_9d;
              _local_a8 = auVar18._0_12_;
              uStack_9c = 0;
              lVar27 = 0xb;
              if (bVar29 == 0xff) {
                uStack_9e = auVar18[10];
                bVar29 = uStack_9e;
                _local_a8 = auVar18._0_11_;
                _uStack_9d = 0;
                lVar27 = 10;
                if (bVar29 == 0xff) {
                  uStack_9f = auVar18[9];
                  bVar29 = uStack_9f;
                  _local_a8 = auVar18._0_10_;
                  _uStack_9e = 0;
                  lVar27 = 9;
                  if (bVar29 == 0xff) {
                    local_a8 = auVar18._0_9_;
                    _uStack_9f = 0;
                    lVar27 = 8;
                    bVar29 = bVar37;
                    if (bVar37 == 0xff) {
                      local_a8[7] = auVar18[7];
                      bVar29 = local_a8[7];
                      local_a8._0_8_ = auVar18._0_8_;
                      uVar34 = local_a8._0_8_;
                      stack0xffffffffffffff60 = 0;
                      lVar27 = 7;
                      if (bVar29 == 0xff) {
                        local_a8[6] = auVar18[6];
                        bVar29 = local_a8[6];
                        local_a8._0_8_ = uVar34 & 0xffffffffffffff;
                        stack0xffffffffffffff60 = 0;
                        lVar27 = 6;
                        if (bVar29 == 0xff) {
                          bVar29 = local_a8[5];
                          stack0xffffffffffffff60 = 0;
                          local_a8._0_8_ = uVar34 & 0xffffffffffff;
                          lVar27 = 5;
                          if (bVar29 == 0xff) {
                            local_a8[4] = (byte)((uVar34 & 0xffffffffffff) >> 0x20);
                            bVar29 = local_a8[4];
                            stack0xffffffffffffff60 = 0;
                            local_a8._0_8_ = uVar34 & 0xffffffffff;
                            lVar27 = 4;
                            if (bVar29 == 0xff) {
                              local_a8[3] = (byte)((uVar34 & 0xffffffffff) >> 0x18);
                              bVar29 = local_a8[3];
                              stack0xffffffffffffff60 = 0;
                              local_a8._0_8_ = uVar34 & 0xffffffff;
                              lVar27 = 3;
                              if (bVar29 == 0xff) {
                                local_a8[2] = (byte)((uVar34 & 0xffffffff) >> 0x10);
                                bVar29 = local_a8[2];
                                stack0xffffffffffffff60 = 0;
                                local_a8._0_8_ = uVar34 & 0xffffff;
                                lVar27 = 2;
                                if (bVar29 == 0xff) {
                                  local_a8[1] = (byte)((uVar34 & 0xffffff) >> 8);
                                  bVar29 = local_a8[1];
                                  stack0xffffffffffffff60 = 0;
                                  local_a8._0_8_ = uVar34 & 0xffff;
                                  lVar27 = 1;
                                  if (bVar29 == 0xff) {
                                    local_a8[0] = (byte)(uVar34 & 0xffff);
                                    bVar29 = local_a8[0];
                                    stack0xffffffffffffff60 = 0;
                                    local_a8._0_8_ = uVar34 & 0xff;
                                    lVar27 = 0;
                                    if (bVar29 == 0xff) {
                                      _local_a8 = ZEXT716(0) << 8;
                                      iVar19 = 0;
                                      goto LAB_00101385;
                                    }
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
      local_a8[lVar27] = bVar29 + 1;
      iVar19 = 0;
    }
LAB_00101385:
    lVar27 = (long)iVar19;
    iVar19 = iVar19 + 1;
    *local_1e8 = *local_1e8 ^ local_98[lVar27];
    local_1e8 = local_1e8 + 1;
    if (local_48 == local_1e8) {
      iVar19 = memcmp(local_88,input,0x40);
      if (iVar19 != 0) {
        puts("Nope, come back later");
      }
      else {
        puts("Yep, that\'s it!");
      }
      if (local_40 == *(long *)(in_FS_OFFSET + 0x28)) {
        return iVar19 != 0;
      }
                    /* WARNING: Subroutine does not return */
      __stack_chk_fail();
    }
  } while( true );
}
```

However, if we pay attention we can see that `input` is only used twice,
once when reading into it from the player, and another time as a final
check using `memcmp`. Therefore the flag should be the first input to
`memcmp` near the end of the function. We can use a debugger like GDB
and set a breakpoint there.

In gdb an easy way to do this is using the following string of
instructions:

```
start
break memcmp
c
x/s $rdi
```

To get the flag `picoCTF{c0mp1l3r_0pt1m1z4t10n_15_pur3_w1z4rdry_but_n0_pr0bl3m?}`
