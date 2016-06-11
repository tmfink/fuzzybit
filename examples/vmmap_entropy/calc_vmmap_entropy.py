#!/usr/bin/python

"""Example of how to use fuzzybit to show vmmap entropy"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os
import subprocess
import sys

from fuzzybit import FuzzyInt


def get_value_from_hex(s):
    """Convert hex string starting with 0x to an int"""

    if s.startswith('0x'):
        return int(s[2:], 16)
    else:
        raise Exception('Hex string must start with "0x"')


def get_vmmap_values(get_cmd_output_lines):
    """
    Parse vmmap command output lines

    :param list[str] get_cmd_output_lines: list of vmmap output commands
    :rtype: list[(int, int)]
    :return: list of parsed rows
    """

    return [tuple(get_value_from_hex(v) for v in x.split()[:2])
            for x in get_cmd_output_lines()]


def get_section_names(get_cmd_output_lines):
    """Get name of sections"""

    return [' '.join(x.split()[2:])
            for x in get_cmd_output_lines()]


def get_vmmap_entropy(vmmap_cmd, iterations=5, bit_len=64):
    """
    Get entropy of sections after given number of iterations.

    :param list[str] vmmap_cmd: argv of command that prints start/end
        addresses of sections.
    :param int iterations: number of iterations to sample start/end addresses
    :rtype: (list[(FuzzyInt, FuzzyInt)], list[str])
    :return: (vmmap_fuzzy_values, section_names), where:

        vmmap_fuzzy_values
          list of section start/end address FuzzyInts

        section_names
          list of section names
    """

    if iterations < 2:
        raise Exception('Number of sample iterations must be >= 2')

    def get_cmd_output_lines():
        try:
            cmd_output = subprocess.check_output(vmmap_cmd).decode()
        except subprocess.CalledProcessError:
            print('Command %s failed' % ' '.join(vmmap_cmd))
            sys.exit(1)

        return filter(None, cmd_output.split('\n'))

    section_names = get_section_names(get_cmd_output_lines)

    vmmap_fuzzy_values = [(FuzzyInt(bit_len), FuzzyInt(bit_len))
                          for _ in range(len(section_names))]

    for _ in range(iterations):
        vmmap_values = get_vmmap_values(get_cmd_output_lines)
        for ((fuzzy_start_addr, fuzzy_end_addr), (start_addr, end_addr)) in zip(
                vmmap_fuzzy_values, vmmap_values):
            fuzzy_start_addr.observe_value(start_addr)
            fuzzy_end_addr.observe_value(end_addr)

    return vmmap_fuzzy_values, section_names


def print_sections_entropy(fuzzy_values, section_names):
    """Print bit-level entropy of sections"""

    for ((start, end), name) in zip(fuzzy_values, section_names):
        print('{start} -> {end}  {name}\n'
              '    entropy: {start_entropy}, {end_entropy} bits'.format(
                  start=start.get_value(), end=end.get_value(), name=name,
                  start_entropy=start.get_entropy(), end_entropy=end.get_entropy())
        )


def main():
    """Parse command-line arguments and print sections entropy"""

    parser = argparse.ArgumentParser(description='Process vmmap output')
    parser.add_argument('--iterations', '-i', default=5, type=int,
                        help='Number of times to run vmmap command')
    parser.add_argument('--bit-len', '-b', default=64, type=int,
                        help='Number of times to run vmmap command')
    parser.add_argument('command', nargs='+',
                        help='command to run to get instance of vmmap output')
    args = parser.parse_args()

    vmmap_cmd = args.command
    num_iterations = args.iterations

    # Prepend current working directory to PATH
    os.environ["PATH"] = os.getcwd() + os.pathsep + os.environ["PATH"]

    fuzzy_values, section_names = get_vmmap_entropy(
            vmmap_cmd,
            iterations=num_iterations, bit_len=args.bit_len
    )

    print_sections_entropy(fuzzy_values, section_names)


if __name__ == '__main__':
    main()
