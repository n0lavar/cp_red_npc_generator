import os
import secrets
import subprocess
import sys

from base_test import BaseTest, PROJECT_DIR


REPOSITORY_DIR = PROJECT_DIR.parent
MAIN_SCRIPT = PROJECT_DIR / "src" / "main.py"


class SeedDeterminismTest(BaseTest):
    def test_same_seed_and_arguments_produce_same_output_for_all_ranks_and_roles(self):
        seed = secrets.randbelow(2 ** 32 - 1) + 1
        environment = dict(os.environ, PYTHONPATH=str(REPOSITORY_DIR))

        for matrix_arguments in self.argument_matrix():
            with self.subTest(seed=seed, **matrix_arguments):
                arguments = [
                    sys.executable,
                    str(MAIN_SCRIPT),
                    f"--seed={seed}",
                    f"--rank={matrix_arguments['rank']}",
                    f"--role={matrix_arguments['role']}",
                    "--nationality=en_US",
                    "--flat",
                    "--model-id=",
                ]

                first_run = self._run(arguments, environment)
                second_run = self._run(arguments, environment)

                self.assertEqual(first_run.stdout + first_run.stderr,
                                 second_run.stdout + second_run.stderr)

    @staticmethod
    def _run(arguments, environment):
        return subprocess.run(
            arguments,
            cwd=PROJECT_DIR,
            env=environment,
            capture_output=True,
            text=True,
            check=True,
        )