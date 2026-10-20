.intel_syntax noprefix
.text

.globl run_chain
run_chain:
    mov     qword ptr [rip + saved_rsp], rsp
    lea     rsp, [rip + chain]
    ret

.globl g_setup, g_check, g_advance, g_loop, g_exit

g_check:
    movzx   eax, byte ptr [rdi]
    xor     al, cl
    xor     al, byte ptr [rsi]
    or      r8b, al
    ret

g_exit:
    movzx   eax, r8b
    mov     rsp, qword ptr [rip + saved_rsp]
    ret

g_advance:
    add     cl, dl
    inc     rdi
    inc     rsi
    dec     r9
    ret

g_setup:
    pop     rcx
    pop     rdx
    pop     rsi
    pop     r9
    xor     r8d, r8d
    ret

g_loop:
    pop     rax
    pop     r10
    test    r9, r9
    cmovz   rax, r10
    xchg    rax, rsp
    ret

.bss
.align 8
saved_rsp:
    .quad 0

.section .note.GNU-stack, "", @progbits
