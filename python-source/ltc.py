
from typing import List, Tuple

def ltc_code(data_stream: List[Tuple[int, int]], e: int) -> List[Tuple[int, int]]:
    # Функция для обработки потока данных по заданному алгоритму.
    # 
    # Алгоритм:
    # 1. Инициализация: получение первой точки данных, сохранение её в z. Получение следующей точки (t2, v2),
    #    использование её для инициализации границ UL (верхняя граница) и LL (нижняя граница).
    # 2. Вычисление highLine как линии, соединяющей z и UL.
    # 3. Вычисление lowLine как линии, соединяющей z и LL.
    # 4. Получение следующей точки данных. Преобразование точки в вертикальный сегмент с использованием погрешности e.
    #    Определение ul как верхней точки сегмента и ll как нижней точки сегмента.
    # 5. Если highLine находится ниже ll или lowLine находится выше ul, переход к шагу 9, иначе продолжение.
    # 6. Если highLine выше ul, установка UL в ul.
    # 7. Если lowLine ниже ll, установка LL в ll.
    # 8. Переход к шагу 2.
    # 9. Завершение: вывод z в выходной поток данных.
    # 10. Установка z как точки, находящейся посередине между UL и LL.
    # 11. Установка UL как ul.
    # 12. Установка LL как ll.
    # 13. Переход к шагу 2.

    def calculate_line(p1: Tuple[float, float], p2: Tuple[int, int]) -> Tuple[int, int]:
        #Вычисляет коэффициенты прямой, проходящей через две точки (p1 и p2)
        x1, y1 = p1
        x2, y2 = p2
        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1
        return slope, intercept

    result_stream = []
    z = data_stream[0]
    t2, v2 = data_stream[1]
    UL = (t2, v2 + e)
    LL = (t2, v2 - e)
    i = 2

    while i < len(data_stream):
        highLine = calculate_line(z, UL)
        lowLine = calculate_line(z, LL)
        t, v = data_stream[i]
        ul = (t, v + e)
        ll = (t, v - e)
        
        slope_high, intercept_high = highLine
        slope_low, intercept_low = lowLine
        
        if (slope_high * t + intercept_high < ll[1]) or (slope_low * t + intercept_low > ul[1]):
            result_stream.append(z)
            z = ((UL[0] + LL[0]) / 2, (UL[1] + LL[1]) / 2)
            UL = ul
            LL = ll
        else:
            if slope_high * t + intercept_high > ul[1]:
                UL = ul
            if slope_low * t + intercept_low < ll[1]:
                LL = ll

        i += 1

    result_stream.append(z)
    
    return result_stream