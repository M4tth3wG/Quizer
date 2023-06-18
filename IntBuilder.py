from exceptions import EmptyListException, UnexpectedEventException, NoQuizArgumentsException

class IntBuilder:

    def __init__(self):
        self._int_list = []
        self._actual_index = 0

    @property
    def current_index(self):
        return self._actual_index

    @property
    def current_int(self):
        if not self.is_empty():
            return self._int_list[self._actual_index]
        else:
            return None
    
    @current_int.setter
    def current_int(self, new_int):
        if not self.is_empty():
            self._int_list[self._actual_index] = new_int
        elif self._actual_index == 0:
            self._int_list.append(new_int)
        else:
            raise UnexpectedEventException('Something is wrong!')


    def add_int(self, new_int):
        if not self.is_empty():
            self._actual_index += 1
        self._int_list.insert(self._actual_index, new_int)


    def has_previous(self):
        return self._actual_index > 0

    def has_next(self):
        return self._actual_index < len(self._int_list)-1

    def prev(self):
        if self.has_previous():
            self._actual_index -= 1
            return self._int_list[self._actual_index]
        else:
            raise IndexError()

    def next(self):
        if self.has_next():
            self._actual_index += 1
            return self._int_list[self._actual_index]
        else:
            raise IndexError()
        
    def is_empty(self):
        return self._int_list == []
    
    def get_length(self):
        return len(self._int_list)
        
    def drop_current_int(self):
        if not self.is_empty():
            self._int_list.pop(self._actual_index)
            if self._actual_index >= 1:
                self._actual_index -= 1
        else: 
            raise EmptyListException("Integer list is empty!!!")
        
    def print_list(self):
        result = '['
        for num in self._int_list:
            result += f'{str(num)}, '
        result = result[:-2] + ']'
        print(result)


