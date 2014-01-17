#include <pthread.h>
#include <stdio.h>
int global_increment = 0;
void *inc_global()
{
     for (int i=0; i<1000000; ++i)
          global_increment++;
     return NULL;

}


int main() {

     pthread_t increment_global;

     if(pthread_create(&increment_global, NULL, inc_global, NULL)) {
          fprintf(stderr, "Error creating thread 1\n");
          return 1;
     }

     for (int i=0; i<1000000; ++i)
          global_increment--;

     if(pthread_join(increment_global, NULL)) {
          fprintf(stderr, "Error joining thread 1\n");
          return 2;
     }

     printf("global = %d\n", global_increment);
     
     return 0;
}

