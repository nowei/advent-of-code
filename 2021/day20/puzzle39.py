sample = False
file = "sample20.txt" if sample else "input20.txt"
image = []
with open(file, "r") as f:
    enhancement_algo = [0 if c == "." else 1 for c in f.readline().strip()]
    f.readline()
    for line in f:
        image.append([0, 0] + [0 if c == "." else 1 for c in line.strip()] + [0, 0])
    image.insert(0, [0 for _ in range(len(image[0]))])
    image.insert(0, [0 for _ in range(len(image[0]))])
    image.append([0 for _ in range(len(image[0]))])
    image.append([0 for _ in range(len(image[0]))])
rows = len(image)
cols = len(image[0])


def print_image(image):
    for line in image:
        print("".join(["#" if i == 1 else "." for i in line]))


print_image(image)


def apply_algo(image, outside, algo):
    outside = algo[int("{}{}{}{}{}{}{}{}{}".format(*[outside for _ in range(9)]), 2)]
    new_image = []
    for i in range(1, len(image) - 1):
        new_image.append([outside, outside])
        for j in range(1, len(image[0]) - 1):
            v = algo[
                int(
                    "{}{}{}{}{}{}{}{}{}".format(
                        *[
                            image[i + k][j + l]
                            for k in range(-1, 2)
                            for l in range(-1, 2)
                        ]
                    ),
                    2,
                )
            ]
            new_image[-1].append(v)
        new_image[-1].append(outside)
        new_image[-1].append(outside)
    print("creating new image???")
    new_image.insert(0, [outside for _ in range(len(new_image[0]))])
    new_image.insert(0, [outside for _ in range(len(new_image[0]))])
    new_image.append([outside for _ in range(len(new_image[0]))])
    new_image.append([outside for _ in range(len(new_image[0]))])
    return new_image, outside


outside = 0
for i in range(2):
    image, outside = apply_algo(image, outside, enhancement_algo)
    print_image(image)

ans = sum([sum(row) for row in image])
print(ans)
if sample:
    assert ans == 35
