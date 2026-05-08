def len(list):  # Ручной подсчёт длины списка без использования len()
    size_list = 0
    temp = list
    while True: # Проходим по индексам до возникновения IndexError
        try:
            temp[size_list]
            size_list += 1
        except IndexError:
            break
    return size_list

def input_user():
    print("Введите список чисел(нажмите enter для генерации):")
    A = []
    generated_list = []
    user_input_A = input()
    if user_input_A == '':
        count_str = input("Сколько чисел сгенерировать?")
        try:                                                      # Автогенерация с защитой от некорректного ввода
            n = int(count_str)
        except ValueError:
            print("Ошибка: введите целое число.")
            return input_user()
        prev_val = 1
        i = 0
        while i < n:
            val = (prev_val * 7 + i * 3 + 5) % 100
            generated_list.append(int(val))
            prev_val = val
            i += 1
        A = generated_list
    else:
        current_num = ''
        for char in user_input_A:
            if char != ' ':
                current_num += char
            else:
                if current_num != '':
                    A.append(int(current_num))
                    current_num = ''
        if current_num != '':
            try:
                A.append(int(current_num))
            except ValueError:
                print("Ошибка: введите целое число.")
                return input_user()

    print("список до A[" + str(len(A)) + "]:" , A)
    return A

def delete(A):       #Выполнение алгоритма без стандартных функций
    swap_A = []
    max = int(A[0])
    gh = 0
    for i in range(len(A) - 1):
        if max < int(A[i + 1]):
            max = A[i + 1]
            gh = i+1
    for i in range(len(A)):
        current_val = A[i]
        if i <= gh or (int(current_val) % 2 != 0 and i >= gh):
            swap_A.append(int(A[i]))
    print("список после A[" + str(len(swap_A)) + "]:" , swap_A)

def main():
    print("Задание 11: Удалить четные элементы после максимального")
    b = input_user()
    delete(b)

if __name__ == "__main__":
    main()
