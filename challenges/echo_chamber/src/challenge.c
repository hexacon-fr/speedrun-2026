#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FLAG_PATH "flag.txt"
#define FLAG_SIZE 0x80

char flag[FLAG_SIZE];

static void load_flag(void) {
    FILE *f = fopen(FLAG_PATH, "r");

    if (!f) {
        puts("Could not open " FLAG_PATH ", this should not happen.");
        exit(1);
    }

    size_t n = fread(flag, 1, sizeof(flag) - 1, f);
    fclose(f);

    flag[n] = '\0';
    flag[strcspn(flag, "\n")] = '\0';
}

// Filter nasty formatters, heard %n was harmful
static int filter_input(const char *s) {
    while ((s = strchr(s, '%')) != NULL) {
        if (*++s == '%') {
            s++;
            continue;
        }
        // position, flags, width, precision and length modifiers are safe
        s += strspn(s, "0123456789$#-+ '.*hljztLqI");
        if (*s == 'n') {
            return 1;
        }
    }

    return 0;
}

static void __attribute__((constructor)) setup(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    load_flag();
}

int main(void) {
    char input[256] = {0};

    puts("Welcome to echo chamber.");
    puts("Say something (max 255 bytes):");

    while(1){
        if (fgets(input, sizeof(input), stdin) == NULL) {
            return 1;
        }

        if (strstr(input, "exit")) {
            break;
        }

        input[strcspn(input, "\n")] = '\0';

        if (filter_input(input)) {
            puts("Nice try. %n-style writes are forbidden.");
            return 1;
        }

        printf(input);
        printf("\n");

    }
    return 0;
}
