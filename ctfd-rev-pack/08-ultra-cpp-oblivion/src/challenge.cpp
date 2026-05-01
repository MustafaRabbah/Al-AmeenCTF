#include <iostream>
#include <vector>
#include <array>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <string>
#include <unistd.h>

static constexpr size_t IN_LEN = 28;

static uint64_t rol64(uint64_t x, uint32_t r) {
    return (x << (r & 63)) | (x >> ((64 - r) & 63));
}

static bool anti_debug() {
    const char *lp = getenv("LD_PRELOAD");
    if (lp && *lp) return true;

    std::ifstream f("/proc/self/status");
    if (!f.good()) return false;
    std::string line;
    while (std::getline(f, line)) {
        if (line.rfind("TracerPid:", 0) == 0) {
            int pid = std::stoi(line.substr(10));
            return pid != 0;
        }
    }
    return false;
}

// --- lots of noisy arithmetic helpers to bloat CFG ---
#define JF(N, A, B) \
static uint64_t junk_##N(uint64_t x) { \
    x ^= (0x9e3779b97f4a7c15ULL + (uint64_t)(N) * (A)); \
    x = rol64(x, ((N) % 17) + 5); \
    x += (uint64_t)(B) * 0x100000001b3ULL; \
    x ^= (x >> (((N) % 11) + 1)); \
    return x; \
}

JF(0,13,7) JF(1,29,11) JF(2,31,19) JF(3,37,23) JF(4,41,29)
JF(5,43,31) JF(6,47,37) JF(7,53,41) JF(8,59,43) JF(9,61,47)
JF(10,67,53) JF(11,71,59) JF(12,73,61) JF(13,79,67) JF(14,83,71)
JF(15,89,73) JF(16,97,79) JF(17,101,83) JF(18,103,89) JF(19,107,97)
JF(20,109,101) JF(21,113,103) JF(22,127,107) JF(23,131,109) JF(24,137,113)
JF(25,139,127) JF(26,149,131) JF(27,151,137) JF(28,157,139) JF(29,163,149)
JF(30,167,151) JF(31,173,157) JF(32,179,163) JF(33,181,167) JF(34,191,173)
JF(35,193,179) JF(36,197,181) JF(37,199,191) JF(38,211,193) JF(39,223,197)
JF(40,227,199) JF(41,229,211) JF(42,233,223) JF(43,239,227) JF(44,241,229)
JF(45,251,233) JF(46,257,239) JF(47,263,241) JF(48,269,251) JF(49,271,257)
JF(50,277,263) JF(51,281,269) JF(52,283,271) JF(53,293,277) JF(54,307,281)
JF(55,311,283) JF(56,313,293) JF(57,317,307) JF(58,331,311) JF(59,337,313)
JF(60,347,317) JF(61,349,331) JF(62,353,337) JF(63,359,347)

using JFPtr = uint64_t(*)(uint64_t);
static const std::array<JFPtr, 64> JTAB = {
    junk_0,junk_1,junk_2,junk_3,junk_4,junk_5,junk_6,junk_7,
    junk_8,junk_9,junk_10,junk_11,junk_12,junk_13,junk_14,junk_15,
    junk_16,junk_17,junk_18,junk_19,junk_20,junk_21,junk_22,junk_23,
    junk_24,junk_25,junk_26,junk_27,junk_28,junk_29,junk_30,junk_31,
    junk_32,junk_33,junk_34,junk_35,junk_36,junk_37,junk_38,junk_39,
    junk_40,junk_41,junk_42,junk_43,junk_44,junk_45,junk_46,junk_47,
    junk_48,junk_49,junk_50,junk_51,junk_52,junk_53,junk_54,junk_55,
    junk_56,junk_57,junk_58,junk_59,junk_60,junk_61,junk_62,junk_63
};

static uint64_t phase_hash(const std::string &s) {
    uint64_t h = 0x6a09e667f3bcc909ULL;
    for (size_t i = 0; i < s.size(); i++) {
        uint64_t b = (uint8_t)s[i];
        h ^= (b + (i * 0x9dULL) + (h << 7) + (h >> 3));
        h = rol64(h, (uint32_t)((b % 17ULL) + 5ULL));
        h = h * 0x100000001b3ULL + 0x9e3779b97f4a7c15ULL;
        h = JTAB[(i * 7 + b) & 63](h);
    }
    h ^= h >> 33;
    h *= 0xff51afd7ed558ccdULL;
    h ^= h >> 33;
    h *= 0xc4ceb9fe1a85ec53ULL;
    h ^= h >> 33;
    return h;
}

static bool phase_dynamic(const std::string &s) {
    static const uint8_t enc[IN_LEN] = {
        232,213,188,158,112,90,58,156,183,167,149,126,80,18,234,193,
        187,143,124,74,17,243,179,198,229,8,70,99
    };
    uint8_t d = 0;
    for (size_t i = 0; i < IN_LEN; i++) {
        uint8_t key = (uint8_t)(0xA5 ^ ((i * 37) & 0xff));
        uint8_t sec = enc[i] ^ key;
        d |= (uint8_t)((uint8_t)s[i] ^ sec);
    }
    return d == 0;
}

static std::string decrypt_flag() {
    static const uint8_t encf[35] = {
        28,61,94,61,218,239,234,198,193,178,170,137,130,156,135,93,98,122,
        79,71,79,45,32,52,58,66,75,180,167,195,159,130,133,248,174
    };
    std::string out;
    out.resize(35);
    for (size_t i = 0; i < 35; i++) {
        out[i] = (char)(encf[i] ^ ((0x5D + (i * 11)) & 0xff));
    }
    return out;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::cout << "Al-Ameen CTF\n";
    std::cout << "Designed by Mustafa Rabbah\n";
    std::cout << "[Ultra] C++ Oblivion Engine\n";
    std::cout << "Enter activation phrase:\n";

    std::string in;
    std::getline(std::cin, in);
    if (in.size() != IN_LEN || anti_debug()) {
        std::cout << "Access denied.\n";
        return 0;
    }

    const uint64_t expected = 0xa151c6d389966b0eULL;
    if (phase_hash(in) == expected && phase_dynamic(in)) {
        std::cout << "Access granted.\n";
        std::cout << decrypt_flag() << "\n";
    } else {
        std::cout << "Access denied.\n";
    }
    return 0;
}

