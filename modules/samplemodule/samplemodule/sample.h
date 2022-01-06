#ifndef SAMPLE_H
#define SAMPLE_H

#include "pandabase.h"


BEGIN_PUBLISH // This exposes all functions in this block to python

inline int multiply(int a, int b) {
    return a * b;
}

END_PUBLISH


class SampleClass {
    PUBLISHED: // Exposes all functions in this scope, use instead of "public:"
        inline int get_answer() {
            return 42;
        };
};


#endif SAMPLE_H
