#include <ctype.h>
#include <stdio.h>
#include <string.h>

static void reveal_flag(void) {
    unsigned char encoded[] = {
        118, 98, 26, 116, 100, 76, 90, 82, 83, 94, 66, 90, 104, 90, 66, 91, 67,
        94, 68, 67, 86, 80, 82, 104, 92, 82, 78, 104, 69, 82, 84, 88, 65, 82,
        69, 82, 83, 74
    };
    const unsigned char key = 0x37;
    size_t i;

    fputs("Flag: ", stdout);
    for (i = 0; i < sizeof(encoded); i++) {
        putchar((char)(encoded[i] ^ key));
    }
    putchar('\n');
}

static int check_part1(const char *p1) {
    const int target[4] = {9, 13, 25, 6};
    int i;

    for (i = 0; i < 4; i++) {
        if (!isupper((unsigned char)p1[i])) {
            return 0;
        }
        if ((((p1[i] - 'A') * 7 + 3) % 26) != target[i]) {
            return 0;
        }
    }
    return 1;
}

static int check_part2(const char *p1, const char *p2) {
    int i;
    int sum = 0;
    int value = 0;
    int magic;

    for (i = 0; i < 4; i++) {
        if (!isdigit((unsigned char)p2[i])) {
            return 0;
        }
        sum += (p2[i] - '0');
        value = value * 10 + (p2[i] - '0');
    }

    magic = sum * 13 + (value % 97) + (p1[0] - 'A');
    return magic == 228;
}

static int check_part3(const char *p3) {
    const char expected[4] = {'!', 'R', '3', 'V'};
    int i;

    for (i = 0; i < 4; i++) {
        if (p3[i] != expected[i]) {
            return 0;
        }
    }
    return 1;
}

static int check_checksum(const char *key) {
    int i;
    int sum = 0;

    for (i = 0; key[i] != '\0'; i++) {
        if (key[i] != '-') {
            sum += (unsigned char)key[i];
        }
    }
    return sum == 783;
}

int main(void) {
    char key[128];
    char p1[5], p2[5], p3[5];

    puts("=== Al-Ameen CTF ===");
    puts("Designed by Mustafa Rabbah");
    puts("----------------------");
    puts("Reverse Challenge: Medium 05");
    puts("Expected key format: XXXX-YYYY-ZZZZ");
    printf("Enter key: ");

    if (scanf("%127s", key) != 1) {
        puts("Input error.");
        return 1;
    }

    if (strlen(key) != 14 || key[4] != '-' || key[9] != '-') {
        puts("Invalid format.");
        return 1;
    }

    memcpy(p1, key, 4);
    p1[4] = '\0';
    memcpy(p2, key + 5, 4);
    p2[4] = '\0';
    memcpy(p3, key + 10, 4);
    p3[4] = '\0';

    if (!check_part1(p1) || !check_part2(p1, p2) || !check_part3(p3) || !check_checksum(key)) {
        puts("Wrong key.");
        return 1;
    }

    puts("Key accepted.");
    reveal_flag();
    return 0;
}
