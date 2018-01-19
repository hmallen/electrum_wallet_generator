x = '(123, 456)'
print(x)
print(type(x))

y = tuple(x.strip('\(').strip('\)').split(', '))
print(y)
print(type(y))
print(type(y[0]))

z = tuple([int(num) for num in y])
print(z)
print(type(z))
print(type(z[0]))

x = {'a':'(123, 456)', 'b':'(769, 101)', 'c':'(213, 141)'}
print(x)
print(type(x))

for key in x:
    x[key] = tuple(x[key].strip('\(').strip('\)').split(', '))
print(x)
print(type(x))
print(type(x['a']))

for key in x:
    x[key] = tuple([int(val) for val in x[key]])
print(x)
print(type(x))
print(type(x['a']))
