#Дано положительное число. Реализуйте метод, который выведет все его
#цифры по одной, в обратном порядке, а также их сумму. Реализовать двумя
#способами: с использованием рекурсии и без.

def without_recursion(num):
    print(*[i for i in reversed(num)])
    print(sum(map(int, [i for i in num])))


def with_recursion(num, summ=0):
    if not num:
        print('\n', summ, sep='')
        return
    else:
        summ += int(num[-1])
        print(num[-1], end=" ")
        with_recursion(num[:-1], summ)


def main():
    num = input()
    with_recursion(num)
    #without_recursion(num)


if __name__ == "__main__":
    main()
