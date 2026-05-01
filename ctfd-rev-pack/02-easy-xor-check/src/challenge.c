#include <stdio.h>
#include <string.h>

static void reveal_flag(void) {
    unsigned char encoded[] = {
        118, 98, 26, 116, 100, 76, 82, 86, 68, 78, 104, 79, 88, 69,
        104, 84, 95, 82, 84, 92, 104, 81, 88, 66, 89, 83, 74
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
    const unsigned char enc[8] = {55, 47, 41, 46, 59, 60, 59, 109};
    size_t i;

    if (strlen(s) != 8) {
        return 0;
    }

    for (i = 0; i < 8; i++) {
        if (((unsigned char)s[i] ^ 0x5A) != enc[i]) {
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
    puts("Reverse Challenge: Easy 02");
    printf("Enter key: ");

    if (scanf("%127s", input) != 1) {
        puts("Input error.");
        return 1;
    }

    if (verify(input)) {
        puts("Correct key.");
        reveal_flag();
    } else {
        puts("Invalid key.");
    }

    return 0;
}
