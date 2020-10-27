def add(x,y):
    sum = x + y
    return sum

def main():
    x = int(input("Num1:"))
    y = int(input("Num2:"))
    pdb.set_trace()
    z = add(x,y)
    print(z)

if __name__ == "__main__":
    main()
    