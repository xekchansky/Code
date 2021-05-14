#include <iostream>
#include <vector>

using namespace std;

vector<int>::iterator mypartition(auto v_begin, auto v_end, int g) {
    vector<int>::iterator last = v_begin;
    for (auto i = v_begin; i < v_end; i++) {
        if (*i < g) {
            swap(*i, *last);
            last++;
        }
    }
    return last;
}

void my_quicksort(auto v_begin, auto v_end) {
    if ((v_end - v_begin) < 2)
        return;
    int Max = -1000000000;
    int Min = 1000000000;
    auto i = v_begin;
    while (i != v_end) {
        if (*i < Min)
            Min = *i;
        if (*i > Max)
            Max = *i;
        i++;
    }
    if (Min == Max)
        return;
    int g = (Max + Min) / 2;
    if (g == Max)
        g--;
    if (g == Min)
        g++;
    auto middle = mypartition(v_begin, v_end, g);
    my_quicksort(v_begin, middle);
    my_quicksort(middle, v_end);
}

int main() {
    int n;
    cin >> n;
    vector<int> V;
    for (int i = 0; i < n; i++) {
        int a;
        cin >> a;
        V.push_back(a);
    }
    my_quicksort(V.begin(), V.end());
    for (int i = 0; i < n; i++) {
        cout << V[i] << ' ';
    }
}

