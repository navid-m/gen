import os
import sys


def generate_script(jar_path):
    jar_abs_path = os.path.abspath(jar_path)
    display_name = os.path.splitext(
        os.path.basename(
            jar_abs_path
        )
    )[0].split('-')[0]

    cmnd = f"java --add-opens=java.base/java.lang=ALL-UNNAMED -jar {
        jar_abs_path} %*\n"

    sc = f"@echo off\n{cmnd}" if os.name == 'nt' else f"#!/bin/bash\n{cmnd}"
    out_name = f"{display_name}.{'cmd' if os.name == 'nt' else 'sh'}"

    with open(out_name, 'w') as sc_file:
        sc_file.write(sc)

    if os.name != 'nt':
        os.chmod(out_name, 0o755)

    return out_name


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: genjar <path_to_jar>")
        sys.exit(1)

    jar_path = sys.argv[1]
    if os.path.exists(jar_path):
        out_name = generate_script(jar_path)
        print(f"Generated: {out_name}")
    else:
        print("Specified JAR does not exist")
        sys.exit(1)
