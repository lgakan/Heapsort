import time
import random


class Node:
    def __init__(self, data, priority):
        self.data = data
        self.priority = priority

    def __lt__(self, other):
        if self.priority < other.priority:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.priority > other.priority:
            return True
        else:
            return False


class Queue:
    def __init__(self, elements_to_sort=None):
        self.table = []
        self.table_size = 0
        # self.elements_to_sort = elements_to_sort
        if elements_to_sort is not None:
            self.heapify(elements_to_sort)

    def is_empty(self) -> bool:
        if self.table_size == 0:
            return True
        elif self.table_size > 0:
            return False

    def peek(self):
        return self.table[0].data

    def dequeue(self):
        if self.is_empty():
            return None

        [self.table[0], self.table[self.table_size - 1]] = [self.table[self.table_size - 1], self.table[0]]
        answer = self.table[self.table_size - 1]
        self.table_size -= 1

        if self.table_size == 0:
            return answer.data

        counter_idx = 0
        counter = self.table[counter_idx]

        while self.left(counter_idx) < self.table_size or self.right(counter_idx) < self.table_size:
            # Only left exist
            if self.left(counter_idx) < self.table_size and self.right(counter_idx) >= self.table_size:
                if counter < self.table[self.left(counter_idx)]:
                    [self.table[self.left(counter_idx)], self.table[counter_idx]] = [self.table[counter_idx],
                                                                                     self.table[self.left(counter_idx)]]
                    counter_idx = self.left(counter_idx)
                    counter = self.table[counter_idx]
                else:
                    break
            # Only right exist
            elif self.left(counter_idx) >= self.table_size and self.right(counter_idx) < self.table_size:
                if counter < self.table[self.right(counter_idx)]:
                    [self.table[self.right(counter_idx)], self.table[counter_idx]] = [self.table[counter_idx],
                                                                                      self.table[
                                                                                          self.right(counter_idx)]]
                    counter_idx = self.right(counter_idx)
                    counter = self.table[counter_idx]
                else:
                    break

            else:
                # Both exist
                # left > right
                if self.table[self.left(counter_idx)] > self.table[self.right(counter_idx)]:
                    if self.table[self.left(counter_idx)] > counter:
                        left = self.table[self.left(counter_idx)]
                        [self.table[self.left(counter_idx)], self.table[counter_idx]] = [self.table[counter_idx],
                                                                                         self.table[
                                                                                             self.left(counter_idx)]]
                        counter_idx = self.left(counter_idx)
                        counter = self.table[counter_idx]
                    else:
                        break
                # right > left
                elif self.table[self.left(counter_idx)] < self.table[self.right(counter_idx)]:
                    if self.table[self.right(counter_idx)] > counter:
                        [self.table[self.right(counter_idx)], self.table[counter_idx]] = [self.table[counter_idx],
                                                                                          self.table[
                                                                                              self.right(counter_idx)]]
                        counter_idx = self.right(counter_idx)
                        counter = self.table[counter_idx]
                    else:
                        break
                # right == left
                else:
                    if self.table[self.left(counter_idx)] > counter:
                        left = self.table[self.left(counter_idx)]
                        [self.table[self.left(counter_idx)], self.table[counter_idx]] = [self.table[counter_idx],
                                                                                         self.table[
                                                                                             self.left(counter_idx)]]
                        counter_idx = self.left(counter_idx)
                        counter = self.table[counter_idx]
                    else:
                        break
        return answer.data

    def enqueue(self, data, priority):
        add_element = Node(data, priority)
        self.table.append(add_element)
        self.table_size += 1

        child_idx = self.table_size - 1
        parent_idx = self.parent(child_idx)
        child = self.table[child_idx]
        parent = self.table[parent_idx]

        while parent != child:
            if child > parent:
                [self.table[child_idx], self.table[parent_idx]] = [self.table[parent_idx], self.table[child_idx]]
                child_idx = parent_idx
                parent_idx = self.parent(child_idx)
                parent = self.table[parent_idx]
            else:
                break

    def print_tab(self):
        if len(self.table) == 0:
            print("{}")
            return
        print('{', end=' ')
        for i in range(len(self.table) - 1):
            print(self.table[i].data, end=', ')
        if self.table[self.table_size - 1]: print(self.table[self.table_size - 1].data, end=' ')
        print('}')

    def print_tree(self, idx, lvl):
        if idx < len(self.table):
            self.print_tree(self.right(idx), lvl + 1)
            print(2 * lvl * '  ', self.table[idx].data, ':', self.table[idx].priority if self.table[idx] else None)
            self.print_tree(self.left(idx), lvl + 1)

    def parent(self, idx):
        ans = (idx - 1) // 2
        if ans > 0:
            return ans
        else:
            return 0

    def left(self, idx):
        return 2 * (idx + 1) - 1

    def right(self, idx):
        return 2 * (idx + 1)

    def heapify(self, elements_to_sort):
        node_array = []
        for l, r in elements_to_sort:
            node_array.append(Node(r, l))

        self.table = node_array
        self.table_size = len(node_array)
        idx_to_sort = []
        for i in range(len(node_array)):
            if self.right(i) < len(node_array) or self.left(i) < len(node_array):
                idx_to_sort.append(i)

        for i in range(len(idx_to_sort) - 1, -1, -1):
            self.repair(i)

    def repair(self, idx):
        answer = self.table[idx]

        if self.table_size == 0:
            return answer.data

        counter_idx = idx
        counter = self.table[counter_idx]

        while self.left(counter_idx) < self.table_size or self.right(counter_idx) < self.table_size:
            # Only left exist
            if self.left(counter_idx) < self.table_size and self.right(counter_idx) >= self.table_size:
                if counter < self.table[self.left(counter_idx)]:
                    [self.table[self.left(counter_idx)], self.table[counter_idx]] = [self.table[counter_idx],
                                                                                     self.table[self.left(counter_idx)]]
                    counter_idx = self.left(counter_idx)
                    counter = self.table[counter_idx]
                else:
                    break
            # Only right exist
            elif self.left(counter_idx) >= self.table_size and self.right(counter_idx) < self.table_size:
                if counter < self.table[self.right(counter_idx)]:
                    [self.table[self.right(counter_idx)], self.table[counter_idx]] = [self.table[counter_idx],
                                                                                      self.table[
                                                                                          self.right(counter_idx)]]
                    counter_idx = self.right(counter_idx)
                    counter = self.table[counter_idx]
                else:
                    break

            else:
                # Both exist
                # left > right
                if self.table[self.left(counter_idx)] > self.table[self.right(counter_idx)]:
                    if self.table[self.left(counter_idx)] > counter:
                        left = self.table[self.left(counter_idx)]
                        [self.table[self.left(counter_idx)], self.table[counter_idx]] = [self.table[counter_idx],
                                                                                         self.table[
                                                                                             self.left(counter_idx)]]
                        counter_idx = self.left(counter_idx)
                        counter = self.table[counter_idx]
                    else:
                        break
                # right > left
                elif self.table[self.left(counter_idx)] < self.table[self.right(counter_idx)]:
                    if self.table[self.right(counter_idx)] > counter:
                        [self.table[self.right(counter_idx)], self.table[counter_idx]] = [self.table[counter_idx],
                                                                                          self.table[
                                                                                              self.right(counter_idx)]]
                        counter_idx = self.right(counter_idx)
                        counter = self.table[counter_idx]
                    else:
                        break
                # right == left
                else:
                    if self.table[self.left(counter_idx)] > counter:
                        left = self.table[self.left(counter_idx)]
                        [self.table[self.left(counter_idx)], self.table[counter_idx]] = [self.table[counter_idx],
                                                                                         self.table[
                                                                                             self.left(counter_idx)]]
                        counter_idx = self.left(counter_idx)
                        counter = self.table[counter_idx]
                        break
                    else:
                        break

        return answer.data


if __name__ == "__main__":
    list_of_elements = [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'), (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'),
                        (2, 'J')]
    queue = Queue(list_of_elements)
    queue.print_tab()
    queue.print_tree(0, 0)
    while not queue.is_empty():
        queue.dequeue()
    queue.print_tab()

    print()

    list_of_numbers = []
    for i in range(10000):
        list_of_numbers.append((int(random.random() * 100), 'X'))

    t_start = time.perf_counter()
    queue_2 = Queue(list_of_numbers)
    while not queue_2.is_empty():
        queue_2.dequeue()
    t_stop = time.perf_counter()
    print("Czas obliczeń dla sortowania kopcowego:", "{:.7f}".format(t_stop - t_start))
