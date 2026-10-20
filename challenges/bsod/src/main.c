#include <stdio.h>
#include <string.h>
#include <ctype.h>

#include "logo.h"

#define RESET  "\033[0m"
#define WHITE  "\033[1;37m"
#define GRAY   "\033[0;37m"
#define LRED   "\033[1;31m"
#define LGREEN "\033[1;32m"
#define YELLOW "\033[1;33m"

static const char *cell_color(char c)
{
    switch (c) {
    case 'K': return "\033[0;30;100m";
    case 'R': return "\033[1;31;41m";
    case 'G': return "\033[1;32;42m";
    case 'B': return "\033[1;34;44m";
    case 'Y': return "\033[1;33;43m";
    default:  return RESET;
    }
}

static void draw_logo(void)
{
    for (int i = 0; i < LOGO_ROWS; i++) {
        char cur = 0;

        fputs("  ", stdout);
        for (const char *p = LOGO[i]; *p; p++) {
            if (*p != cur) {
                cur = *p;
                fputs(cell_color(cur), stdout);
            }
            putchar(cur == ' ' ? ' ' : '#');
        }
        puts(RESET);
    }

    putchar('\n');
    for (int i = 0; i < TITLE_ROWS; i++)
        printf("  %s%s" RESET "\n", i == 0 ? GRAY : WHITE, TITLE[i]);
}

static int all_digits(const char *s, int n)
{
    for (int i = 0; i < n; i++)
        if (s[i] < '0' || s[i] > '9')
            return 0;
    return 1;
}

static int number(const char *s, int n)
{
    int v = 0;
    for (int i = 0; i < n; i++)
        v = v * 10 + (s[i] - '0');
    return v;
}

// digit sum divisible by 13 and a last digit that is not [0, 8, 9]
static int check_block(const char *s)
{
    int sum = 0;

    for (int i = 0; i < 7; i++)
        sum += s[i] - '0';
    if (s[6] == '0' || s[6] >= '8')
        return 0;
    return sum % 13 == 0;
}

/* DDDYY-OEM-0XXXXXX-XXXXX */
static int check_oem(const char *k)
{
    if (k[5] != '-' || k[9] != '-' || k[17] != '-')
        return 0;
    if (k[6] != 'O' || k[7] != 'E' || k[8] != 'M')
        return 0;
    if (!all_digits(k, 5) || !all_digits(k + 10, 7) || !all_digits(k + 18, 5))
        return 0;

    int day = number(k, 3), year = number(k + 3, 2);
    if (day < 1 || day > 366)
        return 0;
    if (year < 95 && year > 3)
        return 0;
    if (k[10] != '0')
        return 0;
    return check_block(k + 10);
}

static int check_key(const char *k)
{
    return strlen(k) == 23 && check_oem(k);
}

static void print_flag(void)
{
    char flag[128];
    FILE *f = fopen("flag.txt", "r");

    if (!f || !fgets(flag, sizeof(flag), f)) {
        puts("  flag.txt is missing, please contact an admin.");
        return;
    }
    fclose(f);
    flag[strcspn(flag, "\r\n")] = 0;
    printf("  " YELLOW "%s" RESET "\n", flag);
}

int main(void)
{
    char key[64];

    setvbuf(stdout, NULL, _IONBF, 0);

    fputs("\033[2J\033[H", stdout);
    draw_logo();
    puts("\n  Type the OEM Product ID printed on your Certificate of Authenticity.\n");
    fputs(WHITE "  CD Key: " RESET, stdout);

    if (!fgets(key, sizeof(key), stdin))
        return 1;
    key[strcspn(key, "\r\n")] = 0;
    for (char *p = key; *p; p++)
        *p = toupper((unsigned char)*p);

    if (check_key(key)) {
        puts(LGREEN "  Product ID accepted. Welcome to Windows 95!" RESET);
        print_flag();
        return 0;
    }
    puts(LRED "  The CD Key you entered is not valid. Setup will now exit." RESET);
    return 1;
}
