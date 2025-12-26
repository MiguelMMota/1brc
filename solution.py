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

# TODO:
# 1. Read File line by line
# 2. Process each line as straightforwardly as possible
# 3. Aggregate, sort, and print results



from collections import defaultdict


def process_line(line: str) -> tuple[str, float]:
    station, temperature = line.split(";")
    return station, float(temperature)


def main() -> None:
    data = defaultdict(list)
    with open("measurements.txt", "r") as f:
        lines = f.readlines()

        for line in lines:
            station, temperature = process_line(line)
            data[station].append(temperature)

    aggregate_data = {}
    for station, temperatures in data.items():
        _min = min(temperatures)
        _mean = round(sum(temperatures) / len(temperatures), 1)
        _max = max(temperatures)
        aggregate_data[station] = f"{_min}|{_mean}|{_max}"

    print(dict(sorted(aggregate_data.items())))


if __name__ == "__main__":
    main()
