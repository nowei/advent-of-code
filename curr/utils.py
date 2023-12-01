import os

base_text = """
from typing import Any

sample_file = "test/{day}.sample"
input_file = "test/{day}.input"
sample_expected = 0

def parse_file_{day}(file_path) -> Any:
    with open(file_path, "r") as f:
        for line in f:
            pass

def solve_{day}(input: Any) -> Any:
    pass

def main_{day}():
    print("Running script for day {day}")
    sample = parse_file_{day}(sample_file)
    input = parse_file_{day}(input_file)

    sample_out = solve_{day}(sample)

    if sample_out != sample_expected:
        print("Sample results do not match")
        print("Sample expected:")
        print(sample_expected)
        print("Sample result:")
        print(sample_out)
    else:
        print("Sample matched")
    
    out = solve_{day}(input)
    print("This is the result:")
    print(out)


if __name__ == "__main__":
    main_{day}()
"""

def generate_files(day: int):
    s = "{:02d}".format(day)
    day_dict = {"day": s}
    with open("src/day{day}.py".format_map(day_dict), "w") as f:
        out = base_text.format_map(day_dict)
        f.write(out)
    # touch files to create them
    with open("test/{day}.sample".format_map(day_dict), "w") as f:
        pass
    with open("test/{day}.input".format_map(day_dict), "w") as f:
        pass

def main():
    generate_files(2)

if __name__ == '__main__':
    main()
