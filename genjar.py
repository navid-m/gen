import os
import sys


def generate_script(jar_path):
    jar_abs_path = os.path.abspath(jar_path)
    jar_name = os.path.basename(jar_abs_path)
    shortened_name = jar_name.split('-')[0].replace(".jar", "")
    command = f"java --add-opens=java.base/java.lang=ALL-UNNAMED -jar {
        jar_abs_path} %* \n"

    if os.name == 'nt':
        script_name = f"{shortened_name}.cmd"
        with open(script_name, 'w') as script_file:
            script_file.write(f"@echo off\n{command}")
    else:
        script_name = f"{shortened_name}.sh"
        with open(script_name, 'w') as script_file:
            script_file.write(f"#!/bin/bash\n{command}")
        os.chmod(script_name, 0o755)

    print(f"Generated: {script_name}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: genjar <path_to_jar>")
    else:
        jar_path = sys.argv[1]
        generate_script(jar_path)
