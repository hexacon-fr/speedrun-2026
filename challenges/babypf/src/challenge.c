#include <errno.h>
#include <stdio.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>
#include <sys/prctl.h>
#include <sys/syscall.h>
#include <linux/audit.h>
#include <linux/filter.h>
#include <linux/seccomp.h>

#include "filter.h"

#define MASK_BASE 0x5A
#define MASK_STEP 7

static int install_filter(void) {
    struct sock_filter filter_prog[sizeof(bpf) / sizeof(struct sock_filter)];
    memcpy(filter_prog, bpf, sizeof(bpf));

    struct sock_fprog prog = {
        .len = (unsigned short)(sizeof(filter_prog) / sizeof(filter_prog[0])),
        .filter = filter_prog,
    };

    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) != 0) {
        return -1;
    }
    return prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog);
}

static int check_char(int position, char c) {
    long mask = (0x5a + 7 * position) & 0xFF;
    return syscall(SYS_getpriority, position, c ^ mask) == 0;
}

int main(int argc, char **argv) {
    char input[128] = {0};

    if (argc > 1) {
        strncpy(input, argv[1], sizeof(input) - 1);
    } else {
        printf("Flag: ");
        fflush(stdout);
        if (!fgets(input, sizeof(input), stdin)) {
            return 1;
        }
    }
    input[strcspn(input, "\r\n")] = '\0';

    if (install_filter() != 0) {
        puts("seccomp unavailable.");
        return 1;
    }

    if (strlen(input) != FLAG_LEN) {
        puts("[-] Incorrect flag.");
        return 1;
    }

    int valid = 0;
    for (int i = 0; i < FLAG_LEN; i++) {
        valid += check_char(i, input[i]);
    }

    if (valid == FLAG_LEN) {
        puts("[+] Congratulations, correct flag !");
        return 0;
    }

    puts("[-] Incorrect flag.");
    return 1;
}
