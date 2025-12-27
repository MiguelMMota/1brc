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
| Replace `min()`/`max()` with `if` statements | 2:35.85 | Avoid extra function call and memory allocations, and allow CPU to optimise branch paths that will rarely be taken  | ❌ |
| Mutate objects in place | 2:31.88 | Avoid extra function call and memory allocations, and allow CPU to optimise branch paths that will rarely be taken  | ✅ |
| Hoist list access | 2:39.06 | | ❌ |
| mmap | 2:10.87 | | ✅ |
| Only decode station name into utf-8 when aggregating results | 2:01.56 | We don't need to decode it every line | ✅ |
| Treat floats as ints | 1:55.12 | We're casting the temperature bytes to float every line, but we know the values follow a strict format. This allows us to treat them as ints, and convert back to single decimal place floats when printing results. | ✅ |
| Implicitly skip the "." character | 1:45.30 | Instead of comparing each byte to the floating point character, iterate all bytes up to the last two, then add the last byte, which corresponding to the number after the decimal point | ✅ |
| Store value directly in `temperature` instead of temporarily using `result` | 1:44.45 | This also includes a change to set the sign of `temperature` by multiplying it in place, instead of assigning from `result * sign`. Hard to say how much of the performance boost is due to noise, but it seems a sound change anyways | ✅ |
| Initialise temperature directly to the first digit's value, instead of 0 | 1:33.54 | This allows us to skip an iteration when we loop over the bytes. A separate measurement gave ~1:39, so measurements should be taken with an extra grain of salt from now on | ✅ |
| Use arithmetic instead of if-statement to determine sign and offset | 1:32.39 | Since the first byte is always either b'-' (45) or b'0' - b'9' (48-57), we can determine the sign and offset with a series of arithmetic operations, removing a branch that is hard for the CPU to predict correctly (assuming there's a roughly equal amount of negative and positive temperatures in the dataset) | ✅ |
| Use mm.readline | 1:08.49 | It's much faster than trying to find "\n" | ✅ |
| Parallelisation | 8.677 | My `CPU_COUNT` is 14 | ✅ |

## Take-aways

1. We don't get to do some optimisations on account of internal optimisations that pypy's JIT compiler already does. For example: swap order of operands, replacing `min()`/`max()` with branched paths that will frequently be skipped
2. `perf` isn't very useful with pypy's JIT compiler because a lot of the code is already optimised and it's difficult to gather insights from the report
3. SIMD isn't valuable in this case, as the Python overhead would negate SIMD gains
