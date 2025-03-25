#include <iostream>
#include <random>
#include <iomanip>
#include <chrono>

using namespace std;

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        cerr << "Not enought arguments. Usage: " << argv[0] << " <Iterations> <Seed>" << std::endl;
    }

    auto start = chrono::high_resolution_clock::now();

    long long num_points = stoll(argv[1]);
    long long seed = stoll(argv[2]);

    mt19937 gen(seed);
    uniform_real_distribution<> dis(0, 1);

    long long num_inside = 0;
    for (long long i = 0; i < num_points; i++)
    {
        double x = dis(gen);
        double y = dis(gen);
        if (x * x + y * y <= 1)
        {
            num_inside++;
        }
    }

    auto stop = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::microseconds>(stop - start);

    // time in microseconds
    cout << num_inside << endl << num_points << endl << duration.count() << endl;

    return 0;
}