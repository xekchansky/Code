//simple multi-thread program
/*На стандартном потоке ввода задаются:

    Число счетов acc_count - положительное целое 32-битное число.
    Число нитей thr_count - положительное целое 32-битное число.
    Далее для каждой нити задаются 5 чисел, описывающих параметры работы нити:
        Число итераций - положительное целое 32-битное число.
        Индекс первого счета (в интервале [0; acc_count)).
        Сумма для зачисления на первый счет или списания с первого счета (double).
        Индекс второго счета (в интервале [0; acc_count), не совпадает с первым индексом).
        Сумма для зачисления на второй счет или списания со второго счета (double).

Счета хранятся в типе double. Начальное состояние каждого счета - нулевое.

Главная программа должна создать thr_count нитей, каждая из которых должна обновлять состояние двух счетов следующим образом.

Каждая нить выполняет предписанное ей число итераций обновления состояния счетов. На каждой итерации к первому счету прибавляется сумма для зачисления на первый счет, а ко второму счету - сумма для зачисления на второй счет. Отрицательная сумма подразумевает списание со счета.

После завершения работы нитей главная программа выводит на стандартный поток вывода итоговое состояние всех счетов с помощью форматного преобразования %.10g и завершает работу.

Каждая нить должна блокировать только те счета, с которыми ведется работа. Обновление и первого, и второго счета должно выполняться в одной критической секции в каждой итерации цикла.

Не используйте глобальные переменные.

*/
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
