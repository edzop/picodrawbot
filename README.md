# picodrawbot

Raspberry Pico based drawing robot


Linux Setup:

`sudo usermod -a -G dialout $USER`

Example commands:

``
LT 10
RT 10 FW 10


BW 10
``

## Repeat & Iteration Commands

### REPEAT

Executes a block of commands a fixed number of times.

**Syntax:**
```
REPEAT <count> [ <commands> ]
```

**Example** — draw a square:
```
REPEAT 4 [ FW 50 RT 30 ]
```

Commands inside the block are case-insensitive:
```
repeat 10 [ fw 5 lt 6 ]
```

### FOR

Executes a block of commands once per iteration, stepping a counter variable `$i` from a start value to an end value (inclusive).

**Syntax:**
```
FOR <start> <end> <step> [ <commands> ]
```

- `<start>` — initial value of `$i`
- `<end>` — final value of `$i` (inclusive)
- `<step>` — amount `$i` increases each iteration
- `$i` — use inside the block to refer to the current counter value

**Example** — draw a spiral:
```
FOR 10 100 10 [ FW $i RT 30 ]
```
This runs 10 iterations with `$i` = 10, 20, 30, … 100.

Both constructs can be used anywhere in a command sequence and can appear on a single line or spread across multiple lines.
