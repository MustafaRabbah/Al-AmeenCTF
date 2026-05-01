#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ptrace.h>
#include <time.h>

#define IN_LEN 24

static uint32_t rol32(uint32_t v, uint32_t r) {
    return (v << (r & 31)) | (v >> ((32 - r) & 31));
}
static uint64_t rol64(uint64_t v, uint32_t r) {
    return (v << (r & 63)) | (v >> ((64 - r) & 63));
}

static int anti_debug(void) {
    if (getenv("LD_PRELOAD") != NULL) return 1;

    FILE *f = fopen("/proc/self/status", "r");
    if (f) {
        char line[128];
        while (fgets(line, sizeof(line), f)) {
            if (strncmp(line, "TracerPid:", 10) == 0) {
                int pid = atoi(line + 10);
                fclose(f);
                if (pid != 0) return 1;
                return 0;
            }
        }
        fclose(f);
    }

    return 0;
}

static uint64_t phase2_hash(const char *in) {
    static const uint8_t t[16] = {
        0x51, 0xC3, 0x17, 0x9A, 0x2D, 0xEE, 0x74, 0x08,
        0xB1, 0x65, 0x3F, 0xD4, 0x8B, 0x20, 0xFA, 0x46
    };
    uint64_t s = 0x243f6a8885a308d3ULL;
    for (int i = 0; i < IN_LEN; i++) {
        uint64_t v = ((uint8_t)in[i]) ^ t[i & 15];
        s ^= (v + 0x9e37ULL + (s << 6) + (s >> 2));
        s = rol64(s, (uint32_t)((v % 13U) + 5U));
        s += v * 0x100000001b3ULL;
    }
    s ^= s >> 33;
    s *= 0xff51afd7ed558ccdULL;
    s ^= s >> 33;
    s *= 0xc4ceb9fe1a85ec53ULL;
    s ^= s >> 33;
    return s;
}

static void preprocess(const char *in, uint8_t out[IN_LEN]) {
    static const uint8_t k[IN_LEN] = {
        0x73, 0x11, 0xA7, 0x4C, 0x20, 0xD8, 0x92, 0x3B,
        0x55, 0xBE, 0x19, 0x9F, 0xC2, 0x61, 0x0E, 0x74,
        0xE1, 0x33, 0x8A, 0x57, 0xA0, 0x14, 0xCD, 0xF2
    };
    for (int i = 0; i < IN_LEN; i++) {
        uint8_t x = ((uint8_t)in[i]) ^ k[i];
        out[i] = (uint8_t)((x << 1) | (x >> 7));
    }
}

/*
 * "VM-like" mixer:
 * Intentionally difficult to invert directly from constants.
 */
static void vm_mix(const uint8_t m[IN_LEN], uint32_t out[4]) {
    uint32_t r0 = 0x9E3779B9u;
    uint32_t r1 = 0xA5A5A5A5u;
    uint32_t r2 = 0xC3EF3720u;
    uint32_t r3 = 0x13579BDFu;

    for (uint32_t i = 0; i < IN_LEN; i++) {
        uint32_t v = m[i];
        r0 = rol32((r0 + v) ^ (i * 0x45D9F3Bu), 5);
        r1 = (r1 ^ (v + r0)) * 0x45D9F3Bu + 0x27100001u;
        r2 = rol32(r2 + (v ^ r1), 7) ^ 0xA3B1BAC6u;
        r3 = rol32(r3 ^ (r2 + i + v), 9) + 0x7F4A7C15u;

        /* opaque-ish noise */
        if (((r0 ^ r1) & 3u) == 1u) {
            r2 ^= (r0 >> ((i % 5) + 1));
        } else {
            r1 ^= (r3 << ((i % 3) + 1));
        }
    }

    r0 ^= rol32(r2, 11) ^ 0xDEADC0DEu;
    r1 ^= rol32(r3, 13) ^ 0xB16B00B5u;
    r2 ^= rol32(r0, 17) ^ 0x00C0FFEEu;
    r3 ^= rol32(r1, 19) ^ 0xFACEFEEDu;

    out[0] = r0;
    out[1] = r1;
    out[2] = r2;
    out[3] = r3;
}

