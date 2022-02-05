def create_function(type):

    if type == 'haha':
        def return_func():
            print('haha')
    else:
        def return_func():
            print('not funny')

    return return_func


func = create_function('dfadf')

func()