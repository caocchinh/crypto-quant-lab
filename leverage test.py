
def reverse_engineer_original_amount(borrowed_amount, multiplier):
    original_amount = (borrowed_amount / multiplier )
    return original_amount

# Example usage
borrowed_amount_ftm = 10.746928312146009
borrowed_amount_near = 8.060196234109506
borrowed_amount_op = 8.060196234109506
multiplier_ftm = 5.0
multiplier_near = 1.0
multiplier_op = 5.0
allowance = 8.98

original_amount_ftm = reverse_engineer_original_amount(borrowed_amount_ftm, multiplier_ftm, allowance )
original_amount_near = reverse_engineer_original_amount(borrowed_amount_near, multiplier_near, allowance )
original_amount_op = reverse_engineer_original_amount(borrowed_amount_op, multiplier_op, allowance)

print("Original Amount for FTMUSDT:", original_amount_ftm)
print("Original Amount for NEARUSDT:", original_amount_near)
print("Original Amount for OPUSDT:", original_amount_op)
