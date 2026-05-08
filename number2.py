import numpy as np

def generate():
    print("автоматическая генерация")
    lines_arr = input("строк массива?")
    try:
        n = int(lines_arr)
    except ValueError:
        print("Ошибка: введите целое число.")
        return generate()
    columns_str = input("столбцов массива?")
    try:
        g = int(columns_str)
    except ValueError:
        print("Ошибка: введите целое число.")
        return generate()

    A = np.empty((n, g))
    i = 0
    while i < n:
        random_integers = np.random.randint(0 , 100 , g)
        A[i] = random_integers
        i += 1
    print("список до A[" + str(n) + "][" + str(g) + "]:", "\n" , A)
    return A

def files(array_A):
    np.savetxt('number2_before.txt' , array_A , fmt='%d' , delimiter=' ' , newline='\n')
    array_B = np.loadtxt('number2_before.txt')
    n = np.size(array_B, axis=0)
    g = np.size(array_B , axis=1)
    print("Какую строку просуммировать")
    choice = input()
    choice = int(choice) - 1
    array_C = array_B[choice].copy()
    i = 0
    while i < n:
        array_B[i] += array_C
        i += 1
    np.savetxt('number2_after.txt' , array_B , fmt='%d' , delimiter=' ' , newline='\n')



def main():
    print("Задание 11: Выполнить обработку матрицы. Просуммировать элементы каждой строки матрицы с соответствующими элементами L-й строки")
    a = generate()
    b = files(a)


if __name__ == "__main__":
    main()
