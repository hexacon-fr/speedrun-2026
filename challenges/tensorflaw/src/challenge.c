#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define VRAM_BUDGET  4096      /* bytes of weights the GPU can hold */

typedef struct {
    size_t rows;
    size_t cols;
    float vram[VRAM_BUDGET / sizeof(float)];
    int (*status)(const char *name);
    char name[16];
} gpu_t;

static gpu_t g_gpu;

static int gpu_report(const char *name) {
    printf("%s: ", name);
    return system("uptime");
}

static void __attribute__((constructor)) setup(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    g_gpu.status = gpu_report;
    strcpy(g_gpu.name, "HTX 6000");
}

static void load_tensor(void) {
    size_t rows = 0, cols = 0;

    printf("Rows: ");
    scanf("%zu", &rows);
    printf("Cols: ");
    scanf("%zu", &cols);

    /* Keep the tensor inside the VRAM budget. */
    size_t bytes = rows * cols * sizeof(float);
    if (bytes == 0 || bytes > VRAM_BUDGET) {
        puts("VRAM budget exceeded.");
        return;
    }

    g_gpu.rows = rows;
    g_gpu.cols = cols;
    printf("Tensor loaded (%zu x %zu).\n", rows, cols);
}

static void upload_weights(void) {
    if (g_gpu.rows * g_gpu.cols == 0) {
        puts("No tensor loaded.");
        return;
    }

    printf("Weights: ");
    for (size_t i = 0; i < g_gpu.rows * g_gpu.cols; i++) {
        if (scanf("%f", &g_gpu.vram[i]) != 1) {
            puts("Invalid weight, upload aborted.");
            scanf("%*[^\n]");
            return;
        }
    }
    puts("Weights uploaded.");
}

int main(void) {
    int choice;

    puts("=== TensorFlaw ===");
    while (1) {
        printf("\n");
        printf("1. Load tensor\n");
        printf("2. Upload weights\n");
        printf("3. GPU status\n");
        printf("4. Shutdown\n");
        printf("> ");

        if (scanf("%d", &choice) != 1)
            break;

        switch (choice) {
            case 1: load_tensor();                break;
            case 2: upload_weights();             break;
            case 3: g_gpu.status(g_gpu.name);     break;
            default: return 0;
        }
    }
    return 0;
}
