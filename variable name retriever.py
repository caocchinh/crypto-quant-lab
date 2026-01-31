import inspect

x, y, z = 1, 2, 3

def retrieve_name(var):
    return [var_name for var_name, var_val in inspect.currentframe().f_back.f_locals.items() if var_val is var][0]

print(retrieve_name(y))