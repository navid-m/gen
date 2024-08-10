import os
import sys

out_name = ""


def generate_script(jar_path):
    global out_name
    jar_abs_path = os.path.abspath(jar_path)
    display_name = os.path.basename(
        jar_abs_pat
    ).split('-')[0].replace(".jar", "")

    command = f"java --add-opens=java.base/java.lang=ALL-UNNAMED -jar {
        jar_abs_path} %* \n"

    if os.name == 'nt':
        out_name = f"{display_name}.cmd"
        with open(out_name, 'w') as script_file:
            script_file.write(f"@echo off\n{command}")
        return

    out_name = f"{display_name}.sh"

    with open(out_name, 'w') as script_file:
        script_file.write(f"#!/bin/bash\n{command}")

    os.chmod(out_name, 0o755)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: genjar <path_to_jar>")
    else:
        jar_path = sys.argv[1]
        if (os.path.exists(jar_path)):
            generate_script(jar_path)
            print(f"Generated: {out_name}")
            raise SystemExit()
        print("Specified JAR does not exist")
