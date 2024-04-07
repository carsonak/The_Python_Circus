#!/usr/bin/python3
f = float("infinity")
n = float("nan")
f2 = float("infinity")
n2 = float("nan")

print(f"-1 > n:", -1 > n)
print(f"0 > n:", 0 > n)
print(f"1 > n:", 1 > n)

print(f"-1 < n:", -1 < n)
print(f"0 < n:", 0 < n)
print(f"1 < n:", 1 < n, end="\n\n")

print(f"-1 > f:", -1 > f)
print(f"0 > f:", 0 > f)
print(f"1 > f:", 1 > f)

print(f"-1 < f:", -1 < f)
print(f"0 < f:", 0 < f)
print(f"1 < f:", 1 < f, end="\n\n")

print(f"f > f:", f > f)
print(f"f > f2:", f > f2)
print(f"f > n:", f > n)

print(f"n > n:", n > n)
print(f"n > n2:", n > n2)
print(f"n > f:", n > f, end="\n\n")

print(f"f < f:", f < f)
print(f"f < f2:", f < f2)
print(f"f < n:", f < n)

print(f"n < n:", n < n)
print(f"n < n2:", n < n2)
print(f"n < f:", n < f, end="\n\n")

print(f"f == f:", f == f)
print(f"f == f2:", f == f2)
print(f"f == n:", f == n)

print(f"n == n:", n == n)
print(f"n == n2:", n == n2)
print(f"n == f:", n == f, end="\n\n")

print(f"f != f:", f != f)
print(f"f != f2:", f != f2)
print(f"f != n:", f != n)

print(f"n != n:", n != n)
print(f"n != n2:", n != n2)
print(f"n != f:", n != f, end="\n\n")

print(f"n is n:", n is n)
print(f"n is n2:", n is n2)
print(f"n2 is n:", n2 is n)
print(f"n is not n2:", n is not n2)
print(f"n2 is n2:", n2 is n2, end="\n\n")

print(f"f is f:", f is f)
print(f"f is f2:", f is f2)
print(f"f2 is f:", f is f)
print(f"f is not f2:", f is not f2)
print(f"f2 is f2:", f2 is f2, end="\n\n")

print(f"f is n:", f is n)
print(f"n is f:", n is f)
print(f"f is not n:", f is not n)
print(f"n is not f:", n is not f)
