import sys
import time

# Message to be deleted and printed again
message = "Hello, World!"

# Print the message
sys.stdout.write(message)
sys.stdout.flush()

# Wait for a few seconds
time.sleep(2)

# Delete the message by printing backspaces
sys.stdout.write('\b' * len(message))
sys.stdout.flush()

# Print the message again
sys.stdout.write(message)
sys.stdout.flush()
