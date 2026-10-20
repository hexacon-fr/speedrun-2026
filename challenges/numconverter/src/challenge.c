#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

#define BUFFER_SIZE 0x40
#define COUNT_ELEMENTS(x) (sizeof(x) / sizeof(*x))

static char buf[BUFFER_SIZE] = { 0 };

static char * formatters[] = {
    "%lu",
    "0x%lx",
    "0o%lo",
};

static int formatters_count = COUNT_ELEMENTS(formatters);

static void win(void)
{
    printf("Congratulations, here is your bounty:\n");
    execve("/bin/sh", NULL, NULL);
}

static size_t read_int(void)
{
    read(0, buf, sizeof buf);
    return strtoull(buf, NULL, 10);
}

static size_t formatter_menu(void)
{
    printf("0. Decimal\n");
    printf("1. Hexadecimal\n");
    printf("2. Octal\n");
    printf("> ");

    return read_int();
}

static void __attribute__((constructor)) setup(void)
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
}

int main(int argc, char * argv[])
{
    size_t in_formatter, out_formatter, value;

    printf("Welcome to my number converter !\n");
    
    printf("Choose your input number representation\n");
    in_formatter = formatter_menu();

    printf("Enter the number to convert: ");
    scanf(formatters[in_formatter], &value);

    printf("Choose your output number representation\n");
    out_formatter = formatter_menu();

    if (in_formatter >= formatters_count ||
        out_formatter >= formatters_count) {
        printf("Invalid formatters\n");
        return 1;
    }
    
    snprintf(buf, sizeof(buf) - 1, "%s = %s\n",  
        formatters[in_formatter], formatters[out_formatter]
    );
    
    // Finally format the in / out formatters and print the conversion
    printf(buf, value, value);

    return 0;
}
