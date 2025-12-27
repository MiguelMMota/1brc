# 1️⃣🐝🏎️ The One Billion Row Challenge

My take on the 1BRC challenge in Python.

## Steps

| Change | Benchmark | Comments | Kept? |
|--------|-----------|----------|-------|
| Read whole file eagerly, process each line, store all values | - | As simple (and inefficient) as possible. Didn't even finish, because we're trying to load the entire file into memory  | ✅ |
| Read lazily | - | Still didn't finish, because we're storing all samples into memory | ✅ |
| Don't store values | 9:59.44 | Instead of storing all measurements for each station, store only max, min, sum, count | ✅ |
| pypy3 | 6:26.15 | From this row on, all runs will be with pypy |
| Single function | 4:36.39 | 22.61% of the time was spent on _PyObject_MakeTpCall (calling Python functions). This is interpreter overhead, which we can minimise by using a single function, and fewer temporary variables | ✅ |
| Tuple of station data instead of dict | 3:26.75 | dict storage and lookups are slower than tuples because they require hashing the key | ✅ |
| Single lookup when updating station data | 2:42.68 | Read station data once and mutate it, instead of reading each element separately, which incurs multiple dict lookups | ✅ |
| Set dict default value instead of checking if key is present | 2:30.51 | This saves us an additional lookup for each station, and a branching path | ✅ |
| Swap order of operands | 2:35.04 | This might have resulted in optimisations by the JIT compiler | ❌ |
| Replace `min()`/`max()` with `if` statements | ... | Avoid extra function call and memory allocations, and allow CPU to optimise branch paths that will rarely be taken  | ❌ |
