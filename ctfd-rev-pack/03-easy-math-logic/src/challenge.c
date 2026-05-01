#include <stdio.h>
#include <string.h>

static void reveal_flag(void) {
    unsigned char encoded[] = {
        118, 98, 26, 116, 100, 76, 82, 86, 68, 78, 104, 90, 86, 67, 95, 104,
        91, 88, 80, 94, 84, 104, 69, 82, 65, 82, 69, 68, 82, 83, 74
    };
    const unsigned char key = 0x37;
    size_t i;

    fputs("Flag: ", stdout);
    for (i = 0; i < sizeof(encoded); i++) {
        putchar((char)(encoded[i] ^ key));
    }
    putchar('\n');
}

static int verify(const char *s) {
    const int target[6] = {9, 0, 6, 4, 3, 2};
    int i;

    if (strlen(s) != 6) {
        return 0;
    }

    for (i = 0; i < 6; i++) {
        if (s[i] < '0' || s[i] > '9') {
            return 0;
        }
    }

    for (i = 0; i < 6; i++) {
        int d = s[i] - '0';
        int t = (d * 3 + i * 7) % 10;
        if (t != target[i]) {
            return 0;
        }
    }
    return 1;
}

int main(void) {
    char input[128];

    puts("=== Al-Ameen CTF ===");
    puts("Designed by Mustafa Rabbah");
    puts("----------------------");
    puts("Reverse Challenge: Easy 03");
    printf("Enter 6-digit code: ");

    if (scanf("%127s", input) != 1) {
        puts("Input error.");
        return 1;
    }

    if (verify(input)) {
        puts("Code accepted.");
        reveal_flag();
    } else {
        puts("Code rejected.");
    }

    return 0;
}
