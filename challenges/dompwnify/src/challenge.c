#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_INPUT 64

static void __attribute__((constructor)) setup(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

static void html_sanitize(const char *src, char *dst) {
    for (; *src; src++) {
        switch (*src) {
            case '&':  dst = stpcpy(dst, "&amp;");  break;
            case '<':  dst = stpcpy(dst, "&lt;");   break;
            case '>':  dst = stpcpy(dst, "&gt;");   break;
            case '"':  dst = stpcpy(dst, "&quot;"); break;
            case '\'': dst = stpcpy(dst, "&#39;");  break;
            default:   *dst++ = *src;
        }
    }
    *dst = '\0';
}

static void include_file(const char *path) {
    char line[256];
    FILE *f = fopen(path, "r");

    if (!f) {
        printf("<!-- missing %s -->\n", path);
        return;
    }

    while (fgets(line, sizeof(line), f))
        fputs(line, stdout);

    fclose(f);
}

int main(void) {
    struct {
        char unsanitized[MAX_INPUT + 1];
        char sanitized[2 * MAX_INPUT];
        char footer_filename[32];
    } ctx = {};

    strcpy(ctx.footer_filename, "footer.html");

    printf("=== Hello App (sanitized by DOMPwnify) ===\n");
    printf("What is your name ? (max %d chars) ", MAX_INPUT);

    if (!fgets(ctx.unsanitized, sizeof(ctx.unsanitized), stdin))
        return 1;

    ctx.unsanitized[strcspn(ctx.unsanitized, "\n")] = '\0';

    html_sanitize(ctx.unsanitized, ctx.sanitized);

    printf("\n<html><body>\n");
    printf("<h1>Hello App</h1>\n");
    printf("<p>Hello %s !</p>\n", ctx.sanitized);
    include_file(ctx.footer_filename);
    puts("</body></html>");

    return 0;
}
