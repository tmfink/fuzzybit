#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 BINARY"
    exit 1
fi

if [[ -z "$GDB" ]]; then
    GDB=gdb
fi

BINARY="$1"

filter_word="Start"

# Run binary with GDB and execute commands from entropy-test.gdb
$GDB -x entropy-test.gdb "$BINARY" | grep -A1000 "$filter_word" | grep -v "$filter_word"
