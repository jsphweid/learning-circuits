#include <stdio.h>
#include <time.h>

// NOTE: can't be bothered to learn how to do this with minimal code duplication in C for now

/*
Results:
  These tests were so much faster than python I had add two more orders of magnitude
  to the test lengths...

  I kept seeing almost no differences until I added this global variable. I believe
  the compiler was just removing the line of code before that since it was deemed "useless"
*/

int result;

double runConventionalTests(int numTests)
{
  clock_t t;
  t = clock();
  for (int i = 0; i < numTests; i++)
  {
    result = i % 2;
  }
  t = clock() - t;
  return ((double)t) / CLOCKS_PER_SEC;
}

double runBitwiseTests(int numTests)
{
  clock_t t;
  t = clock();
  for (int i = 0; i < numTests; i++)
  {
    result = i & 1;
  }
  t = clock() - t;
  return ((double)t) / CLOCKS_PER_SEC;
}

int main()
{
  int iterations[7] = {1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000};

  for (int i = 0; i < 7; i++)
  {

    int numIterations = iterations[i];

    double conventionalTestTime = runConventionalTests(numIterations);
    printf("conventionalTestTime() took %f seconds to execute %d iterations\n", conventionalTestTime, numIterations);

    double bitwiseTestTime = runBitwiseTests(numIterations);
    printf("bitwiseTestTime() took %f seconds to execute %d iterations\n", bitwiseTestTime, numIterations);
  }
  return 0;
}