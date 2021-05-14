#include <iostream>
#include <vector>

using namespace std;

void mymerge(auto v1_begin, auto v1_end, auto v2_begin, auto v2_end, auto v_begin) {
    while (v1_begin != v1_end && v2_begin != v2_end) {
        if (*v1_begin < *v2_begin) {
            *v_begin = *v1_begin;
            v1_begin++;
        } else {
            *v_begin = *v2_begin;
            v2_begin++;
        }
        v_begin++;
    }
    while (v1_begin != v1_end) {
        *v_begin = *v1_begin;
        v1_begin++;
        v_begin++;
    }
    while (v2_begin != v2_end) {
        *v_begin = *v2_begin;
        v2_begin++;
        v_begin++;
    }
}

void my_merge_sort(auto v_begin, auto v_end) {
    if ((v_end - v_begin) < 2)
        return;
    auto middle = v_begin + ((v_end - v_begin) / 2);
    my_merge_sort(v_begin, middle);
    my_merge_sort(middle, v_end);
    vector<int> new_v(v_end - v_begin);
    mymerge(v_begin, middle, middle, v_end, new_v.begin());
    copy(new_v.begin(), new_v.end(), v_begin);
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
    my_merge_sort(V.begin(), V.end());
    for (int i = 0; i < n; i++) {
        cout << V[i] << ' ';
    }
}
