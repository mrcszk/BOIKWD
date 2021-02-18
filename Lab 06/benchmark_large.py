from knapsack_benchmark import KnapsackBenchmark

problems = ["ks_82_0", "ks_100_1", "ks_106_0", "ks_200_1", "ks_300_0", "ks_400_0"]

benchmark = KnapsackBenchmark(problems)
benchmark.run()