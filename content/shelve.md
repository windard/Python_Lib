## shelve

shelve 是一个简单的 数据存储方案 ，在数据量比较小的情况下可以作为数据库使用，将数据以键值对的形式保存。

### 简单示例

```
# coding=utf-8

import shelve

s = shelve.open('test.dat')

s['x'] = ['a', 1, [2, 'b']]

s['x'].append('d')

print s['x']

```

结果是

```
['a', 1, [2, 'b']]
```

这就很奇怪了，因为所有的键值对都是不可改变对象，只能通过一个中间临时变量来改变。

```
# coding=utf-8

import shelve

s = shelve.open('test.dat')

s['x'] = ['a', 1, [2, 'b']]

temp = s['x']

temp.append('d')

s['x'] = temp

print s['x']

```

这样的结果是

```
['a', 1, [2, 'b'], 'd']
```

或者这样

```
# coding=utf-8

import shelve

s = shelve.open('test.dat', writeback=True)

s['x'] = ['a', 1, [2, 'b']]

s['x'].append('d')

print s['x']

```

结果是

```
['a', 1, [2, 'b'], 'd']
```

## 高级应用

使用 shelve 做一个简单的数据库应用

```
# coding=utf-8

import sys
import shelve

def store_person(db):
    """
    Query user from data and store it in the shelf object
    """

    pid = raw_input('Enter unique ID number: ')

    person = {}
    person['name'] = raw_input('Enter name: ')
    person['age'] = raw_input('Enter age: ')
    person['phone'] = raw_input('Enter phone number: ')

    db[pid] = person

def lookup_person(db):
    """
    Query user from ID and desired field, and fetch the corresponding data from
    the shelf object
    """
    pid = raw_input('Enter ID number: ')
    field = raw_input('what would you like to know? (name, age, phone) ')
    field = field.strip().lower()
    print field.capitalize() + ':', db[pid][field]

def print_help():
    print 'The available commands are:'
    print 'store    : Store information about a person'
    print 'lookup   : Looks up a person from ID number'
    print 'quit     : Save changes and exit'
    print '?        : Prints this message'

def enter_command():
    cmd = raw_input('Enter command (? for help): ')
    cmd = cmd.strip().lower()
    return cmd

def main():
    database = shelve.open('D:\\database.dat')
    try:
        while True:
            cmd = enter_command()
            if cmd == 'store':
                store_person(database)
            elif cmd == 'lookup':
                lookup_person(database)
            elif cmd == '?':
                print_help()
            elif cmd == 'quit':
                break
    finally:
        database.close()

if __name__ == '__main__':
    main()
```

```
Enter command (? for help): ?
The available commands are:
store    : Store information about a person
lookup   : Looks up a person from ID number
quit     : Save changes and exit
?        : Prints this message
Enter command (? for help): store
Enter unique ID number: 1
Enter name: windard
Enter age: 12
Enter phone number: 12345678
Enter command (? for help): lookup
Enter ID number: 1
what would you like to know? (name, age, phone) name
Name: windard
Enter command (? for help): lookup
Enter ID number: 1
what would you like to know? (name, age, phone) age
Age: 12
Enter command (? for help): lookup
Enter ID number: 1
what would you like to know? (name, age, phone) phone
Phone: 12345678
Enter command (? for help): ?
The available commands are:
store    : Store information about a person
lookup   : Looks up a person from ID number
quit     : Save changes and exit
?        : Prints this message
Enter command (? for help): quit
```