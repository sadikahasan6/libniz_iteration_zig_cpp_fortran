#include <cstdint>
#include <cassert>

extern "C" double calculate_pi(uint64_t iterations) {
    double sum = 0.0;
    double sign = 1.0;
    for (uint64_t i = 0; i < iterations; ++i) {
        sum += sign / (2.0 * static_cast<double>(i) + 1.0);
        sign *= -1.0;
    }
    return 4.0 * sum;
}

#ifdef RUN_TESTS
void test_calculate_pi() {
    double approx_pi = calculate_pi(1000000);
    assert(approx_pi > 3.14 && approx_pi < 3.15 && "Pi approximation out of expected range");
}

int main() {
    test_calculate_pi();
    return 0;
}
#endif