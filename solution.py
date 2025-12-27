#
#  Copyright 2023 The original authors
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

# TODO: efficiency ideas:
# 1. Read as byte data
# 2. mmap
# 3. Handle floats as ints
# 4. Custom hashing
# 5. Avoid branch predictions with high odds of failure
# 6. SIMD
# 7. "|".join(item) instead of f"{_min}|{_sum/_count:.1f}|{_max}"
# 8. More efficient data aggregation and dict sorting?

from collections import defaultdict
import math
import mmap


def main() -> None:
    data = defaultdict(lambda: [math.inf, -math.inf, 0, 0])

    with open("measurements.txt", "r+b") as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            start = 0
            while True:
                end = mm.find(b'\n', start)
                if end == -1:
                    break

                line = mm[start:end]
                start = end + 1

                semicolon_pos = line.find(b';')
                station = line[:semicolon_pos].decode('utf-8')
                temperature = float(line[semicolon_pos+1:])

                entry = data[station]
                entry[0] = min(temperature, entry[0])
                entry[1] = max(temperature, entry[1])
                entry[2] += temperature
                entry[3] += 1

    aggregate_data = {}
    for station, (_min, _max, _sum, _count) in data.items():
        aggregate_data[station] = f"{_min}|{_sum/_count:.1f}|{_max}"

    print(dict(sorted(aggregate_data.items())))


if __name__ == "__main__":
    main()
