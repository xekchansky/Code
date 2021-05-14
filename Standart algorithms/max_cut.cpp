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
    int n, optimum = -1;
    cin >> n;
    vector<vector<int>> Nodes(n, vector<int> (n));
    for (size_t i = 0; i < n; ++i) {
        for (size_t j = 0; j < n; ++j) {
            cin >> Nodes[i][j];
        }
    }
    vector<int> Color(n);
    vector<int> Optimum_Color(n);
    for (size_t i = 0; i < (n / 2) + 1; ++i) {
        Color[i] = 1;
        int local_cut = 0;
        sort(Color.begin(), Color.end());
        for (size_t j = 0; j < Fact(n); ++j) {
            local_cut = 0;
            for (int x = 0; x < n; ++x) {
                if (Color[x] == 1) {
                    for (int y = 0; y < n; ++y) {
                        if (Color[y] == 0) {
                            local_cut += Nodes[x][y];
                        }
                    }
                }
            }
            if (local_cut > optimum) {
                optimum = local_cut;
                Optimum_Color = Color;
            }
            if (next_permutation(Color.begin(), Color.end()) == false)
                break;
        }
        // cout << "round " << Color[0] << ' ' << Color[1] << ' ' << Color[2] << '\n';
    }
    cout << optimum << '\n';
    for (int i = 0; i < n; ++i) {
        Optimum_Color[i]++;
        cout << Optimum_Color[i] << ' ';
    }
}
