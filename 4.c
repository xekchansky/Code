#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>

struct Mythread
{
    int iterations;
    int first;
    double addfirst;
    int second;
    double addsecond;
    double *accounts;
    pthread_mutex_t *mutexes;
};

void *routine(void *ptr) {
    struct Mythread thr = *(struct Mythread *)ptr;
    for (int i = 0; i < thr.iterations; ++i) {
        pthread_mutex_lock(&thr.mutexes[thr.first]);
        pthread_mutex_lock(&thr.mutexes[thr.second]);
    
        //printf("%.10g %.10g", thr.accounts[thr.first], thr.addfirst);
        //printf("%.10g %.10g", thr.accounts[thr.second], thr.addsecond);
        thr.accounts[thr.first] += thr.addfirst;
        thr.accounts[thr.second] += thr.addsecond;
        //printf("%.10g %.10g", thr.accounts[thr.first], thr.accounts[thr.second]);

        pthread_mutex_unlock(&thr.mutexes[thr.first]);
        pthread_mutex_unlock(&thr.mutexes[thr.second]);
    }
    return NULL;
}

int swap_prop_acc(struct Mythread *prop) {
    int b = prop->first;
    double bd = prop->addfirst;
    //printf("%d %d\n", prop->first, prop->second);
    prop->first = prop->second;
    prop->addfirst = prop->addsecond;
    prop->second = b;
    prop->addsecond = bd;
    //printf("%d %d\n", prop->first, prop->second);
    return 0;
}


int main() {
    //printf("START\n");
    int acc_count;
    int thr_count;
    scanf("%d %d", &acc_count, &thr_count);
    pthread_mutex_t *mutexes = calloc(acc_count, sizeof(*mutexes));
    double *accounts = calloc(acc_count, sizeof(*accounts));
    //printf("iniating mutexes\n");
    for (int i = 0; i < acc_count; ++i) {
        pthread_mutex_init(&mutexes[i], NULL);
    }
    //printf("inited\n");
    struct Mythread *propthreads = malloc(thr_count * sizeof(*propthreads));
    for (int i = 0; i < thr_count; ++i) {
        scanf("%d", &propthreads[i].iterations);
        scanf("%d %lf", &propthreads[i].first, &propthreads[i].addfirst);
        scanf("%d %lf", &propthreads[i].second, &propthreads[i].addsecond);
        if (propthreads[i].first > propthreads[i].second) {
            swap_prop_acc(&propthreads[i]);
        }
        propthreads[i].accounts = accounts;
        propthreads[i].mutexes = mutexes;
        //printf("prop %d inited", i);
    }
    pthread_attr_t tattr;
    pthread_attr_init(&tattr);
    pthread_attr_setstacksize(&tattr, sysconf(_SC_THREAD_STACK_MIN));
    pthread_t threads[thr_count];
    for (int i = 0; i < thr_count; ++i) {
        pthread_create(&threads[i], &tattr, routine, &propthreads[i]);
    }
    //printf("created\n");
    for (int i = 0; i < thr_count; ++i) {
        pthread_join(threads[i], NULL);
    }
    for (int i = 0; i < acc_count; ++i) {
        printf("%.10g\n", accounts[i]);
    }
    return 0;
}
