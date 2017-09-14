/*
 * blackngel's original example slightly modified
 */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void fvuln(unsigned long len, char *str, char *buf)
{
  char *ptr1, *ptr2, *ptr3;

  ptr1 = malloc(256);
  printf("PTR1 = [ %p ]\n", ptr1);
  strcpy(ptr1, str);

  printf("Allocated MEM: %lu bytes\n", len);
  ptr2 = malloc(len);
  ptr3 = malloc(256);

  strcpy(ptr3, buf);
}

int main(int argc, char *argv[])
{
  char *pEnd;
  if (argc == 4)
    fvuln(strtoull(argv[1], &pEnd, 10), argv[2], argv[3]);

  return 0;
}
