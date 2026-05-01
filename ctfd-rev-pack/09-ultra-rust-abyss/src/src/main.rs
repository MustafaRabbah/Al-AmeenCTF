use std::env;
use std::fs;
use std::hint::black_box;
use std::time::{SystemTime, UNIX_EPOCH};

const IN_LEN: usize = 26;
const H_EXPECT: u64 = 0x57a6_e61e_33e5_b058;
const P2_ENC: [u8; IN_LEN] = [
    228, 239, 152, 136, 172, 184, 78, 26, 11, 16, 6, 55, 33, 217, 214, 234, 224, 153, 136, 179,
    196, 62, 38, 0, 96, 115,
];

const FLAG_ENC: [u8; 32] = [
    29, 4, 107, 56, 59, 102, 103, 107, 64, 91, 191, 140, 178, 128, 153, 235, 211, 224, 212, 210,
    43, 62, 29, 19, 29, 119, 81, 58, 0, 28, 234, 178,
];

fn anti_dbg() -> bool {
    if env::var("LD_PRELOAD").is_ok() {
        return true;
    }
    if let Ok(s) = fs::read_to_string("/proc/self/status") {
        for l in s.lines() {
            if let Some(v) = l.strip_prefix("TracerPid:") {
                if v.trim() != "0" {
                    return true;
                }
            }
        }
    }
    false
}

fn rotl64(x: u64, r: u32) -> u64 {
    x.rotate_left(r)
}

fn p1_hx(inp: &[u8]) -> u64 {
    let mut h: u64 = 0x9e37_79b9_7f4a_7c15;
    for (i, b) in inp.iter().enumerate() {
        let t = (*b as u64)
            .wrapping_add(((i as u64) + 1).wrapping_mul(0x45))
            .wrapping_add(h.wrapping_shl(5))
            .wrapping_add(h >> 2);
        h ^= t;
        h = rotl64(h, ((*b % 19) + 3) as u32);
        h = h
            .wrapping_mul(0x1000_0000_01b3)
            .wrapping_add(0x27d4_eb2f_1656_67c5);
    }
    h ^= h >> 33;
    h = h.wrapping_mul(0xff51_afd7_ed55_8ccd);
    h ^= h >> 33;
    h = h.wrapping_mul(0xc4ce_b9fe_1a85_ec53);
    h ^= h >> 33;
    h
}

fn p2_dyn(inp: &[u8]) -> bool {
    let nanos = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|d| d.as_nanos() as u64)
        .unwrap_or(0);
    let seed = (std::process::id() as u64)
        .wrapping_mul(0x9e37_79b1)
        .wrapping_add(nanos & 0xffff);
    let noise = ((seed ^ (seed >> 17) ^ (seed << 7)) & 0xff) as u8;
    black_box(noise);

    let mut ok = true;
    for i in 0..IN_LEN {
        let m = (0xA9u8).wrapping_add((i as u8).wrapping_mul(17));
        let d = P2_ENC[i] ^ m;
        ok &= inp[i] == d;
    }
    ok
}

fn p3_vm(inp: &[u8]) -> bool {
    let mut acc: u64 = 0x6d5a_b73c_c41d_e992;
    for (i, b) in inp.iter().enumerate() {
        let mut v = (*b as u64) ^ ((i as u64).wrapping_mul(0x13));
        for _ in 0..4 {
            v ^= v << 7;
            v ^= v >> 9;
            v ^= v << 8;
            acc = acc.rotate_left(11) ^ v.wrapping_mul(0x9e37_79b9);
            acc = acc.wrapping_add(0xa076_1d64_78bd_642f);
        }
    }
    (acc ^ 0x8f7a_21d3_c54e_9012) == 0xc57e_6988_ce57_3abf
}

fn flag_out() -> String {
    let mut out = String::with_capacity(FLAG_ENC.len());
    for (i, c) in FLAG_ENC.iter().enumerate() {
        let k = 0x5Cu8 ^ ((i as u8).wrapping_mul(13));
        out.push((c ^ k) as char);
    }
    out
}

fn spam_noise() -> u64 {
    let mut z = 0x1234_5678_9abc_def0u64;
    for i in 0..3000u64 {
        z ^= i.wrapping_mul(0x9e37_79b9_7f4a_7c15);
        z = z.rotate_left(((i & 31) + 1) as u32);
        z = z.wrapping_mul(0xff51_afd7_ed55_8ccd).wrapping_add(i ^ 0xa5);
        black_box(z);
    }
    z
}

fn main() {
    let _ = spam_noise();
    if anti_dbg() {
        println!("denied");
        return;
    }

    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        println!("usage: ./abyss <key>");
        return;
    }
    let input = args[1].as_bytes();
    if input.len() != IN_LEN {
        println!("nope");
        return;
    }
    if p1_hx(input) != H_EXPECT {
        println!("nope");
        return;
    }
    if !p2_dyn(input) {
        println!("nope");
        return;
    }
    if !p3_vm(input) {
        println!("nope");
        return;
    }
    println!("{}", flag_out());
}

