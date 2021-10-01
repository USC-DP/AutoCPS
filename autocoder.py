#!/usr/bin/env python3
import argparse


parser = argparse.ArgumentParser(description='Generate a C project with a'
                                 'random FSW.')
parser.add_argument('--type', nargs=1, dest='vehicle_type', default=['rover'],
                    help='vehicle type (default=rover)')


# Run autocoder CLI
def run():
    args = parser.parse_args()
    print(args.vehicle_type[0])


if __name__ == "__main__":
    run()
