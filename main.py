#!/usr/bin/python
# -*- coding: utf-8 -*-

import loot
import equipment
import argparse


def main(rank_num: int) -> int:
    loot.generate_loot(rank_num)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--rank", type=int, required=True)
    args = parser.parse_args()

    return_code = main(args.rank)
    exit(return_code)
