#include <_stdio.h>
#include <errno.h>
#include <limits.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/syslimits.h>
#include <sys/types.h>

#define MAXCHAR 1000
#define DEFAULT_PACE 25

typedef struct {
  char *progressive_frame;
  char *top_field_first;
  char *repeat_first_field;
  char *frame_period;
} RowCSV;

// Source - https://stackoverflow.com/a/28879929
// Posted by alk, modified by community. See post 'Timeline' for change history
// Retrieved 2026-11-12, License - CC BY-SA 3.0

int mkdirr(const char *path, const mode_t mode, const int fail_on_exist) {
  int result = 0;
  char *dir = NULL;

  do {
    if (NULL == path) {
      errno = EINVAL;
      result = -1;
      break;
    }

    if ((dir = strrchr(path, '/'))) {
      *dir = '\0';
      result = mkdirr(path, mode, fail_on_exist);
      *dir = '/';

      if (result) {
        break;
      }
    }

    if (strlen(path)) {
      if ((result = mkdir(path, mode))) {
        char s[PATH_MAX];
        snprintf(s, PATH_MAX, "mkdir() failed for '%s'", path);
        perror(s);

        if ((EEXIST == result) && (0 == fail_on_exist)) {
          result = 0;
        } else {
          break;
        }
      }
    }
  } while (0);

  return result;
}

bool get_arguments(int argc, char **argv, char **in, char **out,
                   char **deinterlace_mode) {

  if (argc < 2) {
    fprintf(stderr, "You must have at least 2 arguments.");
    return false;
  }

  int i = 1;
  while (i < argc) {
    char *arg = argv[i++];
    if (strcmp(arg, "--in") == 0) {
      *in = argv[i++];
      continue;
    } else if (strcmp(arg, "--out") == 0) {
      *out = argv[i++];
      continue;
    } else if (strcmp(arg, "--deinterlace_mode") == 0) {
      *deinterlace_mode = argv[i++];
      continue;
    } else {
      fprintf(stderr, "%s is not a valide argument.", arg);
      return false;
    }
  }

  return true;
}

int main(int argc, char **argv) {

  char *in = NULL;
  char *out = NULL;
  char *deinterlace_mode = NULL;

  if (!get_arguments(argc, argv, &in, &out, &deinterlace_mode)) {
    exit(EXIT_FAILURE);
  }

  printf("in: %s\nout: %s\ndeinterlace_mode: %s\n", in, out, deinterlace_mode);

  if (out != NULL) {
    if (mkdirr(out, 0777, 0) == -1) {
      fprintf(stderr, "Can not create the output directory.");
    }
  }

  char *logs_file = strcat(in, "/logs.csv");

  printf("logs file: %s\n", logs_file);

  FILE *fp1;
  int count = 0;
  char c;

  fp1 = fopen(logs_file, "r");

  if (fp1 == NULL) {
    printf("Could not open file %s", logs_file);
    return 0;
  }

  for (c = getc(fp1); c != EOF; c = getc(fp1))
    if (c == '\n')
      count = count + 1;

  fclose(fp1);

  FILE *fp;
  char row[MAXCHAR];
  char *token;
  char *csv_matrix[count][4];

  fp1 = fopen(logs_file, "rb");

  while (feof(fp1) != true) {
    fgets(row, MAXCHAR, fp1);
    printf("Row: %s", row);

    token = strtok(row, ";");

    while (token != NULL) {
      printf("Token: %s\n", token);
      token = strtok(NULL, ";");
    }
  }

  return 0;
}
