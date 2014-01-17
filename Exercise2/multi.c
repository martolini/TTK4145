#include <pthread.h>
#include <stdio.h>
#include <semaphore.h>

int global_increment = 0;
sem_t mutex;


void *inc_global()
{
     for (int i=0; i<10000; ++i) {
          sem_wait(&mutex);
          printf("Incrementing, global was %i\n", global_increment);
          int a = global_increment;
          a += 1;
          global_increment = a;
          printf("Incrementing, global is %i\n", global_increment);
          sem_post(&mutex);
     }
     return NULL;

}

void *dec_global() {
     for (int i=0; i<10001; ++i) {
          sem_wait(&mutex);
          printf("Decrementing, global was %i\n", global_increment);
          int a = global_increment;
          a -= 1;
          global_increment = a;
          printf("Incrementing, global is %i\n", global_increment);
          sem_post(&mutex);
     }
     return NULL;
}


int main() {

     sem_init(&mutex, 1, 0);

     pthread_t increment_global;
     pthread_t decrement_global;

     pthread_create(&increment_global, NULL, inc_global, NULL);
     pthread_create(&decrement_global, NULL, dec_global, NULL);

     pthread_join(increment_global, NULL);
     pthread_join(decrement_global, NULL);

     sem_destroy(&mutex);

     printf("global = %d\n", global_increment);
     
     return 0;
}

