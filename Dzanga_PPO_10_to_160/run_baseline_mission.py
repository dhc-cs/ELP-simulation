#!/usr/bin/env python3
"""Run and record one headless mission using the existing PPO simulator."""
import argparse
import hashlib
import json
import os
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--strategy', default='uniform_original', choices=[
        'uniform_original', 'fortress_original', 'perimeter_original',
        'combination_original', 'random',
    ])
    parser.add_argument('--seed', type=int, default=2026)
    parser.add_argument('--mics', type=int, default=80, choices=range(10, 161, 5))
    parser.add_argument('--sim-seconds', type=float, default=86400)
    parser.add_argument('--dt', type=float, default=1)
    parser.add_argument('--output-root', type=Path,
                        default=Path(__file__).resolve().parent / 'baseline_pilot')
    args = parser.parse_args()
    if not (args.sim_seconds > 0 and args.dt > 0):
        parser.error('--sim-seconds and --dt must be positive')

    # One simulation worker; limit numerical libraries to one thread as well.
    for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                     'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        os.environ[variable] = '1'
    simulator_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(simulator_dir))
    from dzanga_optimize import Config, run_configuration, write_rows

    cfg = Config(sim_seconds=args.sim_seconds, dt=args.dt, seed=args.seed)
    started = datetime.now(timezone.utc)
    stamp = started.strftime('%Y%m%dT%H%M%S_%fZ')
    output = args.output_root.resolve() / f'{args.strategy}_n{args.mics}_seed{args.seed}_{stamp}'
    output.mkdir(parents=True, exist_ok=False)
    metadata = {
        'purpose': 'baseline_pilot',
        'started_utc': started.isoformat(),
        'strategy': args.strategy,
        'requested_mics': args.mics,
        'spacing_level': 2,
        'config': asdict(cfg),
        'python_version': sys.version,
        'simulator_directory': str(simulator_dir),
        'source_sha256': {
            name: hashlib.sha256((simulator_dir / name).read_bytes()).hexdigest()
            for name in ('dzanga_optimize.py', 'dzanga_sim.py')
        },
    }
    (output / 'settings.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(f'Starting ONE mission: {args.strategy}, {args.mics} mics, seed {args.seed}', flush=True)
    print(f'Maximum simulated duration: {cfg.sim_seconds:g} seconds; timestep: {cfg.dt:g} second(s)', flush=True)
    print(f'Output: {output}', flush=True)
    print('Running headlessly on CPU. Results will appear when the mission finishes. Ctrl+C stops it.', flush=True)
    before = perf_counter()
    try:
        result = run_configuration(args.mics, args.strategy, 2, args.seed, cfg,
                                   layout_path=output / 'microphone_layout.csv')
    except KeyboardInterrupt:
        (output / 'interrupted.txt').write_text('Stopped before completion; no final mission result.\n')
        print('\nStopped. Settings and any saved layout remain; no final mission result was recorded.')
        return 130
    row = dict(strategy=args.strategy, seed=args.seed, requested_mics=args.mics,
               spacing_level=2, horizon_seconds=cfg.sim_seconds, dt=cfg.dt,
               **result, wall_seconds=round(perf_counter() - before, 3))
    write_rows(output / 'mission_results.csv', [row])
    (output / 'mission_results.json').write_text(json.dumps(row, indent=2) + '\n')
    print('\nMission finished:')
    print(json.dumps(row, indent=2))
    print(f'\nSaved results to: {output}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
