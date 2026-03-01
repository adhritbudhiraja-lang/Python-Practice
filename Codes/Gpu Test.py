"""
TensorFlow GPU Benchmark Suite
Tests GPU power, memory bandwidth, compute throughput, and other GPU-related factors.
This program requires a CUDA-compatible GPU and will NOT fall back to CPU.
"""

import os
import sys
import time
import numpy as np

# Force TensorFlow to use GPU only — disable CPU fallback
os.environ["CUDA_VISIBLE_DEVICES"] = "0"          # Use first GPU
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "1"          # Suppress INFO logs

import tensorflow as tf

# ─────────────────────────────────────────────────────────────
# SETUP / VALIDATION
# ─────────────────────────────────────────────────────────────

def validate_gpu():
    """Ensure at least one GPU is available; abort if not."""
    gpus = tf.config.list_physical_devices("GPU")
    if not gpus:
        print("[FATAL] No GPU detected. This benchmark requires a CUDA-compatible GPU.")
        print("        Install the appropriate CUDA + cuDNN drivers and try again.")
        sys.exit(1)

    print("=" * 65)
    print("  TensorFlow GPU Benchmark Suite")
    print("=" * 65)
    print(f"  TensorFlow version : {tf.__version__}")
    print(f"  GPU(s) found       : {len(gpus)}")
    for i, gpu in enumerate(gpus):
        print(f"    [{i}] {gpu.name}")
    print("=" * 65)

    # Enable memory growth so we don't pre-allocate everything
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)

    return gpus


# ─────────────────────────────────────────────────────────────
# BENCHMARK HELPERS
# ─────────────────────────────────────────────────────────────

def _run_on_gpu(fn, device="/GPU:0"):
    """Run fn() pinned to the GPU device; raise if GPU not available."""
    with tf.device(device):
        return fn()


def print_result(name, value, unit="", width=40):
    print(f"  {name:<{width}} {value:>12.4f}  {unit}")


def separator(title=""):
    if title:
        print(f"\n{'─'*20}  {title}  {'─'*20}")
    else:
        print("─" * 65)


# ─────────────────────────────────────────────────────────────
# TEST 1 — GPU DETECTION & MEMORY INFO
# ─────────────────────────────────────────────────────────────

def test_gpu_info():
    separator("GPU Hardware Info")

    for i, gpu in enumerate(tf.config.list_physical_devices("GPU")):
        details = tf.config.experimental.get_device_details(gpu)
        print(f"\n  GPU {i}: {gpu.name}")
        for k, v in details.items():
            print(f"    {k:<30} {v}")

    # Current memory stats
    mem = tf.config.experimental.get_memory_info("GPU:0")
    print(f"\n  {'Memory current (MB)':<40} {mem['current'] / 1024**2:>12.2f}  MB")
    print(f"  {'Memory peak (MB)':<40} {mem['peak'] / 1024**2:>12.2f}  MB")


# ─────────────────────────────────────────────────────────────
# TEST 2 — RAW COMPUTE: FP32 TFLOPS
# ─────────────────────────────────────────────────────────────

def test_fp32_throughput(size=8192, iterations=20):
    separator("FP32 Matrix Multiply Throughput (TFLOPS)")

    def bench():
        A = tf.random.normal([size, size], dtype=tf.float32)
        B = tf.random.normal([size, size], dtype=tf.float32)

        # Warm-up
        for _ in range(3):
            tf.linalg.matmul(A, B)

        start = time.perf_counter()
        for _ in range(iterations):
            C = tf.linalg.matmul(A, B)
        _ = C.numpy()   # Force execution
        elapsed = time.perf_counter() - start
        return elapsed

    elapsed = _run_on_gpu(bench)
    # FLOPs for one matmul: 2 * N^3
    flops = 2 * (size ** 3) * iterations
    tflops = flops / elapsed / 1e12
    print_result(f"FP32 {size}x{size} matmul × {iterations}", tflops, "TFLOPS")


# ─────────────────────────────────────────────────────────────
# TEST 3 — FP16 (HALF PRECISION) THROUGHPUT
# ─────────────────────────────────────────────────────────────

def test_fp16_throughput(size=8192, iterations=20):
    separator("FP16 Matrix Multiply Throughput (TFLOPS)")

    def bench():
        A = tf.random.normal([size, size], dtype=tf.float16)
        B = tf.random.normal([size, size], dtype=tf.float16)

        for _ in range(3):
            tf.linalg.matmul(A, B)

        start = time.perf_counter()
        for _ in range(iterations):
            C = tf.linalg.matmul(A, B)
        _ = C.numpy()
        return time.perf_counter() - start

    elapsed = _run_on_gpu(bench)
    flops = 2 * (size ** 3) * iterations
    tflops = flops / elapsed / 1e12
    print_result(f"FP16 {size}x{size} matmul × {iterations}", tflops, "TFLOPS")


# ─────────────────────────────────────────────────────────────
# TEST 4 — MEMORY BANDWIDTH
# ─────────────────────────────────────────────────────────────

def test_memory_bandwidth(tensor_gb=1.0, iterations=10):
    separator("GPU Memory Bandwidth")

    n_elements = int(tensor_gb * 1024**3 / 4)   # float32 = 4 bytes

    def bench():
        src = tf.random.normal([n_elements], dtype=tf.float32)
        _ = src.numpy()  # ensure allocated

        start = time.perf_counter()
        for _ in range(iterations):
            dst = tf.identity(src)
        _ = dst.numpy()
        return time.perf_counter() - start

    elapsed = _run_on_gpu(bench)
    bytes_transferred = tensor_gb * 1024**3 * iterations * 2  # read + write
    bandwidth_gb_s = bytes_transferred / elapsed / 1024**3
    print_result(f"Bandwidth ({tensor_gb:.0f} GB tensor × {iterations})", bandwidth_gb_s, "GB/s")


