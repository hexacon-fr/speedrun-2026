#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>

#define BUF_SIZE  0x20
#define LOCK_SIZE 0x40

static char lock[LOCK_SIZE + 1];
static bool disable_backdoor = true;

// Initialize secret lock (hex)
static bool configure_vault(void)
{
    FILE *fp = NULL;
    
    if ((fp = fopen("/dev/urandom", "rb")) == NULL) {
        perror("fopen");
        return false;
    }

    char raw_lock[LOCK_SIZE / 2];
    if (fread(raw_lock, sizeof *raw_lock, sizeof raw_lock, fp) 
        != sizeof raw_lock) {
        perror("fread");
        return false;
    }

    for (int i = 0; i < sizeof raw_lock; i++) {
        snprintf(&lock[i * 2], 3, "%02hhx", raw_lock[i]);
    }

    fclose(fp);

    return true;
}

static void __attribute__((constructor)) setup(void)
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    
    if (!configure_vault()) {
        printf("The vault could not be configured. This should not happen (:\n");
        exit(-1);
    }
}

static size_t read_long(void)
{
    char buf[BUF_SIZE] = { };
    fgets(buf, sizeof buf, stdin);
    return strtoull(buf, NULL, 10);
}

static void read_str(char *buf, uint32_t size)
{
    read(0, buf, size);
    buf[size - 1] = '\0';
}

static void open_vault(void)
{
    printf("The vault is opening...\n");
    system("/bin/sh");
}

int main(int argc, char * argv[])
{
    printf("Welcome to the vault !\n");
    printf("Try to unlock it! Be careful you've got only 1 try !\n\n");

    printf("How many moves do you need ? ");
    uint64_t guess_size = read_long();

    char *guess = malloc(guess_size);

    printf("Ok, now this is your time to shine: ");
    read_str(guess, guess_size);
    
    if (disable_backdoor && strncmp(lock, guess, LOCK_SIZE)) {
        printf("Sadly this doesn't seem to open the vault...\n");
        return 1;
    }

    open_vault();

    return 0;
}
