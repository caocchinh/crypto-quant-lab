# Given dictionary
portfolio = {
    'ALGOUSDT': {
        'ALGO_Base_USDT_Value': 0.0,
        'ALGO_Base_Value': 0.0,
        'USDT_Quote_Value': 61.89688085,
        'USDT_Total_Value': 61.89688085
    },
    'ARBUSDT': {
        'ARB_Base_USDT_Value': 120.0,
        'ARB_Base_Value': 2.0,
        'USDT_Quote_Value': 41.13002685,
        'USDT_Total_Value': 41.13002685
    },
    # ... (other entries)
}

# Extract the part of the key up to the underscore for keys that match the pattern
result = {key: {"quote": {k.split('_')[0]: v for k, v in value.items() if k.endswith('_Total_Value')},
                "base": {k.split('_')[0]: v for k, v in value.items() if k.endswith('_Base_Value')}}
          for key, value in portfolio.items()}

# Display the result
print(result)
