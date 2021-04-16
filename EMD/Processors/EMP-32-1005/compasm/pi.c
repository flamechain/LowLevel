#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>

double random() {
    return (double)rand() / (double)RAND_MAX;
}

int main() {
    time_t t;
    srand((unsigned) time(&t));

    long samplesize = 100000;
    double points[samplesize][2];

    for (int i=0;i < samplesize; i++) {
        points[i][0] = random();
        points[i][1] = random();
    }

    int in_circle = 0;

    for (int i=0; i < samplesize; i++) {
        if (sqrt(pow(points[i][0], 2) + pow(points[i][1], 2)) < 1) {
            in_circle++;
        }
    }

    double pi = 4 * ((double)in_circle / (double)samplesize);

    printf("%f\n", pi);

    return 0;
}
