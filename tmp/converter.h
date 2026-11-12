#ifndef CONVERTER_H
#define CONVERTER_H

#include "image.h"
#include <climits>
#include <stdint.h>
#include <stdio.h>

int clamp(double v);
RGB yuv_to_rgb(int y, int u, int v);
void interpolate_matrix(RGB **matrix, int f_width, int y);
void vec_to_decoded_vec(RGB **final_matrix, uint8_t **matrix, int f_width,
                        int f_height, int y, int h);
RGB **matrix_to_decoded_matrix(uint8_t **matrix, int width, int height);
int matrix_to_decoded_multiple_matrices(uint8_t **matrix, int width, int height,
                                        RGB ***top_field_matrix,
                                        RGB ***bot_field_matrix);
void free_rgb_matrix(RGB **matrix, int height);

#endif // CONVERTER_H
