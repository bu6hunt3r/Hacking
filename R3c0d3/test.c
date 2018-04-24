#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <stdint.h>

#define MAXOPSIZE 4

int main(int argc, char **argv) {
    char source[MAXOPSIZE+1];
    FILE *f=fopen("imp.rco","r");
    if(f != NULL)  {
        size_t newlen=fread(source, sizeof(char), MAXOPSIZE, f);
        if(ferror(f)!=0) {
            fputs("Reading error from file\n",stderr);
        } else {
            source[newlen++]="\0";
        }
    fclose(f);

    uint8_t b[4];
    b[0]=source[3];
    b[1]=source[2];
    b[2]=source[1];
    b[3]=source[0];
    printf("Buffer is %s\n", source);
    printf("Char 0 -> %x\n", b[0]);
    printf("Char 1 -> %x\n", b[1]);
    printf("Char 2 -> %x\n", b[2]);
    printf("Char 3 -> %x\n", b[3]);

    uint32_t opcode=*(uint32_t*)b;

    printf("Opcode is 0x%x", opcode);
    return EXIT_SUCCESS;
    }
}