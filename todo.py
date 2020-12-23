import click, fileinput, sys,os,datetime


@click.command()
@click.argument('name', default='')
@click.argument('values', default= '', type= str)


def main(name,values):
    number = 1
    is_skipped = False
    number_of_lines = 0

    f = open(r'C:/Users/SparkySmith/projectCli/todo.txt','r')
    content = f.read()
    coList = content.split("\n")

    for i in coList:
        if i :
            number += 1
        elif is_skipped == True:
            number -= 1 
        else:
            number = 1



    if name == 'help' or name == '':
        click.echo('''Usage :-
$ ./todo add "todo item"  # Add a new todo
$ ./todo ls               # Show remaining todos
$ ./todo del NUMBER       # Delete a todo
$./todo done NUMBER       # Complete a todo
$ ./todo help             # Show usage
$ ./todo report           # Statistics
        ''')
    
    if name == 'add' and values == '':
        print("Error: missing todo after 'add'.")
    elif name == 'add' and values != '':
        click.echo(f"Added todo: \"{values}\"")
        values = f'[{number}] ' + values
        
        file_name = 'C:/Users/SparkySmith/projectCli/todo.txt'
        dummy_file = file_name + '.bak'
        
        with open(file_name,'r')as f, open(dummy_file,'w') as df:
            # deleting the first \n for not creating an extra line
            if os.path.getsize(file_name) == 0:
                #write given line to the dummy file without \n
                df.write(values)
                
            else:
                df.write(values + '\n')
                
            #Read lines from original file one by one and append them to the dummy file
            for line in f:
                df.write(line)

        #remove original file
        os.remove(file_name)
        #rename dummy file as original file
        os.rename(dummy_file,file_name)
        
         
    
      

    if name == 'ls':
        file_name = 'C:/Users/SparkySmith/projectCli/todo.txt'
        file_size = os.path.getsize(file_name)
        if file_size == 0:
            click.echo('The List is Empty!')
        else:
            with open(file_name,'r') as f: 
                print(f.read())
            
        
    
   
    #if the method is del or done
    if name == 'done' or name == 'del':
    
        file_name = 'C:/Users/SparkySmith/projectCli/todo.txt'
        dummy_file = file_name + '.bak'
        done_file = 'C:/Users/SparkySmith/projectCli/done.txt'

        #getting the number of lines in the file
        with open(file_name,'r') as f:
            for line in f.readlines():
                number_of_lines += 1

        file_size = os.path.getsize(file_name)

            
        if name == 'del':
            if values == '':
                click.echo("Error: No arguments added after method")
            elif file_size == 0 or int(values) > number_of_lines:
                click.echo(f"Error: todo #{values} doesn't exit. Nothing Deleted.")
            
        elif name == 'done':
            if values == '' or values == ' ' or values == "   ":
                click.echo("Error: No arguments added after method")
            elif file_size == 0 or int(values) > number_of_lines :
                click.echo(f"Error: todo #{values} doesn't exit.")
            

        #index for updating the line in files
        index = number_of_lines
        update_index = 0

        
        with open(file_name,'r')as f, open(dummy_file,'w') as df, open(done_file,'a') as done:
            
            # Line by line copy data from original file to dummy file
            for line in f:
                # if current line number matches the given line number then skip copying  
                if index == int(values): 
                    is_skipped = True
                    
                    #update the line in done.txt
                    update_array = line.split(' ')
                    
                    update_array[0] = f'[{number_of_lines-1}]'
                    
                    line = ' '.join(update_array)
                
                    if name == 'del':
                        click.echo(f'Deleted todo #{values}')                    
                    elif name == 'done':
                        click.echo(f'Marked todo #{values} as done.')

                        now = datetime.datetime.now()
                        date = f'{now.year}' + '-' + f'{now.month}' + '-' + f'{now.day}'
                        update_array = line.split(' ')
            
                        update_array[0] = 'x' + ' ' + date + ' '
                                        
                        line = ' '.join(update_array)

                        done.write(line)

                else:
                
                    #updating the line number in done.txt
                    update_array = line.split(' ')
                
                    if index > int(values):
                        update_array[0] = f'[{index-1}]'
                    else:
                        update_array[0] = f'[{index}]'

                    line = ' '.join(update_array)
                    
                    df.write(line)
                
                index -= 1
     

        if is_skipped:
            os.remove(file_name)
            os.rename(dummy_file, file_name)

        else:
            os.remove(dummy_file)


    if name == 'report':

        lines_in_todo = 0
        lines_in_done = 0

        todo_file = 'C:/Users/SparkySmith/projectCli/todo.txt'
        done_file = 'C:/Users/SparkySmith/projectCli/done.txt'

        with open(todo_file, 'r') as tf, open(done_file, 'r') as df:
            for line in tf.readlines():
                lines_in_todo += 1
            for line in df.readlines():
                lines_in_done += 1

        now = datetime.datetime.now()
        date = f'{now.year}' + '-' + f'{now.month}' + '-' + f'{now.day}'
                        
        if lines_in_done == 0:
            click.echo(f'{date} Pending : {lines_in_todo} Completed : {lines_in_done}')
        else:   
            click.echo(f'{date} Pending : {lines_in_todo} Completed : {lines_in_done}')




if __name__ == '__main__':
    main()