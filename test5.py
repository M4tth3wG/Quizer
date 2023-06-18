

from IntBuilder import IntBuilder


x = []

x.insert(-1,-1)
x.insert(-1,-2)

print(x)


ib = IntBuilder()

ib.add_int(1)
ib.add_int(2)
ib.add_int(3)

ib.print_list()

print(ib.prev())
print(ib.current_int)
ib.drop_current_int()
ib.add_int(4)
ib.print_list()