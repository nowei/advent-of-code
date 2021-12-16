sample = False
file = "sample16.txt" if sample else "input16.txt"
ans = []

def parse(byte_str, ind):
    version_number = int(byte_str[ind:ind+3], 2)
    packet_type = int(byte_str[ind+3:ind+6], 2)
    total = version_number
    if packet_type == 4: # it's a literal
        # check every 5 bits 
        i = 0
        tmp = ""
        while byte_str[ind+6+i * 5] != '0':
            tmp += byte_str[ind+6+i*5+1:ind+6+i*5+5]
            i += 1
        tmp += byte_str[ind+6+i*5+1:ind+6+i*5+5]
        end_ind = ind+6+i*5+5
        total = version_number
    else: # it's an operator
        length_type = int(byte_str[ind+6], 2)
        if length_type == 0:
            bits_in_subpackets = int(byte_str[ind+7:ind+22], 2)
            end_ind = ind+22+bits_in_subpackets
            next_ind = ind+22
            while next_ind < end_ind:
                temp, next_ind = parse(byte_str, next_ind)
                total += temp
            assert(next_ind == end_ind)
        else: #length_type == 0
            num_subpackets = int(byte_str[ind+7:ind+18], 2)
            next_ind = ind + 18
            for i in range(num_subpackets):
                temp, next_ind = parse(byte_str, next_ind)
                total += temp
            end_ind = next_ind
    return total, end_ind

with open(file, "r") as f:
    for line in f:
        byte_str = ""
        for c in line.strip():
            byte_str += bin(int(c, 16))[2:].zfill(4)
        next_ind = 0
        total = 0
        while next_ind < len(byte_str):
            if all([c == '0' for c in byte_str[next_ind:]]): break
            temp, next_ind = parse(byte_str, next_ind)
            total += temp
        ans.append(total)
print(ans)
if sample:
    assert(ans[0] == 14)
    assert(ans[1] == 16)
    assert(ans[2] == 12)
    assert(ans[3] == 23)
    assert(ans[4] == 31)