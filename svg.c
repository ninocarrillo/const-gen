#include "svg.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>


void ConstellationSVG(int16_t *symbol, int count) {
    FILE *svg;
    char work_string[100];
    snprintf(work_string, sizeof(work_string), "svg/const-%i.svg", count);
    svg = fopen(work_string, "w");
    if (svg == NULL) {
        printf("Could not create %s.\r\n", work_string);
    } else {
        // Make an SVG viewbox
        int16_t uc_rad = 32767;
        int xdim = 72000;
        int ydim = 72000;
        snprintf(work_string, sizeof(work_string), "%i, %i, %i, %i", /* xmin */-(xdim/2), /* ymin */ -(ydim/2), /* width */ xdim, /* height */ ydim);
        fprintf(svg, "<svg xmlns='http://www.w3.org/2000/svg' viewBox='%s'>\r\n", work_string);
		// Add some text
        int text_size = 1500;
        int text_line_int = 1.5 * text_size;
        int text_x = -32767;
        int text_y = -32767 + text_size;
        snprintf(work_string, sizeof(work_string), "x='%i' y='%i' font-size='%i'", text_x, text_y, text_size);
        fprintf(svg, " <text %s font-family='Arial, sans-serif' fill='black'>", work_string);
        fprintf(svg, "Constellation Size %i", count);
        fprintf(svg, " </text>\r\n");
        text_y += text_line_int;
        snprintf(work_string, sizeof(work_string), "x='%i' y='%i' font-size='%i'", text_x, text_y, text_size);
        fprintf(svg, " <text %s font-family='Arial, sans-serif' fill='black'>", work_string);
        fprintf(svg, "Odd Points Filled");
        fprintf(svg, " </text>\r\n");
        text_y += text_line_int;
        // Draw the constellation unit circle
        fprintf(svg, " <circle stroke='gray' stroke-width='100' r='%i' fill='none' opacity='0.25'>\r\n", uc_rad);
		fprintf(svg, "  <title>Constellation Unit Circle Radius %i</title>\r\n", uc_rad);
		fprintf(svg, " </circle>\r\n");
        // Draw the real axis
        fprintf(svg, " <line stroke='gray' stroke-width='100' x1='%i' y1='%i' x2='%i' y2='%i' fill='none' opacity='0.25'>\r\n", -32768, 0, 32768, 0);
		fprintf(svg, "  <title>Constellation Real Axis Size %i</title>\r\n", 65536);
		fprintf(svg, " </line>\r\n");
        // Label the real axis
        text_x = (xdim/2);
        text_y = text_size / 2;
        snprintf(work_string, sizeof(work_string), "x='%i' y='%i' font-family='courier' font-size='%i' fill='black'", text_x, text_y, text_size);
        fprintf(svg, " <text %s>", work_string);
        fprintf(svg, "I");
        fprintf(svg, " </text>\r\n");

        // Draw the imag axis
        fprintf(svg, " <line stroke='gray' stroke-width='100' x1='%i' y1='%i' x2='%i' y2='%i' fill='none' opacity='0.25'>\r\n", 0, -32768, 0, 32768);
		fprintf(svg, "  <title>Constellation Imag Axis Size %i</title>\r\n", 65536);
		fprintf(svg, " </line>\r\n");
        // Label the imag axis
        text_x = text_size / 2;
        text_y = text_size-(ydim/2);
        snprintf(work_string, sizeof(work_string), "x='%i' y='%i' font-family='courier' font-size='%i' fill='black'", text_x, text_y, text_size);
        fprintf(svg, " <text %s>", work_string);
        fprintf(svg, "Q");
        fprintf(svg, " </text>\r\n");


        int16_t marker_size = 500;
        int16_t stroke_width = 200;
        for (int i = 0; i < count; i++) {
            int ii = i<<1;
			// SVG graphics treat the y-axis as low values at top, so invert y axis for I/Q plot
            if (i & 1) {
                // Odd index
                snprintf(work_string, sizeof(work_string), "stroke='black' fill='black' stroke-width='%i' cx='%i' cy='%i' r='%i' opacity='1.0'", stroke_width, /* cx */symbol[ii], /* cy */ -symbol[ii+1], marker_size);
                fprintf(svg, "  <circle %s>\r\n", work_string);
                fprintf(svg, "   <title>%i (%i, %i)</title>\r\n", i, symbol[ii], symbol[ii+1]);
    			fprintf(svg, "  </circle>\r\n");
            } else {
                // Even index
                snprintf(work_string, sizeof(work_string), "stroke='black' fill='white' stroke-width='%i' cx='%i' cy='%i' r='%i' opacity='1.0'", stroke_width, /* cx */symbol[ii], /* cy */ -symbol[ii+1], marker_size);
                fprintf(svg, "  <circle %s>\r\n", work_string);
                fprintf(svg, "   <title>%i (%i, %i)</title>\r\n", i, symbol[ii], symbol[ii+1]);
                fprintf(svg, "  </circle>\r\n");
            }

            // Add some text
            int text_size = marker_size*1.5;
            int text_line_int = marker_size*1.5;
            int text_x = symbol[ii];
            int text_y = -symbol[ii+1] + (1.6*text_line_int);
            snprintf(work_string, sizeof(work_string), "x='%i' y='%i' font-size='%i'", text_x, text_y, text_size);
            fprintf(svg, " <text %s font-family='Arial, sans-serif' fill='black'>", work_string);
            fprintf(svg, "%i", i);
            fprintf(svg, " </text>\r\n");
            text_y += text_line_int;
            snprintf(work_string, sizeof(work_string), "x='%i' y='%i' font-size='%i'", text_x, text_y, text_size);
            fprintf(svg, " <text %s font-family='Arial, sans-serif' fill='black'>", work_string);
            fprintf(svg, "%i", symbol[ii]);
            fprintf(svg, " </text>\r\n");
            text_y += text_line_int;
            snprintf(work_string, sizeof(work_string), "x='%i' y='%i' font-size='%i'", text_x, text_y, text_size);
            fprintf(svg, " <text %s font-family='Arial, sans-serif' fill='black'>", work_string);
            fprintf(svg, "%i", symbol[ii+1]);
            fprintf(svg, " </text>\r\n");
        }
        fprintf(svg, "</svg>\r\n");
    }
    fclose(svg);
}
