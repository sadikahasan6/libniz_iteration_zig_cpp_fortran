// backend.zig

// This function will be exported as a shared library function
// It calculates Pi using the Leibniz formula
export fn calculate_pi(iterations: u64) f64 {
    var sum: f64 = 0.0;
    var sign: f64 = 1.0;
    for (0..iterations) |i| {
        sum += sign / (2.0 * @as(f64, @floatFromInt(i)) + 1.0);
        sign *= -1;
    }
    return 4.0 * sum;
}

// A simple test to verify our function works in Zig
test "calculate pi" {
    const approx_pi = calculate_pi(1000000);
    // Check if the value is reasonable, not exact
    try @import("std").testing.expect(approx_pi > 3.14 and approx_pi < 3.15);
}