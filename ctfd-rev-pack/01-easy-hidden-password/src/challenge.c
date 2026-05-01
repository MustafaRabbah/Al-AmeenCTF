#include <stdio.h>
#include <string.h>

static void reveal_flag(void) {
    unsigned char encoded[] = {
        118, 98, 26, 116, 100, 76, 82, 86, 68, 78, 104, 68, 67, 69, 94, 89,
        80, 68, 104, 86, 69, 82, 104, 71, 88, 64, 82, 69, 81, 66, 91, 74
    };
    const unsigned char key = 0x37;
    size_t i;

    fputs("Flag: ", stdout);
    for (i = 0; i < sizeof(encoded); i++) {
        putchar((char)(encoded[i] ^ key));
    }
    putchar('\n');
}

int main(void) {
    char input[128];
    const char *secret = "open_sesame_rev";

    puts("=== Al-Ameen CTF ===");
    puts("Designed by Mustafa Rabbah");
    puts("----------------------");
    puts("Reverse Challenge: Easy 01");
    printf("Enter password: ");

    if (scanf("%127s", input) != 1) {
        puts("Input error.");
        return 1;
    }

    if (strcmp(input, secret) == 0) {
        puts("Access granted.");
        reveal_flag();
    } else {
        puts("Wrong password.");
    }

    return 0;
}
