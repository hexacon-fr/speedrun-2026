A = sys_number
A == getpriority ? check : next
return ALLOW

check:
A = args[0]
pos_0:
A == 0 ? next : pos_1
A = args[1]
A == 0x12 ? next : reject_0
return ERRNO(0)
reject_0:
return ERRNO(1)
pos_1:
A == 1 ? next : pos_2
A = args[1]
A == 0x39 ? next : reject_1
return ERRNO(0)
reject_1:
return ERRNO(1)
pos_2:
A == 2 ? next : pos_3
A = args[1]
A == 0x26 ? next : reject_2
return ERRNO(0)
reject_2:
return ERRNO(1)
pos_3:
A == 3 ? next : pos_4
A = args[1]
A == 0x14 ? next : reject_3
return ERRNO(0)
reject_3:
return ERRNO(1)
pos_4:
A == 4 ? next : pos_5
A = args[1]
A == 0x05 ? next : reject_4
return ERRNO(0)
reject_4:
return ERRNO(1)
pos_5:
A == 5 ? next : pos_6
A = args[1]
A == 0x04 ? next : reject_5
return ERRNO(0)
reject_5:
return ERRNO(1)
pos_6:
A == 6 ? next : pos_7
A = args[1]
A == 0xf7 ? next : reject_6
return ERRNO(0)
reject_6:
return ERRNO(1)
pos_7:
A == 7 ? next : pos_8
A = args[1]
A == 0xe8 ? next : reject_7
return ERRNO(0)
reject_7:
return ERRNO(1)
pos_8:
A == 8 ? next : pos_9
A = args[1]
A == 0xa6 ? next : reject_8
return ERRNO(0)
reject_8:
return ERRNO(1)
pos_9:
A == 9 ? next : pos_10
A = args[1]
A == 0xf5 ? next : reject_9
return ERRNO(0)
reject_9:
return ERRNO(1)
pos_10:
A == 10 ? next : pos_11
A = args[1]
A == 0xcc ? next : reject_10
return ERRNO(0)
reject_10:
return ERRNO(1)
pos_11:
A == 11 ? next : pos_12
A = args[1]
A == 0xf8 ? next : reject_11
return ERRNO(0)
reject_11:
return ERRNO(1)
pos_12:
A == 12 ? next : pos_13
A = args[1]
A == 0x9e ? next : reject_12
return ERRNO(0)
reject_12:
return ERRNO(1)
pos_13:
A == 13 ? next : pos_14
A = args[1]
A == 0xc7 ? next : reject_13
return ERRNO(0)
reject_13:
return ERRNO(1)
pos_14:
A == 14 ? next : pos_15
A = args[1]
A == 0xd5 ? next : reject_14
return ERRNO(0)
reject_14:
return ERRNO(1)
pos_15:
A == 15 ? next : pos_16
A = args[1]
A == 0xf0 ? next : reject_15
return ERRNO(0)
reject_15:
return ERRNO(1)
pos_16:
A == 16 ? next : pos_17
A = args[1]
A == 0xa4 ? next : reject_16
return ERRNO(0)
reject_16:
return ERRNO(1)
pos_17:
A == 17 ? next : pos_18
A = args[1]
A == 0xa5 ? next : reject_17
return ERRNO(0)
reject_17:
return ERRNO(1)
pos_18:
A == 18 ? next : pos_19
A = args[1]
A == 0xeb ? next : reject_18
return ERRNO(0)
reject_18:
return ERRNO(1)
pos_19:
A == 19 ? next : pos_20
A = args[1]
A == 0xbb ? next : reject_19
return ERRNO(0)
reject_19:
return ERRNO(1)
pos_20:
A == 20 ? next : pos_21
A = args[1]
A == 0xb9 ? next : reject_20
return ERRNO(0)
reject_20:
return ERRNO(1)
pos_21:
A == 21 ? next : pos_22
A = args[1]
A == 0x9d ? next : reject_21
return ERRNO(0)
reject_21:
return ERRNO(1)
pos_22:
A == 22 ? next : pos_23
A = args[1]
A == 0x86 ? next : reject_22
return ERRNO(0)
reject_22:
return ERRNO(1)
pos_23:
A == 23 ? next : pos_24
A = args[1]
A == 0xcb ? next : reject_23
return ERRNO(0)
reject_23:
return ERRNO(1)
pos_24:
A == 24 ? next : pos_25
A = args[1]
A == 0x65 ? next : reject_24
return ERRNO(0)
reject_24:
return ERRNO(1)
pos_25:
A == 25 ? next : pos_26
A = args[1]
A == 0x7b ? next : reject_25
return ERRNO(0)
reject_25:
return ERRNO(1)
pos_26:
A == 26 ? next : pos_27
A = args[1]
A == 0x24 ? next : reject_26
return ERRNO(0)
reject_26:
return ERRNO(1)
pos_27:
A == 27 ? next : pos_28
A = args[1]
A == 0x7a ? next : reject_27
return ERRNO(0)
reject_27:
return ERRNO(1)
pos_28:
A == 28 ? next : pos_29
A = args[1]
A == 0x73 ? next : reject_28
return ERRNO(0)
reject_28:
return ERRNO(1)
pos_29:
A == 29 ? next : pos_30
A = args[1]
A == 0x14 ? next : reject_29
return ERRNO(0)
reject_29:
return ERRNO(1)
pos_30:
A == 30 ? next : pos_31
A = args[1]
A == 0x42 ? next : reject_30
return ERRNO(0)
reject_30:
return ERRNO(1)
pos_31:
A == 31 ? next : pos_32
A = args[1]
A == 0x05 ? next : reject_31
return ERRNO(0)
reject_31:
return ERRNO(1)
pos_32:
A == 32 ? next : pos_33
A = args[1]
A == 0x47 ? next : reject_32
return ERRNO(0)
reject_32:
return ERRNO(1)

pos_33:
return ERRNO(1)
