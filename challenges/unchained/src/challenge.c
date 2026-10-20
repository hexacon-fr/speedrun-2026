#include <stdio.h>
#include <stdint.h>

#include "flag.h"

int run_chain(const char *input);
void g_setup(void), g_check(void), g_advance(void), g_loop(void), g_exit(void);

#define PTR(x)  ((uint64_t)(x))
#define LOOP  5
#define END   10

uint64_t chain[] = {
    // [0] INIT cl = key, dl = step, rsi = target, r9 = length, r8 = 0
    PTR(g_setup), 0x37, 0x1d, PTR(target), FLAG_LEN,

    // [5] LOOP
    PTR(g_check),   // r8b |= *rdi ^ cl ^ *rsi */
    PTR(g_advance), // cl += dl, next byte */
    PTR(g_loop), PTR(&chain[LOOP]), PTR(&chain[END]),

    /* [10] END */
    PTR(g_exit), // return r8b
};

int main(int argc, char **argv)
{
    if (argc != 2) {
        printf("Usage: %s <flag>\n", argv[0]);
        return 1;
    }

    if (run_chain(argv[1]) == 0) {
        puts("[+] Correct flag!");
        return 0;
    }
    puts("[-] Wrong flag.");
    return 1;
}