# ─────────────────────────────────────────────────────────────
# TEST 5 — ELEMENT-WISE OPS (GPU UTILISATION)
# ─────────────────────────────────────────────────────────────

def test_elementwise_ops(n=50_000_000, iterations=50):
    separator("Element-Wise Op Throughput (GOPS)")

    def bench():
        x = tf.random.normal([n], dtype=tf.float32)
        _ = x.numpy()

        start = time.perf_counter()
        for _ in range(iterations):
            x = tf.math.sin(x) + tf.math.cos(x) * tf.math.tanh(x)
        _ = x.numpy()
        return time.perf_counter() - start

    elapsed = _run_on_gpu(bench)
    # sin + cos + tanh + * + + ≈ 5 ops per element
    total_ops = n * iterations * 5
    gops = total_ops / elapsed / 1e9
    print_result(f"sin+cos+tanh ({n//1_000_000}M elements × {iterations})", gops, "GOPS")


# ─────────────────────────────────────────────────────────────
# TEST 6 — DEEP LEARNING INFERENCE SPEED (ResNet-style conv)
# ─────────────────────────────────────────────────────────────

def test_conv_throughput(batch=64, iterations=100):
    separator("Convolution Layer Throughput (images/sec)")

    def bench():
        # Simulate a ResNet block: 224×224 image, 64 filters
        x = tf.random.normal([batch, 224, 224, 3], dtype=tf.float32)
        conv = tf.keras.layers.Conv2D(64, 3, padding="same", use_bias=False)
        bn   = tf.keras.layers.BatchNormalization()

        # Build layers
        _ = bn(conv(x), training=False)

        start = time.perf_counter()
        for _ in range(iterations):
            y = bn(conv(x), training=False)
        _ = y.numpy()
        return time.perf_counter() - start

    elapsed = _run_on_gpu(bench)
    imgs_per_sec = (batch * iterations) / elapsed
    print_result(f"Conv2D 224×224×3→64 (batch={batch} × {iterations})", imgs_per_sec, "images/s")


# ─────────────────────────────────────────────────────────────
# TEST 7 — MIXED PRECISION (TF AMP)
# ─────────────────────────────────────────────────────────────

def test_mixed_precision(size=8192, iterations=20):
    separator("Mixed Precision (AMP) Throughput (TFLOPS)")

    tf.keras.mixed_precision.set_global_policy("mixed_float16")

    def bench():
        A = tf.cast(tf.random.normal([size, size]), tf.float16)
        B = tf.cast(tf.random.normal([size, size]), tf.float16)

        for _ in range(3):
            tf.linalg.matmul(A, B)

        start = time.perf_counter()
        for _ in range(iterations):
            C = tf.linalg.matmul(A, B)
        _ = C.numpy()
        return time.perf_counter() - start

    elapsed = _run_on_gpu(bench)
    tf.keras.mixed_precision.set_global_policy("float32")   # reset

    flops = 2 * (size ** 3) * iterations
    tflops = flops / elapsed / 1e12
    print_result(f"AMP {size}x{size} matmul × {iterations}", tflops, "TFLOPS")


# ─────────────────────────────────────────────────────────────
# TEST 8 — GPU TEMPERATURE & UTILISATION (via nvidia-smi)
# ─────────────────────────────────────────────────────────────

def test_gpu_smi_stats():
    separator("nvidia-smi GPU Stats")

    result = os.popen(
        "nvidia-smi --query-gpu=name,temperature.gpu,utilization.gpu,"
        "utilization.memory,memory.total,memory.free,memory.used,"
        "power.draw,power.limit,clocks.current.graphics,clocks.current.memory "
        "--format=csv,noheader,nounits 2>&1"
    ).read().strip()

    if not result or "not found" in result.lower() or "error" in result.lower():
        print("  nvidia-smi not available on this system.")
        return

    fields = [f.strip() for f in result.split(",")]
    labels = [
        "GPU Name", "Temperature (°C)", "GPU Utilisation (%)",
        "Memory Utilisation (%)", "Total VRAM (MB)", "Free VRAM (MB)",
        "Used VRAM (MB)", "Power Draw (W)", "Power Limit (W)",
        "Graphics Clock (MHz)", "Memory Clock (MHz)"
    ]
    for label, value in zip(labels, fields):
        print(f"  {label:<35} {value}")


# ─────────────────────────────────────────────────────────────
# TEST 9 — TENSOR CORE DETECTION (via policy)
# ─────────────────────────────────────────────────────────────

def test_tensor_cores():
    separator("Tensor Core / XLA Info")

    details = tf.config.experimental.get_device_details(
        tf.config.list_physical_devices("GPU")[0]
    )
    compute = details.get("compute_capability", (0, 0))
    major, minor = compute if isinstance(compute, tuple) else (compute, 0)

    print(f"  Compute Capability : {major}.{minor}")
    if major >= 7:
        print("  Tensor Cores       : YES (Volta+ architecture)")
    elif major >= 6:
        print("  Tensor Cores       : NO  (Pascal architecture — no Tensor Cores)")
    else:
        print("  Tensor Cores       : NO  (older architecture)")

    # XLA JIT status
    xla = tf.config.optimizer.get_jit()
    print(f"  XLA JIT enabled    : {bool(xla)}")


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    gpus = validate_gpu()

    test_gpu_info()
    test_fp32_throughput()
    test_fp16_throughput()
    test_memory_bandwidth()
    test_elementwise_ops()
    test_conv_throughput()
    test_mixed_precision()
    test_gpu_smi_stats()
    test_tensor_cores()

    separator()
    print("  Benchmark complete!")
    separator()


if __name__ == "__main__":
    main()