import manager

if __name__ == '__main__':
    user = ''
    while user == '':
        user = input('id? ')

    updateTime = -1
    while type(updateTime) != int or updateTime < 0:
        try:
            updateTime = int(input('updateTime? '))
        except ValueError as e: 
            print(e)

    manager.run(user, updateTime)
