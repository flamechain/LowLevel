long test(long x, long y, long z) {
    long val = x + y + z;

    if (x < -3) {
        if (y < z) {
            val = x*y;
        } else {
            val = ;
        }
    } else if (z >= y) {
        val = ;
    }
    return val
}

int main() {
    test(1, 2, 3);
}
