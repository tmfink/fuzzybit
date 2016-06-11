# Disable ansi color output
pset option ansicolor off

# Make sure ASLR in still enabled
set disable-randomization off

# Break on function that starts main, after segments are mapped by dynamic loader
b __libc_start_main

# Run program
r

# Print section mappings (requires PEDA plugin)
peda vmmap

# Quit
q
