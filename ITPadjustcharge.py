# Load and process the file, round col 7 to 3 decimals, and adjust the top 5 positive & top 5 negative values
# so that the sum of the (rounded-to-3dp) 7th column is exactly zero, with each adjustment < 0.002.
from decimal import Decimal, ROUND_HALF_UP, getcontext
import pandas as pd
from caas_jupyter_tools import display_dataframe_to_user

getcontext().prec = 28  # high precision for safety

path = "test.txt"

# Read as whitespace-delimited to handle variable tabs
df = pd.read_csv(path, sep=r"\s+", header=None, engine="python")

# Ensure we have at least 7 columns (0-indexed col 6 is our target)
if df.shape[1] < 7:
    raise ValueError("File does not have at least 7 columns.")

# Convert column 6 to Decimal
def to_dec(x):
    try:
        return Decimal(str(x))
    except Exception:
        return Decimal("0")

col7 = df[6].apply(to_dec)

# Round to 3 decimals (bankers not wanted -> use ROUND_HALF_UP)
def round3(d: Decimal) -> Decimal:
    return d.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)

rounded = col7.apply(round3)

# Compute needed correction to make sum zero in 0.001 steps
sum_before = sum(rounded)
needed = -sum_before  # target addition to reach zero
# Convert to integer steps of 0.001 to avoid float issues
step = Decimal("0.001")
steps_needed = int((needed / step).to_integral_value(rounding=ROUND_HALF_UP))

# Identify top 5 positive and top 5 negative by value after rounding
# (If there are ties, pandas will pick by order of appearance.)
pos_idx = rounded.sort_values(ascending=False).head(5).index.tolist()
neg_idx = rounded.sort_values(ascending=True).head(5).index.tolist()
targets = pos_idx + neg_idx

# Each target can be adjusted at most 2 steps of 0.001 (i.e., < 0.002 in magnitude)
max_steps_per_target = 2

adjustments = {i: Decimal("0.000") for i in range(len(df))}
capacity = len(targets) * max_steps_per_target

# If the needed steps exceed capacity, cap and note infeasibility
feasible = abs(steps_needed) <= capacity

# Distribute steps round-robin among targets with sign = sign(steps_needed)
def sign(x): 
    return -1 if x < 0 else (1 if x > 0 else 0)

remaining = steps_needed
# We adjust the total upward if remaining > 0 (add +0.001),
# or downward if remaining < 0 (add -0.001)
if feasible:
    per_target_counts = {idx: 0 for idx in targets}
    sgn = sign(remaining)
    # Round-robin allocation
    while remaining != 0:
        for idx in targets:
            if remaining == 0:
                break
            if per_target_counts[idx] < max_steps_per_target:
                adjustments[idx] += step * sgn
                per_target_counts[idx] += 1
                remaining -= sgn
else:
    # Best-effort: push as close to zero as allowed by constraints
    per_target_counts = {idx: 0 for idx in targets}
    sgn = sign(steps_needed)
    # Apply full capacity in the required direction
    for _ in range(capacity):
        idx = targets[_ % len(targets)]
        adjustments[idx] += step * sgn
        per_target_counts[idx] += 1
    remaining = steps_needed - sgn * capacity

# Apply adjustments
adjusted = rounded.copy()
for idx, delta in adjustments.items():
    if delta != 0:
        adjusted.iloc[idx] = round3(adjusted.iloc[idx] + delta)

sum_after = sum(adjusted)

# Prepare an output DataFrame with adjusted 3dp values
df_out = df.copy()
# Format to exactly 3 decimal places as strings for column 6
df_out[6] = adjusted.apply(lambda d: f"{d:.3f}")

# Save the adjusted file
out_path = "test_adjusted.txt"
# Use tab separation and no header/index
df_out.to_csv(out_path, sep="\t", header=False, index=False)

# Build a small report of changes (only rows that changed)
changes = []
for idx, delta in adjustments.items():
    if delta != 0:
        old = rounded.iloc[idx]
        new = adjusted.iloc[idx]
        changes.append({
            "row": int(df.iloc[idx,0]) if pd.api.types.is_numeric_dtype(df.iloc[:,0]) else idx+1,
            "original_3dp": f"{old:.3f}",
            "delta_applied": f"{delta:.3f}",
            "new_3dp": f"{new:.3f}"
        })

report = pd.DataFrame(changes, columns=["row", "original_3dp", "delta_applied", "new_3dp"]).sort_values("row")

# Display the report and also the first few rows of the adjusted column for verification
display_dataframe_to_user("Adjusted rows (only those modified)", report)

# Prepare a compact summary as a dict to print
summary = {
    "rounded_sum_before": f"{sum_before:.3f}",
    "steps_needed_of_0.001": int((needed / step).to_integral_value(rounding=ROUND_HALF_UP)),
    "feasible_under_<0.002_per_target": feasible,
    "total_adjustment_applied": f"{(sum(adjustments.values())):.3f}",
    "sum_after_adjustment": f"{sum_after:.3f}",
    "remaining_steps_unallocated": int(remaining)
}
