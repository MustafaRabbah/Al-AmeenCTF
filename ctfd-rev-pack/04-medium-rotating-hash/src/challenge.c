#include <stdint.h>
#include <stdio.h>
#include <string.h>

static void reveal_flag(void) {
    unsigned char encoded[] = {
        118, 98, 26, 116, 100, 76, 90, 82, 83, 94, 66, 90, 104, 84, 66, 68, 67,
        88, 90, 104, 95, 86, 68, 95, 104, 84, 69, 86, 84, 92, 82, 83, 74
    };
    const unsigned char key = 0x37;
    size_t i;

    fputs("Flag: ", stdout);
    for (i = 0; i < sizeof(encoded); i++) {
        putchar((char)(encoded[i] ^ key));
    }
    putchar('\n');
}

static uint32_t custom_hash(const char *s) {
    uint32_t h = 0x1337;
    size_t i;

    for (i = 0; s[i] != '\0'; i++) {
        h = (h << 5) | (h >> 27);
        h ^= (uint8_t)s[i];
        h += 0x9e3779b9;
    }
    return h;
}

int main(void) {
    char input[128];
    const uint32_t target = 0xA52DF298;

    puts("=== Al-Ameen CTF ===");
    puts("Designed by Mustafa Rabbah");
    puts("----------------------");
    puts("Reverse Challenge: Medium 04");
    printf("Enter phrase: ");

    if (scanf("%127s", input) != 1) {
        puts("Input error.");
        return 1;
    }

    if (custom_hash(input) == target) {
        puts("Hash matched.");
        reveal_flag();
    } else {
        puts("No match.");
    }

    return 0;
}
