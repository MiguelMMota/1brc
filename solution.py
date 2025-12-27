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
# 1. Custom hashing
# 2. Avoid branch predictions with high odds of failure
# 3. SIMD
# 4. "|".join(item) instead of f"{_min}|{_sum/_count:.1f}|{_max}"
# 5. More efficient data aggregation and dict sorting?
# 6. Use string formatting to print ints as single decimal place floats instead of doing multiplication

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
                station = line[:semicolon_pos]
                
                temp_bytes = line[semicolon_pos+1:]

                # if the first byte is less than b'0' (i..e: it's b'-'), offset will be 1. Otherwise (i.e.: it's a digit, it will be 0)
                offset = 1 - temp_bytes[0] // 48
                # if the first byte is "-", offset is 1, and sign is 1-2=-1. If the first byte is a digit, offset is 0, and sign is 1-0=1
                sign = 1 - 2 * offset
                # NB: the alternative to the code above is adding an if-statement to check if the first byte is b'-', but we're likely to
                # incur high penalties from CPU branch predicition, assuming the odds of the character being in the dataset are close to 50%

                temperature = (temp_bytes[offset] - 48) * 10

                # TODO: this will now only ever go over the digit before the decimal place if there are two digits
                # before the decimal place. I wonder if there's a better way to do this, instead of slicing the list
                # for a single iteration.
                for b in temp_bytes[offset+1:-2]:
                    temperature += b - 48  # ord(b'0')
                    temperature *= 10

                temperature += temp_bytes[-1] - 48  # ord(b'0')
                temperature *= sign

                entry = data[station]
                entry[0] = min(temperature, entry[0])
                entry[1] = max(temperature, entry[1])
                entry[2] += temperature
                entry[3] += 1

    aggregate_data = {}
    for station, (_min, _max, _sum, _count) in data.items():
        aggregate_data[station.decode('utf-8')] = f"{0.1*_min:.1f}|{0.1*_sum/_count:.1f}|{0.1*_max:.1f}"

    print(dict(sorted(aggregate_data.items())))


if __name__ == "__main__":
    main()
