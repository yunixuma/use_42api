import sys, os, importlib

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0:
        print("Usage: python3 my_launch.py <python_file>")
        sys.exit(1)
    # module_name = args[0]
    mod_name = os.path.splitext(args[0])[0].replace("/", ".")
    try:
        # import module_name
        mod = importlib.import_module(mod_name)
        if hasattr(mod, "wrapper"):
            ret = mod.wrapper(args)
            print(ret)
        else:
            print(f"Error: {mod_name} does not have a 'main' function.")
    except ModuleNotFoundError:
        print(f"Error: Module '{mod_name}' not found.")
