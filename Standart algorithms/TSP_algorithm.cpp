#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

int Fact(int n) {
    if (n == 0)
        return 1;
    return n * Fact(n - 1);
}

int main() {
    int n, k = 0, optimum = 1000000000;
    cin >> n;
    vector<vector<int>> Nodes(n, vector<int> (n));
    for (size_t i = 0; i < n; ++i) {
        for (size_t j = 0; j < n; ++j) {
            cin >> Nodes[i][j];
        }
    }
    vector<int> Way(n);
    for (size_t i = 0; i < n; ++i) Way[i] = i;
    for (size_t i = 0; i < Fact(n); ++i) {
        bool error = false;
        int min_way = 0;
        for (int j = 0; j < n - 1; ++j) {
            if (Nodes[Way[j]][Way[j + 1]] == 0)
                error = true;
            else
                min_way += Nodes[Way[j]][Way[j + 1]];
        }
        if (Nodes[Way[n - 1]][Way[0]] == 0)
            error = true;
        min_way += Nodes[Way[n - 1]][Way[0]];
        if ((error == false) && (min_way < optimum))
            optimum = min_way;
        if (next_permutation(Way.begin(), Way.end()) == false)
            break;
    }
    if (n == 1)
        cout << 0;
    else if (optimum == 1000000000)
        cout << -1;
    else
        cout << optimum;
}
