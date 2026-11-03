# Baseline pilot — November 3, 2026

All 15 planned missions have saved results: five strategies, each run with seeds 2026, 2027, and 2028.

Each mission used 80 actual microphones, a one-day (86,400-second) horizon, and a one-second timestep. All missions reached that time limit. They used the same simulator source hashes and configuration apart from the seed. Recorded rewards agree with the default reward formula.

| Strategy | Runs | Mean elephants poached | Mean poachers caught | Mean reward | Mean runtime (seconds) |
|---|---:|---:|---:|---:|---:|
| Uniform Spread | 3 | 1.33 | 1.67 | -709.73 | 23.96 |
| Targeted Fortress | 3 | 1.00 | 3.00 | -572.40 | 23.71 |
| Perimeter Defense | 3 | 1.67 | 0.67 | -821.07 | 24.15 |
| 50/50 Combination | 3 | 0.67 | 1.67 | -643.07 | 23.91 |
| Random Placement | 3 | 1.00 | 1.00 | -728.40 | 24.49 |

Total measured mission runtime: 360.648 seconds (6.01 minutes). Average: 24.043 seconds per mission. Range: 22.311–25.889 seconds. This sums time inside the mission calls; it excludes interpreter startup and time between manual commands.

The combination strategy had the lowest mean poaching in these three seeds. Fortress had the highest mean reward and most captures. Reward also values captures and penalizes uncaught poachers, so its ranking differs from the poaching ranking. No mission caught all ten poachers; completed=false is a simulation outcome, not a program failure.

These are exploratory pilot results, not evidence of a statistically reliable winner. The one-day horizon produced both poaching and capture events, supporting its use for an initial training experiment. Three seeds are insufficient for a robust performance comparison.

For a direct PPO comparison, keep the microphone budget at 80, keep the same simulator/horizon/timestep, and evaluate the learned policy and all baselines on a fresh shared set of evaluation seeds excluded from training. The current PPO implementation also selects microphone count, so fixed-budget training needs configuration support before launching it. Decide whether the training reward appropriately reflects the primary goal of reducing elephant poaching.

For planning only, 4,096 missions at the measured mean would take about 27.4 hours of elapsed time serially, before training overhead. This is a rough extrapolation, not a PPO benchmark: layouts, counts, outcomes, hardware and training overhead can change runtime. Full training was not run for this pilot.

| Strategy | Seed | Poached | Caught | Reward | Runtime (seconds) | Source |
|---|---:|---:|---:|---:|---:|---|
| Uniform Spread | 2026 | 0 | 2 | -550.40 | 23.428 | [JSON](uniform_original_n80_seed2026_20261103T231551_920182Z/mission_results.json) |
| Uniform Spread | 2027 | 2 | 1 | -828.40 | 23.401 | [JSON](uniform_original_n80_seed2027_20261103T232456_529508Z/mission_results.json) |
| Uniform Spread | 2028 | 2 | 2 | -750.40 | 25.051 | [JSON](uniform_original_n80_seed2028_20261103T232520_020053Z/mission_results.json) |
| Targeted Fortress | 2026 | 0 | 4 | -394.40 | 22.311 | [JSON](fortress_original_n80_seed2026_20261103T232902_916578Z/mission_results.json) |
| Targeted Fortress | 2027 | 2 | 4 | -594.40 | 23.226 | [JSON](fortress_original_n80_seed2027_20261103T232925_316392Z/mission_results.json) |
| Targeted Fortress | 2028 | 1 | 1 | -728.40 | 25.583 | [JSON](fortress_original_n80_seed2028_20261103T232948_630929Z/mission_results.json) |
| Perimeter Defense | 2026 | 2 | 1 | -828.40 | 22.953 | [JSON](perimeter_original_n80_seed2026_20261103T233250_814077Z/mission_results.json) |
| Perimeter Defense | 2027 | 2 | 0 | -906.40 | 24.867 | [JSON](perimeter_original_n80_seed2027_20261103T233313_861579Z/mission_results.json) |
| Perimeter Defense | 2028 | 1 | 1 | -728.40 | 24.621 | [JSON](perimeter_original_n80_seed2028_20261103T233338_818722Z/mission_results.json) |
| 50/50 Combination | 2026 | 1 | 2 | -650.40 | 22.768 | [JSON](combination_original_n80_seed2026_20261103T233535_214640Z/mission_results.json) |
| 50/50 Combination | 2027 | 1 | 1 | -728.40 | 24.392 | [JSON](combination_original_n80_seed2027_20261103T233558_069851Z/mission_results.json) |
| 50/50 Combination | 2028 | 0 | 2 | -550.40 | 24.565 | [JSON](combination_original_n80_seed2028_20261103T233622_550681Z/mission_results.json) |
| Random Placement | 2026 | 1 | 2 | -650.40 | 23.274 | [JSON](random_n80_seed2026_20261103T233840_813694Z/mission_results.json) |
| Random Placement | 2027 | 1 | 1 | -728.40 | 24.319 | [JSON](random_n80_seed2027_20261103T233904_177461Z/mission_results.json) |
| Random Placement | 2028 | 1 | 0 | -806.40 | 25.889 | [JSON](random_n80_seed2028_20261103T233928_587632Z/mission_results.json) |

Default reward: -100 × poached - 70 × uncaught + 8 × caught - 0.08 × microphones + 50 if all poachers are caught.
