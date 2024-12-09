from typing import List
from dataclasses import dataclass

InputType = str
parent_path = "src/days/day09/"


@dataclass
class Block:
    id: int
    size: int
    freespace: int

    def __repr__(self):
        return f"({self.id}, {self.size}, {self.freespace})"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    result = ""
    with open(file_name, "r") as f:
        result = f.read().strip()
    return result


def _to_blocks(_input: str):
    blocks = []
    for i in range(0, len(_input), 2):
        size_str = _input[i]
        freespace_str = "0"
        if i + 1 != len(_input):
            freespace_str = _input[i + 1]
        blocks.append(Block(i // 2, int(size_str), int(freespace_str)))
    return blocks


def _to_values(gaps: List[Block]) -> List[int]:
    s = []
    for block in gaps:
        s.extend([block.id] * block.size)
        s.extend([-1] * block.freespace)
    return s


def _checksum(s: List[int]):
    total = 0
    for idx, c in enumerate(s):
        if c == -1:
            continue
        total += c * idx
    return total


def consolidate_memory_pt1(s: List[int]):
    result = []
    i = 0
    j = len(s) - 1
    while i <= j:
        if s[i] != -1:
            result.append(s[i])
            i += 1
            continue
        if s[j] == -1:
            j -= 1
            continue
        result.append(s[j])
        i += 1
        j -= 1
    return result


def part1(_input: InputType) -> int:
    blocks = _to_blocks(_input)
    memory_values = _to_values(blocks)
    memory_shifted = consolidate_memory_pt1(memory_values)
    return _checksum(memory_shifted)


def consolidate_memory_pt2(blocks: List[Block]) -> List[Block]:
    j = len(blocks) - 1
    # 00...111...2...333.44.5555.6666.777.888899
    # 0099.111...2...333.44.5555.6666.777.8888..
    # 0099.1117772...333.44.5555.6666.....8888..
    # 0099.111777244.333....5555.6666.....8888..
    # 00992111777.44.333....5555.6666.....8888..
    starting_ind = 0
    # Attempt to move every block from the right side to the left exactly 1 (one) time.
    while j > starting_ind:
        # check if there are any freespace starting from the left of size cand_block.size
        cand_block = blocks[j]
        for i in range(starting_ind, j):
            if blocks[i].freespace >= cand_block.size:
                # There are two cases to be aware of; when
                # * the consolidating block is to the left of the candidate block
                # * the consolidating block is at least 2 steps away from the candidate block

                # On the left of the candidate block
                if i == j - 1:
                    # e.g. 333...444.
                    # ---> 333444....
                    # We need to move over the freespace
                    cand_block.freespace = cand_block.freespace + blocks[i].freespace
                    # Zero out the consolidated block's freespace
                    blocks[i].freespace = 0
                else:
                    # e.g. 222....333...444..
                    # ---> 222444.333........
                    # We need to:
                    # * move over the free space + block size of the cand block -> the left of cand block
                    # * shift over the candidate block to the gap + update its free space
                    # * update the ordering to reflect the change
                    #   * (evaluation index is updated due to shifting around)

                    # current space occupied by candidate block (to be moved)
                    cand_block_size = cand_block.size + cand_block.freespace
                    # The new freespace that the candidate block will have after moving
                    cand_block.freespace = blocks[i].freespace - cand_block.size
                    # Update the freespace of the left block
                    left_of_cand_block = blocks[j - 1]
                    left_of_cand_block.freespace += cand_block_size
                    # Zero out the consolidated block's freespace
                    blocks[i].freespace = 0
                    # Move the blocks such that the candidate block is to the right of the consolidated block.
                    blocks = (
                        blocks[: i + 1]
                        + [cand_block]
                        + blocks[i + 1 : j]
                        + blocks[j + 1 :]
                    )
                    # Increment j because we have shifted the blocks around
                    j += 1
                # There was a consolidation, blocks[i] freespace should be 0
                break
        j -= 1
        # Determine what starting offset we can use (has freespace)
        for i in range(starting_ind, j):
            if blocks[i].freespace != 0:
                starting_ind = i
                break
    # while i < j:
    #     curr_block = result[-1]
    #     cand_block = blocks[j]
    #     if cand_block.size <= curr_block.freespace:
    #         # move the cand block
    #         # add the freespace to the block on the left
    #         cand_block_size = cand_block.size + cand_block.freespace
    #         cand_block.freespace = curr_block.freespace - cand_block.size
    #         left_of_cand_block = blocks[j - 1]
    #         left_of_cand_block.freespace += cand_block_size
    #         result.append(cand_block)
    #         moved.add(cand_block.id)
    #         j -= 1

    #     if blocks[j].size > blocks[i].freespace:
    #         j -= 1
    #         continue
    #     blocks[i].freespace
    #     result.append(blocks[i])
    return blocks


def part2(_input: InputType) -> int:
    blocks = _to_blocks(_input)
    new_blocks = consolidate_memory_pt2(blocks)
    memory_values = _to_values(new_blocks)
    return _checksum(memory_values)


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
