import os
import random


def windscribe(action, location=None):
    windscribe_cli_path = r"C:\\Program Files\\Windscribe\\windscribe-cli.exe"

    if location is None:
        command = f'"{windscribe_cli_path}" {action}'
    else:
        command = f'"{windscribe_cli_path}" {action} {location}'

    os.system(command)


windscribe("connect",random.sample(["crumpets", "Custard", "US", "Zurich", "Toronto", "Vancouver", "Paris", "Frankfurt", "Amsterdam",
 "Fjord", "Bucharest", "Alphorn", "Lindenhof", "Istanbul", "Victoria"],1)[0])


# Disconnect
# windscribe("disconnect")