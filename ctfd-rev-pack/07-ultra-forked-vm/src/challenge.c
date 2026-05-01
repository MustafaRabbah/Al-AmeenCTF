#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdlib.h>

#define N 24

static uint32_t qx_9f(uint32_t x, int r){ return (x<<r)|(x>>(32-r)); }

static int zc_m1(const char *s){
    uint32_t h=0x13572468;
    for(int i=0;i<N;i++){
        h = qx_9f(h ^ (uint8_t)s[i] ^ (i*17), 5) + 0x9e3779b9;
    }
    return h == 0x2ea2f1ef;
}

static int bt_k7(const char *s){
    static const uint8_t k[N]={74,65,114,122,122,14,20,88,85,41,197,194,241,241,226,156,154,187,194,207,56,43,18,19};
    uint8_t d=0;
    for(int i=0;i<N;i++){
        d |= (((uint8_t)s[i] ^ k[i]) - ((i*13+7)&0xff));
    }
    return d==0;
}

static int rq_v2(const char *s){
    /* runtime-decrypted stage to increase reverse complexity */
    static const uint8_t e[N] = {
        0x16,0x18,0x3C,0x75,0x6E,0x97,0x42,0x9F,
        0x89,0x30,0xCB,0x2D,0x55,0x68,0x84,0xAB,
        0xC6,0xE2,0x6C,0xA0,0x2C,0x72,0x04,0xF4
    };
    uint8_t v = 0;
    for(int i=0;i<N;i++){
        uint8_t kk = (uint8_t)((0x5B ^ (i*29)) + ((i&3)*7));
        uint8_t d  = e[i] ^ kk;
        uint8_t c  = (uint8_t)s[i];
        c = (uint8_t)((c << 1) | (c >> 7));
        d = (uint8_t)((d << 1) | (d >> 7));
        v |= (uint8_t)(c ^ d);
    }
    return v == 0;
}

static void pw_o0(void){
    static const uint8_t a[32] = {
        87, 154, 28, 104, 92, 161, 54, 217,
        168, 171, 77, 3, 41, 141, 253, 95,
        7, 79, 236, 91, 251, 80, 162, 179,
        96, 169, 76, 82, 167, 179, 29, 219
    };
    static const uint8_t b[32] = {
        22, 207, 49, 43, 15, 218, 67, 181,
        220, 217, 44, 92, 91, 232, 139, 0,
        97, 32, 158, 48, 158, 52, 253, 197,
        13, 246, 127, 99, 148, 128, 42, 166
    };
    volatile uint8_t noise = (uint8_t)(getpid() & 0xff);
    char out[33];
    for(int i=0;i<32;i++){
        out[i] = (char)(a[i] ^ b[i] ^ noise ^ noise);
    }
    out[32] = '\0';
    puts(out);
}

int main(){
    char in[128];
    puts("Al-Ameen CTF");
    puts("Designed by Mustafa Rabbah");
    puts("[Ultra] Forked VM");
    puts("Enter key:");
    if(!fgets(in,sizeof(in),stdin)) return 1;
    in[strcspn(in,"\n")] = 0;
    if(strlen(in)!=N){ puts("Denied"); return 0; }

    int p[2]; pipe(p);
    pid_t pid = fork();
    if(pid==0){
        close(p[0]);
        int ok = bt_k7(in) && rq_v2(in);
        write(p[1], &ok, sizeof(ok));
        close(p[1]);
        _exit(0);
    }
    close(p[1]);
    int okb=0; read(p[0], &okb, sizeof(okb)); close(p[0]);
    wait(NULL);

    if(zc_m1(in) && okb){
        puts("Access granted");
        pw_o0();
    } else {
        puts("Access denied");
    }
    return 0;
}

