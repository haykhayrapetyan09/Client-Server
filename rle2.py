def rle2_encode(data):
    encoded = ""
    count = 1
    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            encoded += str(count) + data[i - 1]
            count = 1
    encoded += str(count) + data[-1]
    return encoded


def rle2_decode(encoded):
    decoded = ""
    count = ""
    for char in encoded:
        if char.isdigit():
            count += char
        else:
            decoded += char * int(count)
            count = ""
    return decoded


text = "hello aaaaaa dddwddwd wdqqdqdqqd ewdewwd"
encoded_text = rle2_encode(text)
print(encoded_text)

decoded_text = rle2_decode(encoded_text)
print(decoded_text)

