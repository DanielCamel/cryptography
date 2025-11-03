import argparse

# начальные состояния регистров (4 бита каждый)
INIT_R0_STATE = [0, 1, 0, 0]   # R0 начальное состояние: 0100
INIT_R1_STATE = [0, 1, 1, 1]   # R1 начальное состояние: 0111  
INIT_CTRL_STATE = [0, 1, 1, 0] # Управляющий регистр: 0110

# последовательности для каждого регистра
# указываем индексы битов, которые участвуют в XOR для генерации нового бита
TAPS_R0 = [0, 1]    # R0: x^4 + x^3 + 1
TAPS_R1 = [0, 3]    # R1: x^4 + x + 1
TAPS_CTRL = [0, 1, 2, 3]  # CTRL: x^4 + x^3 + x^2 + x + 1

# открытый текст, который требуется зашифровать (16 бит)
PLAINTEXT = '1011010010011101'

class LFSR:
    """класс для работы с линейным регистром сдвига с ОС"""
    
    def __init__(self, taps, init_state, name="LFSR"):
        self.taps = taps          # позиции отводных битов
        self.state = init_state.copy()  # текущее состояние регистра
        self.name = name          # название регистра для отладки

    def step(self):
        """один шаг работы LFSR"""
        # сохраняем текущее состояние для вывода
        old_state = ''.join(str(b) for b in self.state)
        
        # выходной бит - старший бит регистра
        output_bit = self.state[0]
        
        # вычисляем новый бит через XOR отводных битов
        new_bit = 0
        for tap_index in self.taps:
            new_bit ^= self.state[tap_index]
        
        # сдвигаем регистр и добавляем новый бит
        self.state = self.state[1:] + [new_bit]
        
        # формируем новое состояние для вывода
        new_state = ''.join(str(b) for b in self.state)
        
        return old_state, new_state, output_bit

    def get_state(self):
        """возвращаем текущее состояние в виде строки"""
        return ''.join(str(b) for b in self.state)


def simulate(steps):
    """основная функция моделирования генератора Геффе"""
    
    # инициализируем регистры
    r0 = LFSR(TAPS_R0, INIT_R0_STATE, "R0")
    r1 = LFSR(TAPS_R1, INIT_R1_STATE, "R1")  
    ctrl = LFSR(TAPS_CTRL, INIT_CTRL_STATE, "CTRL")
    
    # шаг 1: выводим работу каждого регистра по отдельности
    print("=== Работа регистров по отдельности ===")
    for register in (r0, r1, ctrl):
        print(f"\n--- {register.name} ---")
        outputs = []
        
        for step_num in range(1, steps + 1):
            old_state, new_state, output = register.step()
            print(f"Шаг {step_num}: {old_state} -> {new_state} | выход={output}")
            outputs.append(str(output))
        
        print(f"Выходная последовательность {register.name}: {''.join(outputs)}")
    
    # шаг 2: Пересчитываем выходные последовательности для генерации гаммы
    print("\n=== Генерация гаммы и шифрование ===")
    
    # сбрасываем регистры в исходное состояние
    r0.state = INIT_R0_STATE.copy()
    r1.state = INIT_R1_STATE.copy() 
    ctrl.state = INIT_CTRL_STATE.copy()
    
    # генерируем выходные последовательности
    r0_output = []
    r1_output = []
    ctrl_output = []
    
    for k in range(steps):
        i0, j0, bit0 = r0.step()
        i1, j1, bit1 = r1.step() 
        i_ctrl, j_ctrl, bit_ctrl = ctrl.step()
        
        r0_output.append(str(bit0))
        r1_output.append(str(bit1))
        ctrl_output.append(str(bit_ctrl))
    
    r0_seq = ''.join(r0_output)
    r1_seq = ''.join(r1_output)
    ctrl_seq = ''.join(ctrl_output)
    
    print(f"R0:   {r0_seq}")
    print(f"R1:   {r1_seq}") 
    print(f"CTRL: {ctrl_seq}")
    
    # шаг 3: генерируем гамму по генератора Геффе
    # если управляющий бит = 1, берем бит из R1, иначе из R0
    gamma = []
    for i in range(steps):
        if ctrl_seq[i] == '1':
            gamma.append(r1_seq[i])
        else:
            gamma.append(r0_seq[i])
    
    gamma_seq = ''.join(gamma)
    print(f"\nГамма:              {gamma_seq}")
    
    # шаг 4: шифруем открытый текст
    plaintext = PLAINTEXT.strip().replace(' ', '')
    
    if len(plaintext) != steps:
        print("Ошибка: длина открытого текста не совпадает с числом шагов")
        return
    
    # выполняем побитовое XOR между открытым текстом и гаммой
    cipher = []
    for i in range(steps):
        cipher_bit = str(int(plaintext[i]) ^ int(gamma_seq[i]))
        cipher.append(cipher_bit)
    
    ciphertext = ''.join(cipher)
    
    print(f"Открытый текст:    {plaintext}")
    print(f"Шифртекст:        {ciphertext}")


if __name__ == '__main__':
    # Настройка аргументов командной строки
    parser = argparse.ArgumentParser(description="Генератор Геффе: моделирование и шифрование")
    parser.add_argument('-n', '--steps', type=int, default=16,
                       help='Количество шагов моделирования (по умолчанию: 16)')
    
    args = parser.parse_args()
    
    # Запускаем моделирование
    simulate(steps=args.steps)