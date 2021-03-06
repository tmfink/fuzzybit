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


# pylint: disable=bad-builtin


def get_value_from_hex(hex_str):
    """Convert hex string starting with 0x to an int"""

    if hex_str.startswith('0x'):
        return int(hex_str[2:], 16)
    else:
        raise Exception('Hex string must start with "0x"')


def get_vmmap_values(cmd_output_lines):
    """
    Parse vmmap command output lines

    :param list[str] cmd_output_lines: list of vmmap output commands
    :rtype: list[(int, int)]
    :return: list of parsed rows
    """

    return [tuple(get_value_from_hex(v) for v in x.split()[:2])
            for x in cmd_output_lines]


def get_section_names(cmd_output_lines):
    """Get name of sections"""

    return [' '.join(x.split()[2:])
            for x in cmd_output_lines]


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
        """Helper to get output lines from vmmap command"""
        try:
            cmd_output = subprocess.check_output(vmmap_cmd).decode()
        except subprocess.CalledProcessError:
            print('Command %s failed' % ' '.join(vmmap_cmd))
            sys.exit(1)

        return filter(None, cmd_output.split('\n'))


    for i in range(iterations):
        cmd_output_lines = get_cmd_output_lines()

        # Get section names on first iteration
        if i == 0:
            section_names = get_section_names(cmd_output_lines)

            vmmap_fuzzy_values = [(FuzzyInt(bit_len), FuzzyInt(bit_len))
                                  for _ in range(len(section_names))]

        vmmap_values = get_vmmap_values(cmd_output_lines)
        for (fuzzy_start_addr, fuzzy_end_addr), (start_addr, end_addr) in zip(
                vmmap_fuzzy_values, vmmap_values):
            fuzzy_start_addr.observe_value(start_addr)
            fuzzy_end_addr.observe_value(end_addr)

    return vmmap_fuzzy_values, section_names


def print_sections_entropy(fuzzy_values, section_names, format=None):
    """Print bit-level entropy of sections"""

    if format is None:
        format = 'hex'

    def get_value(fuzzy_int):
        if format == 'hex':
            return fuzzy_int.get_hex_value()
        elif format == 'bin':
            return fuzzy_int.get_value()
        else:
            raise Exception('Unknown format "%s"' % format)

    for ((start, end), name) in zip(fuzzy_values, section_names):
        print('{start} -> {end}  {name}\n'
              '    entropy: {start_entropy}, {end_entropy} bits'.format(
                  start=get_value(start), end=get_value(end), name=name,
                  start_entropy=start.get_entropy(), end_entropy=end.get_entropy()))


def main():
    """Parse command-line arguments and print sections entropy"""

    parser = argparse.ArgumentParser(description='Process vmmap output')
    parser.add_argument('--iterations', '-i', default=5, type=int,
                        help='Number of times to run vmmap command')
    parser.add_argument('--bit-len', '-b', default=64, type=int,
                        help='Number of times to run vmmap command')
    parser.add_argument('--format', '-f', default='hex', choices=['hex', 'bin'],
                        help='fuzzyint number format')
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

    print_sections_entropy(fuzzy_values, section_names, format=args.format)


if __name__ == '__main__':
    main()
