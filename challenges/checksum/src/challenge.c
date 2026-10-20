#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <openssl/evp.h>

#define BUF_SIZE 64

static char *g_data_buf = NULL;
static char *g_flag_buf = NULL;

static void __attribute__((constructor)) setup(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

static void load_flag(void) {
    FILE *f = fopen("flag.txt", "r");
    if (!f) {
        puts("Cannot open flag file.");
        exit(1);
    }
    fgets(g_flag_buf, BUF_SIZE, f);
    g_flag_buf[strcspn(g_flag_buf, "\n")] = '\0';
    fclose(f);
}

static void compute_sha1(const void *data, size_t len, unsigned char *out) {
    EVP_MD_CTX *ctx = EVP_MD_CTX_new();
    unsigned int md_len;
    EVP_DigestInit_ex(ctx, EVP_sha1(), NULL);
    EVP_DigestUpdate(ctx, data, len);
    EVP_DigestFinal_ex(ctx, out, &md_len);
    EVP_MD_CTX_free(ctx);
}

static void print_menu(void) {
    puts("\n=== Checksum Service ===");
    puts("1. Write Data");
    puts("2. Compute SHA-1");
    puts("3. Exit");
    printf("> ");
}

int main(void) {
    int choice;

    g_data_buf = malloc(BUF_SIZE);
    g_flag_buf = malloc(BUF_SIZE);
    if (!g_data_buf || !g_flag_buf) return 1;
    memset(g_data_buf, 0, BUF_SIZE);
    memset(g_flag_buf, 0, BUF_SIZE);

    load_flag();

    while (1) {
        print_menu();
        if (scanf("%d", &choice) != 1) break;

        switch (choice) {
            case 1: {
                printf("Enter data: ");
                read(0, g_data_buf, BUF_SIZE);
                puts("Data stored.");
                break;
            }
            case 2: {
                unsigned int len;
                printf("Length: ");
                if (scanf("%u", &len) != 1) break;

                if (len == 0) {
                    puts("Invalid length.");
                    break;
                }

                unsigned char hash[20];
                compute_sha1(g_data_buf, len, hash);

                printf("SHA-1: ");
                for (int i = 0; i < 20; i++) {
                    printf("%02x", hash[i]);
                }
                puts("");
                break;
            }
            case 3:
                puts("Goodbye.");
                return 0;
            default:
                puts("Invalid choice.");
        }
    }
    return 0;
}
