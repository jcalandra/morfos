import time_manager
import oracle_mso

# Explanation and code based on https://www.programmersought.com/article/55755735846/
input_data = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3,
              3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
              5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 5,
              5, 5, 5, 5, 5, 5, 5, 5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5,
              5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 2, 2, 2, 2, 2, 2, 2, 2,
              2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
              6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 6, 6, 6,
              6, 6, 6, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]

input_stream = ''
for i in input_data:
    input_stream += chr(i + 96)
print(input_stream)
buffer = ""
search_buf_length, look_ahead_buf_length, len_input_stream = len(input_stream), 10, len(input_stream)
search_buf_pos, look_ahead_buf_pos = 0, 0
encode_list = []


def move_forward(step):
    global search_buf_pos, look_ahead_buf_pos, buffer
    search_buf_pos += step; look_ahead_buf_pos += step
    buffer = input_stream[search_buf_pos:search_buf_pos+search_buf_length+look_ahead_buf_length]


def init():
    global buffer
    global look_ahead_buf_pos, search_buf_pos
    sym_offset = 0
    buffer = input_stream[look_ahead_buf_pos:look_ahead_buf_pos + look_ahead_buf_length]
    while sym_offset < search_buf_length:
        max_length, max_offset, next_sym = 0, 0, buffer[sym_offset]
        buffer_length = len(buffer)
        for offset in range(0, sym_offset):
            pos = sym_offset - offset - 1
            n = 0
            while buffer[pos + n] == buffer[sym_offset + n]:
                # si on veut comparer à partir du signal, il faut changer la fonction de similarité à cet endroit
                n += 1
                if n == buffer_length - sym_offset - 1:
                    break
            if max_length < n:
                max_length = n
                max_offset = offset + 1
                next_sym = buffer[sym_offset + n]
        encode_list.append([max_offset, max_length, next_sym])
        look_ahead_buf_pos = look_ahead_buf_pos + max_length + 1
        sym_offset += max_length + 1
        if sym_offset > search_buf_length:
            search_buf_pos = search_buf_pos + max_length + 1
            buffer = input_stream[0: sym_offset + 1]
        else:
            buffer = input_stream[0: look_ahead_buf_length + sym_offset]


def encode():
    if search_buf_length >= len(input_stream):
        return len(input_stream)
    sym_offset = search_buf_length
    max_length, max_offset, next_sym = 0, 0, buffer[sym_offset]
    buffer_length = len(buffer)
    if buffer_length - sym_offset == 1:
        encode_list.append([0, 0, next_sym])
        return max_length
    for offset in range(1, search_buf_length+1):
        pos = sym_offset - offset
        n = 0
        while buffer[pos + n] == buffer[sym_offset + n]:
            n += 1
            if n == buffer_length - search_buf_length - 1:
                break
        if max_length < n:
            max_length = n
            max_offset = offset
            next_sym = buffer[sym_offset+n]
    encode_list.append([max_offset, max_length, next_sym])
    return max_length


def lz77():
    while 1:
        step = encode() + 1
        move_forward(step)
        if look_ahead_buf_pos >= len_input_stream:
            break


def decode(encode_l):
    ans = ''
    for i in encode_l:
        offset, length, sym = i
        for j in range(length):
            ans += ans[-offset]
        ans += sym
    return ans


def reinitialisation():
    global buffer
    global search_buf_pos, look_ahead_buf_pos
    global encode_list
    buffer = ""
    search_buf_pos, look_ahead_buf_pos = 0, 0
    encode_list = []


def main():
    init()
    lz77()
    for i in encode_list:
        print(i)
    print(input_stream == decode(encode_list))


def test_lz77_encodage():
    start_time = time_manager.time()
    for j in range(10000):
        init()
        lz77()
        reinitialisation()
    print(time_manager.time() - start_time)


def test_lz77_decodage():
    start_time = time_manager.time()
    init()
    lz77()
    for j in range(10000):
        decode(encode_list) == input_stream
    print(time_manager.time() - start_time)


def test_lz77():
    start_time = time_manager.time()
    for j in range(10000):
        init()
        lz77()
        decode(encode_list) == input_stream
        reinitialisation()
    print(time_manager.time() - start_time)


def test_oracle():
    start_time = time_manager.time()
    for j in range(10000):
        oracle = oracle_mso.build_oracle(input_data, [], flag='f')
    print(time_manager.time() - start_time)

main()
# test_lz77()
# test_lz77_encodage()
# test_lz77_decodage()
# test_oracle()
