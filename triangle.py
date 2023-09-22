def sum_until_zero(base, sub, total):

    while base - sub != -1:
        total += base
        base -= sub
        print(total)
        print(base)
        print(sub)

    return total

# Example usage
base = 11
sub = 1
total = 0
# result = sum_until_zero(base, sub, total)
# print(result)

# n = 13
# d = 12

# while n < 20000:
#     print(n)
#     d = d + 12
#     n = n + d
n = 74
t = 0
while t < 8266:
    t += n
    n = n + 1
    print(t)
    print(n)