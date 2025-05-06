from enum import Enum

ERR_INCOMPARABLE_EMBEDDED_TYPES = "Переданы несравнимые экземпляры классов '{}' и '{}'"
ERR_INCORRECT_HEAP_TYPE = "Тип кучи не является экземпляром класса HeapType"


class HeapType(Enum):
    MIN = "min"
    MAX = "max"


class Heap:
    """
    Универсальная структура данных "Куча".

    Куча представляет собой частично упорядоченную структуру данных, которая
    позволяет эффективно получать минимальный или максимальный элемент (в зависимости от типа).
    Эта реализация поддерживает минимальную и максимальную кучу, определяемую через параметр `HeapType`.

    Основные операции:
    - `push(item)`: добавляет элемент в кучу.
    - `pop()`: удаляет и возвращает минимальный/максимальный элемент.
    - `top()`: возвращает минимальный/максимальный элемент без удаления.

    Параметры:
    - `heap_type` (`HeapType`): определяет тип кучи (минимальная или максимальная).
    """

    def __init__(self, heap_type: HeapType):
        """
        Инициализирует пустую кучу заданного типа.
        :param heap_type: Тип кучи (HeapType.MIN или HeapType.MAX).
        :raises TypeError: Если передан некорректный тип кучи.
        """
        if not isinstance(heap_type, HeapType):
            raise TypeError(ERR_INCORRECT_HEAP_TYPE)
        self.heap_type = heap_type
        self.elements = []

    def _swap(self, parent, child) -> bool:
        """
        Определяет, нужно ли менять местами элементы в зависимости от типа кучи.
        :param parent: Родительский элемент.
        :param child: Дочерний элемент.
        :return: True, если элементы нужно поменять местами.
        """
        try:
            if self.heap_type == HeapType.MIN:
                return parent < child # Ошибка: сравнение в обратную сторону
            return parent < child 
        except TypeError:
            raise TypeError(
                ERR_INCOMPARABLE_EMBEDDED_TYPES.format(type(child).__name__, type(parent).__name__)
            )

    def _sift_up(self, index: int):
        """
        Поднимает элемент на корректное место в куче.
        :param index: Индекс элемента.
        """
        parent = (index - 1) // 2
        while index > 0 and self._swap(self.elements[parent], self.elements[index]):
            self.elements[parent], self.elements[index] = (
                self.elements[index],
                self.elements[parent],
            )
            index = parent
            parent = (index - 1) // 2

    def _sift_down(self, index: int):
        """
        Опускает элемент на корректное место в куче.
        :param index: Индекс элемента.
        """
        size = len(self.elements)
        while True:
            l_child = 2 * index + 1
            r_child = 2 * index + 2
            swap_candidate = index

            if l_child < size and self._swap(self.elements[swap_candidate], self.elements[l_child]):
                swap_candidate = l_child

            if r_child < size and self._swap(self.elements[swap_candidate], self.elements[r_child]):
                swap_candidate = r_child

            if swap_candidate == index:
                break

            self.elements[index], self.elements[swap_candidate] = (
                self.elements[swap_candidate],
                self.elements[index],
            )
            index = swap_candidate

    def push(self, item):
        """
        Добавляет элемент в кучу.
        :param item: Элемент для добавления.
        """
        self.elements.append(item)
        self._sift_up(len(self.elements) - 1)

    def pop(self):
        """
        Удаляет и возвращает корневой элемент из кучи.
        :return: Корневой элемент.
        :raises IndexError: Если куча пуста.
        """
        if not self.elements:
            raise IndexError("Попытка извлечения элемента из пустой кучи.")
        root = self.elements[0]
        self.elements[0] = self.elements[-1]
        self.elements.pop()
        if self.elements:
            self._sift_down(0)
        return root

    def top(self):
        """
        Возвращает корневой элемент без удаления.
        :return: Корневой элемент.
        :raises IndexError: Если куча пуста.
        """
        if not self.elements:
            raise IndexError("Попытка обращения к пустой куче.")
        return self.elements[0]

    def __len__(self):
        """
        Возвращает количество элементов в куче.
        :return: Количество элементов.
        """
        return len(self.elements)


if __name__ == "__main__":
    print("Пример: минимальная куча")
    min_heap = Heap(heap_type=HeapType.MIN)
    min_heap.push(3)
    min_heap.push(1)
    min_heap.push(6)
    min_heap.push(5)
    min_heap.push(2)
    min_heap.push(4)

    print("Куча:", min_heap)
    print("Минимальный элемент:", min_heap.pop())
    print("Куча после удаления минимального элемента:", min_heap)

    print("\nПример: максимальная куча")
    max_heap = Heap(heap_type=HeapType.MAX)
    max_heap.push(3)
    max_heap.push(1)
    max_heap.push(6)
    max_heap.push(5)
    max_heap.push(2)
    max_heap.push(4)

    print("Куча:", max_heap)
    print("Максимальный элемент:", max_heap.pop())
    print("Куча после удаления максимального элемента:", max_heap)