static void build_sbox(uint8_t s[256], uint64_t seed) {
    for (int i = 0; i < 256; i++) s[i] = (uint8_t)i;
    uint64_t x = seed ^ 0x9e3779b97f4a7c15ULL;
    for (int i = 255; i > 0; i--) {
        x = x * 6364136223846793005ULL + 1ULL;
        uint32_t j = (uint32_t)(x % (uint64_t)(i + 1));
        uint8_t t = s[i];
        s[i] = s[j];
        s[j] = t;
    }
}

static uint8_t dyn_map(uint8_t c, int idx, const uint8_t s[256]) {
    uint8_t x = c;
    for (int r = 0; r < 5; r++) {
        x = s[(uint8_t)(x + (uint8_t)(idx * (r + 3)) + (uint8_t)(r * 17))];
        x = (uint8_t)((x << 1) | (x >> 7));
        x ^= (uint8_t)(0x5A + idx + r);
    }
    return x;
}

/*
 * Dynamic phase: compares input against runtime-decrypted secret
 * through runtime-generated S-Box mapping.
 * This makes pure static extraction significantly harder.
 */
static int phase3_dynamic(const char *input) {
    static const uint8_t sec_enc[IN_LEN] = {
        232, 231, 236, 152, 152, 160, 178, 58,
         55,  72,  20,  98,  30,  24,  22,  55,
         71, 178, 189, 170, 136, 151, 138, 129
    };
    uint8_t sec[IN_LEN];
    for (int i = 0; i < IN_LEN; i++) {
        uint8_t k = (uint8_t)(0xA5 + (i * 13));
        sec[i] = sec_enc[i] ^ k;
    }

    uint8_t sbox[256];
    uint64_t seed = ((uint64_t)(uintptr_t)&phase3_dynamic) ^
                    ((uint64_t)getpid() << 21) ^
                    ((uint64_t)time(NULL) << 7) ^
                    0xD1CEB00B1234ULL;
    build_sbox(sbox, seed);

    uint8_t diff = 0;
    for (int i = 0; i < IN_LEN; i++) {
        uint8_t a = dyn_map((uint8_t)input[i], i, sbox);
        uint8_t b = dyn_map(sec[i], i, sbox);
        diff |= (uint8_t)(a ^ b);
    }
    return diff == 0;
}

static int verify(const char *input) {
    if (strlen(input) != IN_LEN) return 0;
    if (anti_debug()) return 0;

    uint8_t buf[IN_LEN];
    uint32_t regs[4];
    preprocess(input, buf);
    vm_mix(buf, regs);

    uint64_t h = phase2_hash(input);
    uint64_t h_mask = 0xA17C39D24BEF1065ULL;
    uint64_t h_expected_x = 0x3BB58054225B0415ULL; /* expected ^ mask */
    uint64_t h_expected = h_expected_x ^ h_mask;

    return (regs[0] == 0x01CFA15Eu &&
            regs[1] == 0xF6592648u &&
            regs[2] == 0x4E0EFC9Bu &&
            regs[3] == 0xC79AD25Cu &&
            h == h_expected &&
            phase3_dynamic(input));
}

int main(void) {
    char input[128];

    puts("Al-Ameen CTF");
    puts("Designed by Mustafa Rabbah");
    puts("[Hard] VM Labyrinth");
    puts("Enter activation phrase:");

    if (!fgets(input, sizeof(input), stdin)) return 1;
    input[strcspn(input, "\n")] = '\0';

    if (verify(input)) {
        puts("Access granted.");
        puts("AU-CS{hard_vm_labyrinth_2026_77}");
    } else {
        puts("Access denied.");
    }
    return 0;
}

