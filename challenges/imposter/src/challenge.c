#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>

#include "flag.h"

static const char EXPECTED[] = "HXN{str1ngs_1s_n0t_r3v3rs1ng_s0rry}";

static int __attribute__((used, noinline))
inspect(const char *candidate, const char *needle) {
    (void)needle;

    if (strlen(candidate) != FLAG_LEN) {
        return 1;
    }

    int delta = 0;
    for (size_t i = 0; i < FLAG_LEN; i++) {
        unsigned char c = (unsigned char)(candidate[i] + 0x11 + 7 * i);
        delta |= c ^ FLAG[i];
    }

    return delta;
}

__attribute__((constructor))
static void rewire(void) {
    void **slot;
    __asm__("leaq strcmp@GOTPCREL(%%rip), %0" : "=r"(slot));

    long page_size = sysconf(_SC_PAGESIZE);
    void *page = (void *)((uintptr_t)slot & ~(uintptr_t)(page_size - 1));

    if (mprotect(page, (size_t)page_size, PROT_READ | PROT_WRITE) != 0) {
        return;
    }

    *slot = (void *)inspect;

    mprotect(page, (size_t)page_size, PROT_READ);
}

int main(int argc, char **argv) {
    char input[128] = {0};

    if (argc > 1) {
        strncpy(input, argv[1], sizeof(input) - 1);
    } else {
        printf("Enter password: ");
        fflush(stdout);
        if (!fgets(input, sizeof(input), stdin)) {
            return 1;
        }
    }

    input[strcspn(input, "\r\n")] = '\0';

    if (strcmp(input, EXPECTED) == 0) {
        puts("[+] Correct flag!");
        return 0;
    }

    puts("[-] Wrong password.");
    return 1;
}
