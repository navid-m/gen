#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

#ifdef _WIN32
    #include <windows.h>
    #define PATH_MAX 4096
#else
    #include <limits.h>
    #include <unistd.h>
#endif

void generate_script(const char *jar_path) {
    char jar_abs_path[PATH_MAX];
    char jar_name[256];
    char shortened_name[256];
    char command[4196];
    char script_name[260];
    FILE *script_file;

#ifdef _WIN32
    _fullpath(jar_abs_path, jar_path, PATH_MAX);
#else
    realpath(jar_path, jar_abs_path);
#endif

    const char *base_name = strrchr(jar_abs_path, '/');
#ifdef _WIN32
    if (!base_name) {
        base_name = strrchr(jar_abs_path, '\\');
    }
#endif
    if (!base_name) {
        base_name = jar_abs_path;
    } else {
        base_name++;
    }
    strncpy(jar_name, base_name, sizeof(jar_name) - 1);
    char *dash_pos = strchr(jar_name, '-');
    if (dash_pos) {
        strncpy(
            shortened_name, 
            jar_name, 
            dash_pos - jar_name
        );
        shortened_name[dash_pos - jar_name] = '\0';
    } else {
        strncpy(shortened_name, jar_name, sizeof(shortened_name) - 1);
    }
    snprintf(command, sizeof(command), "java -jar %s\n", jar_abs_path);

#ifdef _WIN32
    snprintf(script_name, sizeof(script_name), "%s.cmd", shortened_name);
    script_file = fopen(script_name, "w");
    if (script_file) {
        fprintf(script_file, "@echo off\n%s", command);
        fclose(script_file);
    } else {
        perror("Error creating script file");
        return;
    }
#else
    snprintf(script_name, sizeof(script_name), "%s.sh", shortened_name);
    script_file = fopen(script_name, "w");
    if (script_file) {
        fprintf(script_file, "#!/bin/bash\n%s", command);
        fclose(script_file);
        chmod(script_name, S_IRWXU);
    } else {
        perror("Error creating script file");
        return;
    }
#endif
    printf("Generated: %s\n", script_name);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: genjar <path_to_jar>\n");
        return 1;
    }
    generate_script(argv[1]);
    return 0;
}
