#Даны два целочисленных массива. Верните массив чисел уникальных для
#обоих массивов.

def solution(arr1, arr2):
    set1 = set(arr1)
    set2 = set(arr2)
    union = set1.union(set2)
    intersection = set1.intersection(set2)
    unique_numbers = union - intersection
    return unique_numbers


def main():
    arr1 = input().split()
    arr2 = input().split()
    print(*solution(arr1, arr2))


if __name__ == "__main__":
    main()
