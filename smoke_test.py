#!/usr/bin/env python3
"""
Smoke test for the real space_game.py engine.

Runs headless simulation ticks against the actual game module (not mock copies).
Exit 0 on success, 1 on failure.
"""

import os
import subprocess
import sys

TICKS = os.environ.get('GAME_SMOKE_TICKS', '600')


def main():
    env = os.environ.copy()
    env['GAME_HEADLESS_MODE'] = '1'
    env['GAME_SMOKE_TEST'] = '1'
    env['GAME_SMOKE_TICKS'] = TICKS
    env.setdefault('GAME_VERBOSE', '0')

    result = subprocess.run(
        [sys.executable, 'space_game.py'],
        env=env,
        cwd=os.path.dirname(os.path.abspath(__file__)),
    )
    return result.returncode


if __name__ == '__main__':
    sys.exit(main())
