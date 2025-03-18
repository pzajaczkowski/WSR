#include <iostream>
#include <random>
#include <iomanip>

using namespace std;

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        cerr << "Not enought arguments. Usage: " << argv[0] << " <Iterations> <Seed>" << std::endl;
    }

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

    cout << num_inside << std::endl << num_points << std::endl;

    return 0;
}