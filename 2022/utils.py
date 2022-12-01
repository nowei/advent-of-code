import os
import subprocess
import toml

def generate_files(days):
    data = toml.load("Cargo.toml")
    seen = set(data["workspace"]["members"])
    for d in days:
        day = "day{}".format(d)
        p = subprocess.run(["cargo", "new", "day{}".format(d), "--bin"])

        with open(day + "/" + "sample.txt", 'w') as f: pass
        # TODO: Pull input from internet
        with open(day + "/" + "input.txt", 'w') as f: pass

        if p.returncode == 0:
            # TODO: Init loading file code
            with open(day + "/" + 'src/main.rs', 'w') as f:
                f.write("""
fn main() {
    println!("Hello, worldd!");
}
                """)
            member = day + "/Cargo.toml"
            if member not in seen:
                data["workspace"]["members"].append(member)
    
    with open("Cargo.toml", "w") as toml_file:
        toml.dump(data, toml_file)


def main():
    generate_files([2])

if __name__ == '__main__':
    main()
