# 1️⃣🐝🏎️ The One Billion Row Challenge

My take on the 1BRC challenge in Python.

## Steps

| Change | Benchmark | Comments |
|--------|-----------|----------|
| Read whole file eagerly, process each line, store all values | - | As simple (and inefficient) as possible. Didn't even finish, because we're trying to load the entire file into memory  |
| Read lazily | - | Still didn't finish, because we're storing all samples into memory |
| Don't store values | 9:59.44 | Instead of storing all measurements for each station, store only max, min, sum, count |
| pypy3 | 6:26:15 | From this row on, all runs will be with pypy |
| | | |
| | | |
| | | |
| | | |
| | | |
| | | |