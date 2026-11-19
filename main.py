import math

def simulate_upscale_job(job_id, input_width, input_height, upscale_factor):
    """
    Simulates an upscaling job, calculating input/output pixels and a processing cost.
    The processing cost is directly tied to the output pixel count, reflecting the
    computational load of generating a larger image.
    """
    input_pixels = input_width * input_height
    output_width = input_width * upscale_factor
    output_height = input_height * upscale_factor
    output_pixels = output_width * output_height

    # The core concept: processing cost is primarily driven by the output size.
    # We simulate 1 unit of cost per million output pixels.
    processing_cost = output_pixels / 1_000_000.0

    return {
        "id": job_id,
        "input_dim": f"{input_width}x{input_height}",
        "input_pixels": input_pixels,
        "upscale_factor": f"{upscale_factor}x",
        "output_dim": f"{output_width}x{output_height}",
        "output_pixels": output_pixels,
        "processing_cost": processing_cost,
    }

# Define a set of sample upscaling jobs with varying characteristics
jobs_data = [
    (1, 100, 100, 2),   # Small input, small upscale -> small output
    (2, 50, 50, 10),    # Very small input, large upscale -> medium output
    (3, 1920, 1080, 1), # HD input, no upscale -> HD output (baseline)
    (4, 300, 200, 8),   # Medium input, large upscale -> large output
    (5, 64, 64, 64),    # Tiny input, massive upscale -> very large output (e.g., icon to 4K)
    (6, 1280, 720, 2),  # HD input, 2x upscale -> 4K output
]

all_jobs = [simulate_upscale_job(*job) for job in jobs_data]

print("--- Upscaling Job Analysis ---")
print(f"{'ID':<3} | {'Input Dim':<12} | {'Input Pixels (M)':<18} | {'Factor':<8} | {'Output Dim':<12} | {'Output Pixels (M)':<18} | {'Cost (Units)':<12}")
print("-" * 100)

for job in all_jobs:
    print(
        f"{job['id']:<3} | "
        f"{job['input_dim']:<12} | "
        f"{job['input_pixels']/1_000_000.0:<18.2f} | "
        f"{job['upscale_factor']:<8} | "
        f"{job['output_dim']:<12} | "
        f"{job['output_pixels']/1_000_000.0:<18.2f} | "
        f"{job['processing_cost']:<12.2f}"
    )

print("\n--- Routing Strategy Comparison ---")

# Strategy 1: Naive routing based on INPUT PIXELS
# This often leads to misallocation as input size doesn't reflect processing load.
print("\nStrategy 1: Routing based on INPUT PIXELS (Naive/Misleading)")
light_server_input_jobs = []
heavy_server_input_jobs = []
input_threshold_pixels = 100_000  # Jobs with input < 0.1M pixels go to 'Light Server'

for job in all_jobs:
    if job['input_pixels'] < input_threshold_pixels:
        light_server_input_jobs.append(job)
    else:
        heavy_server_input_jobs.append(job)

print(f"  Jobs routed to 'Light Server' (Input < {input_threshold_pixels/1_000_000:.1f}M pixels):")
for job in light_server_input_jobs:
    print(f"    - Job {job['id']} (Input: {job['input_pixels']/1_000_000:.2f}M, Output: {job['output_pixels']/1_000_000:.2f}M, Cost: {job['processing_cost']:.2f})")
# Summing costs reveals the potential imbalance
total_cost_light_input = sum(j['processing_cost'] for j in light_server_input_jobs)
print(f"  Total processing cost for 'Light Server' (input-based): {total_cost_light_input:.2f} units")

print(f"\n  Jobs routed to 'Heavy Server' (Input >= {input_threshold_pixels/1_000_000:.1f}M pixels):")
for job in heavy_server_input_jobs:
    print(f"    - Job {job['id']} (Input: {job['input_pixels']/1_000_000:.2f}M, Output: {job['output_pixels']/1_000_000:.2f}M, Cost: {job['processing_cost']:.2f})")
total_cost_heavy_input = sum(j['processing_cost'] for j in heavy_server_input_jobs)
print(f"  Total processing cost for 'Heavy Server' (input-based): {total_cost_heavy_input:.2f} units")

# Strategy 2: Recommended routing based on OUTPUT PIXELS / PROCESSING COST
# This strategy accurately reflects the actual workload.
print("\nStrategy 2: Routing based on OUTPUT PIXELS / PROCESSING COST (Recommended)")
light_server_output_jobs = []
heavy_server_output_jobs = []
cost_threshold = 1.0  # Jobs with processing cost < 1.0 units go to 'Light Server'

for job in all_jobs:
    # This is the crucial part: routing decisions are based on the estimated actual work (cost)
    if job['processing_cost'] < cost_threshold:
        light_server_output_jobs.append(job)
    else:
        heavy_server_output_jobs.append(job)

print(f"  Jobs routed to 'Light Server' (Cost < {cost_threshold:.1f} units):")
for job in light_server_output_jobs:
    print(f"    - Job {job['id']} (Input: {job['input_pixels']/1_000_000:.2f}M, Output: {job['output_pixels']/1_000_000:.2f}M, Cost: {job['processing_cost']:.2f})")
total_cost_light_output = sum(j['processing_cost'] for j in light_server_output_jobs)
print(f"  Total processing cost for 'Light Server' (output-based): {total_cost_light_output:.2f} units")

print(f"\n  Jobs routed to 'Heavy Server' (Cost >= {cost_threshold:.1f} units):")
for job in heavy_server_output_jobs:
    print(f"    - Job {job['id']} (Input: {job['input_pixels']/1_000_000:.2f}M, Output: {job['output_pixels']/1_000_000:.2f}M, Cost: {job['processing_cost']:.2f})")
total_cost_heavy_output = sum(j['processing_cost'] for j in heavy_server_output_jobs)
print(f"  Total processing cost for 'Heavy Server' (output-based): {total_cost_heavy_output:.2f} units")

print("\n--- Key Takeaway ---")
print("Observe Job 4 (300x200 to 2400x1600) and Job 5 (64x64 to 4096x4096). These jobs have very small input pixel counts,")
print("but result in significantly large output pixel counts and thus high processing costs. A naive routing strategy")
print("based solely on input size would incorrectly classify them as 'light' jobs, potentially overloading servers.")
print("Routing based on estimated output size or processing cost provides a more accurate and balanced distribution of workload.")
