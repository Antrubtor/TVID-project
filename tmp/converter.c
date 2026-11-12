#include "image.h"
#include <errno.h>

int min(int a, int b) {
  if (a <= b)
    return a;
  return b;
}

int max(int a, int b) {
  if (a >= b)
    return b;
  return a;
}

int clamp(float v) { return max(0, min(255, (int)v)); }

void yuv_to_rgb(int y, int u, int v, int *r, int *g, int *b) {
  y -= 16;
  u -= 128;
  v -= 128;

  *r = clamp(1.164 * y + 1.596 * v);
  *g = clamp(1.164 * y - 0.392 * u - 0.813 * v);
  *b = clamp(1.164 * y + 2.017 * u);
}

void interpolate_matrix(RGB **matrix, int f_width, int y) {}

void vec_to_decoded_vec(RGB **final_matrix, uint8_t **matrix, int f_width,
                        int f_height, int y, int h) {}

RGB **matrix_to_decoded_matrix(uint8_t **matrix, int width, int height) {}

int matrix_to_decoded_multiple_matrices(uint8_t **matrix, int width, int height,
                                        RGB ***top_field_matrix,
                                        RGB ***bot_field_matrix) {}

void free_rgb_matrix(RGB **matrix, int height) {}
