#include <vector>

int main() {
    int n;
    std::cin >> n;
    std::vector<int> weights(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> weights[i];
    }
    std::vector <int> prices(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> prices[i];
    }
    int W;
    std::cin >> W;

	//dp
    std::vector<int> K(W + 2);
    for (int i = 0; i < n; ++i) {
        for (int j = W; j > weights[i]; --j) {
            if (K[j - weights[i]]) {
                K[j] = std::max(K[j], K[j - weights[i]] + prices[i]);
            }
        }
        K[weights[i]] = std::max(K[weights[i]], prices[i]);
    }

	//find best
    int total_weight = 0, total_price = K[0];
    for (int i = 0; i <= W ; ++i) {
        if (total_price < K[i]) {
            total_price = K[i];
            total_weight = i;
        }
    }

    std::cout << total_weight << ' ' << total_price << '\n';
    return 0;
}
