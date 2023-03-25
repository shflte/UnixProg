#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>

void search_directory(char *path, char *str) {
    DIR* dir = opendir(path);
    struct dirent *entry;
    struct stat st;
    
    while ((entry = readdir(dir))) {
        char filepath[1000];
        sprintf(filepath, "%s/%s", path, entry->d_name);
        
        if (lstat(filepath, &st)) {
            perror("stat");
            continue;
        }

        if (S_ISDIR(st.st_mode)) {
            if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
                continue;
            }
            search_directory(filepath, str);
        } 
        else if (S_ISREG(st.st_mode)) {
            FILE *fp = fopen(filepath, "r");
            char buf[1000];
            int find = 0;
            
            if (!fp) continue;
            while(fgets(buf, sizeof(buf), fp)) {
                if (strstr(buf, str)) {
                    printf("%s\n", filepath);
                    exit(0);
                }
            }
            
            fclose(fp);
        }
    }
    
    closedir(dir);
}

int main(int argc, char** argv) {
    char path[1000];
    char str[100];

    strcpy(path, argv[1]);
    strcpy(str, argv[2]);
    
    search_directory(path, str);
    
    return 0;
}