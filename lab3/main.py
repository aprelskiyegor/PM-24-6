# pip install tabulate

import os
import pickle
import csv
from tabulate import tabulate
from random import randint


loaded_files = {}
saved_tables = {}

#Тест для .pkl
data = [['ID', 'USER', 'PASS'], ['1', 'IVAN', 'jhsfuga612'], ['2', 'KOSTYA', 'EFSFGfj145nb'], ['3', 'ARTEM', 'JHFIGAghHFJ6351']]
with open('pikle.pkl', 'wb') as file:
    pickle.dump(data, file)

#Тест для .csv (у меня работает с delimiter'ом через ',', но если слипляет в 1 ячейку, то заменить на ';').
data = [['ID', 'USER', 'PASS'], ['1', 'IVAN', 'jhsfuga612'], ['2', 'KOSTYA', 'EFSFGfj145nb'], ['3', 'ARTEM', 'JHFIGAghHFJ6351']]

with open('test.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerows(data)

def file_name_extension_checker(file):
    file_path = os.path.basename(file)
    split_path = os.path.splitext(file_path)
    if split_path[-1] == '.txt':
        return (split_path[0], 'txt')
    elif split_path[-1] == '.pkl':
        return (split_path[0], 'pkl')
    elif split_path[-1] == '.csv':
        return (split_path[0], 'csv')
    else:
        return (split_path[0], 'The type of your file is not suitable.')


def types_getter(data_list, types_list):
    for i in range(len(data_list)):
        i_type_list = []
        for j in range(len(data_list[i])):
            el = data_list[i][j]
            if el != None:
                if el.isdigit() == True:
                    i_type_list.append(type(100))
                else:
                    if '.' in el:
                        el = el.replace('.', '')
                        if el.isdigit() == True:
                            i_type_list.append(type(1.0))
                        else:    
                            i_type_list.append(type(el))
                                
                    elif ',' in el:
                        el = el.replace(',', '')
                        if el.isdigit() == True:
                            i_type_list.append(type(1.0))
                        else:
                            i_type_list.append(type(el))
    
                    elif el.lower() == 'true' or el.lower() == 'false':
                        i_type_list.append(type(True))
    
                    else:
                        i_type_list.append(type(el))
            else:
                i_type_list.append(type(el))
                                    
        types_list.append(i_type_list)

    return types_list


def None_csv_pikle_setter(start_list, headers):
    data_list = []
    for i in range(len(start_list)):
        splitted_line = start_list[i]
        if '' in splitted_line:
            while '' in splitted_line:
                index = splitted_line.index('')
                splitted_line[index] = None
                data_list.append(splitted_line)
        else:
            if len(splitted_line) < len(headers):
                diff = len(headers) - len(splitted_line)
                splitted_line.append('None')
                if diff != 1:
                    for i in range(diff-1):
                        splitted_line.append('None')
                for j in range(len(splitted_line)):
                    if splitted_line[j] == 'None':
                        splitted_line[j] = None
                data_list.append(splitted_line)
                                
            else:
                data_list.append(splitted_line)

    return data_list


def load_table(*file):
    files = list(file)

    for file in files:
        file_name, ext = file_name_extension_checker(file=file)
        data_list = []
        types_list = []
        if ext == 'txt':
            with open(file, 'r', encoding='UTF-8') as file:
                headers = file.readline().strip().split(' ')
                line = file.readline().strip()
                while line:
                    splitted_line = line.split(' ')
                    while '' in splitted_line:
                        index = splitted_line.index('')
                        splitted_line[index] = None
                        data_list.append(splitted_line)
                    
                    if len(splitted_line) < len(headers):
                        diff = len(headers) - len(splitted_line)
                        splitted_line.append('None')
                        if diff != 1:
                            for i in range(diff-1):
                                splitted_line.append('None')
                        for j in range(len(splitted_line)):
                            if splitted_line[j] == 'None':
                                splitted_line[j] = None
                        data_list.append(splitted_line)
                        
                    else:
                        data_list.append(splitted_line)
                    
                    line = file.readline().strip()
                
                types_list = types_getter(data_list, types_list)
                
                headers_data_dict = {'headers': headers, 'data': data_list, 'types': types_list}
                new_data = {file_name: headers_data_dict}
            loaded_files.update(new_data)
            
                
        elif ext == 'pkl':
            with open(file, 'rb') as file:
                data = pickle.load(file)

            if type(data) == dict:
                data_list = None_csv_pikle_setter(data['data'], data['headers'])
                headers_data_dict = {'headers': data['headers'], 'data': data_list}

            else:
                types_list = []
                headers = data[0]
                data_list = data[1:]
                
                data_list = None_csv_pikle_setter(data_list, headers)
                
                types_list = types_getter(data_list, types_list)
                
                headers_data_dict = {'headers': headers, 'data': data_list, 'types': types_list}

            new_data = {file_name: headers_data_dict}
            loaded_files.update(new_data)
    
        
        elif ext == 'csv':
            with open(file, 'r', newline='', encoding='UTF-8') as file:
                reader = list(csv.reader(file))

            types_list = []
            headers = reader[0]
            data_list = reader[1:]
            
            data_list = None_csv_pikle_setter(data_list, headers)
            
            types_list = types_getter(data_list, types_list)
                    
            headers_data_dict = {'headers': headers, 'data': data_list, 'types': types_list}
                
            new_data = {file_name: headers_data_dict}
            loaded_files.update(new_data)
    
                
        elif ext == 'The type of your file is not suitable.':
            return ext

    return loaded_files


def save_table(loaded_files=loaded_files, file=None, max_rows=None) -> dict:
    if max_rows == None:
        saved_tables.update(loaded_files)
    else:
        file_name, ext = file_name_extension_checker(file=file)
        if max_rows >= len(loaded_files[file_name]['data']):
            saved_tables.update(loaded_files)
        else:
            files_num = len(loaded_files[file_name]['data']) // max_rows
            if len(loaded_files[file_name]['data']) % max_rows != 0:
                files_num += 1

            start = 0
            for file in range(files_num):
                end = min(max_rows + start, len(loaded_files[file_name]['data']))
                new_data = []
                new_data = [loaded_files[file_name]['headers']]
                if start != end:
                    new_data.extend(loaded_files[file_name]['data'][start:end])
                else:
                    new_data.extend(loaded_files[file_name]['data'][start])
    
                new_file = f'{file+1}_{file_name}.{ext}'
    
                if ext == 'txt':
                    with open(new_file, 'w', encoding='UTF-8') as file:
                        for line in new_data:
                            file.write(' '.join(str(word) for word in line) + '\n')
    
                elif ext == 'pkl':
                    with open(new_file, 'wb') as file:
                        pickle.dump(new_data, file)
    
                elif ext == 'csv':
                    with open(new_file, 'w', newline='', encoding='UTF-8') as file:
                        writer = csv.writer(file, delimiter=',')
                        writer.writerows(new_data)
                        
                start = end
            
    return saved_tables


def print_table(file, loaded_files=loaded_files) -> None:
    file_name, _ = file_name_extension_checker(file)
    if file_name not in loaded_files.keys():
        loaded_files = load_table(file)

    table_txt = tabulate(loaded_files[file_name]['data'], headers=loaded_files[file_name]['headers'], tablefmt='grid')
        
    print(table_txt)


def get_rows_by_number(file, start: int, stop: int, copy_table=False):
    loaded_files = load_table(file)
    file_name, ext = file_name_extension_checker(file=file)
    new_table_list = []
    
    if copy_table == False:
        if ext == 'txt':
            with open(file, 'w', encoding='UTF-8') as file:
                for i in range(start-1, stop):
                    new_table_list.append(loaded_files[file_name]['data'][i])
                new_table_dict = {file_name: {'headers': loaded_files[file_name]['headers'], 'data': new_table_list}}
                file.writelines(f'{i} ' for i in new_table_dict[file_name]['headers'])
                file.write('\n')
                for i in range(len(new_table_list)):
                    file.writelines(f'{j} ' for j in new_table_dict[file_name]['data'][i])
                    file.write('\n')
            print(f'Done. Check the file: {file_name}.{ext}')

        elif ext == 'pkl':
            with open(file, 'wb') as file:
                for i in range(start-1, stop):
                    new_table_list.append(loaded_files[file_name]['data'][i])
                new_table_dict = {file_name: {'headers': loaded_files[file_name]['headers'], 'data': new_table_list}}
                pickle.dump(new_table_dict[file_name], file)
            print(f'Done. Check the file: {file_name}.{ext}')

        elif ext == 'csv':
            with open(file, 'w', newline='') as file:
                new_table_list.append(loaded_files[file_name]['headers'])
                for i in range(start-1, stop):
                    new_table_list.append(loaded_files[file_name]['data'][i])
                new_table_dict = {file_name: {'headers': loaded_files[file_name]['headers'], 'data': new_table_list[1:]}}
                writer = csv.writer(file, delimiter=',')
                writer.writerows(new_table_list)
            print(f'Done. Check the file: {file_name}.{ext}')
           
    elif copy_table == True:
        new_file = 'new_' + file_name + f'.{ext}'
        new_file_name = 'new_' + file_name
        
        if ext == 'txt':
            with open(file, 'r', encoding='UTF-8') as file:
                for i in range(start-1, stop):
                    new_table_list.append(loaded_files[file_name]['data'][i])
                new_table_dict = {new_file_name: {'headers': loaded_files[file_name]['headers'], 'data': new_table_list}}
            with open(new_file, 'w', encoding='UTF-8') as file:
                file.writelines(f'{i} ' for i in new_table_dict[new_file_name]['headers'])
                file.write('\n')
                for i in range(len(new_table_list)):
                    file.writelines(f'{j} ' for j in new_table_dict[new_file_name]['data'][i])
                    file.write('\n')
            print(f'Done. Check the file: {new_file}')

        elif ext == 'pkl':
            with open(file, 'rb') as file:
                for i in range(start-1, stop):
                    new_table_list.append(loaded_files[file_name]['data'][i])
                new_table_dict = {new_file: {'headers': loaded_files[file_name]['headers'], 'data': new_table_list}}
            with open(new_file, 'wb') as file:
                pickle.dump(new_table_dict[new_file_name], file)
            print(f'Done. Check the file: {new_file}')

        elif ext == 'csv':
            with open(file, 'r', newline='') as file:
                new_table_list.append(loaded_files[file_name]['headers'])
                for i in range(start-1, stop):
                    new_table_list.append(loaded_files[file_name]['data'][i])
                new_table_dict = {new_file_name: {'headers': loaded_files[file_name]['headers'], 'data': new_table_list[1:]}}
            with open(new_file, 'w', newline='') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerows(new_table_list)
            print(f'Done. Check the file: {new_file}')
        
    loaded_files.update(new_table_dict)   
    save_table(loaded_files)


def get_rows_by_index(file, *val: int, copy_table=False):
    loaded_files = load_table(file)
    file_name, ext = file_name_extension_checker(file=file)
    new_table_list = []
    vals = list(val)
    
    if copy_table == False:
        if ext == 'txt':
            with open(file, 'w', encoding='UTF-8') as file:
                for i in vals:
                    new_table_list.append(loaded_files[file_name]['data'][i-1])
                new_table_dict = {file_name: {'headers': loaded_files[file_name]['headers'], 'data': new_table_list}}
                file.writelines(f'{i} ' for i in new_table_dict[file_name]['headers'])
                file.write('\n')
                for i in range(len(new_table_list)):
                    file.writelines(f'{j} ' for j in new_table_dict[file_name]['data'][i])
                    file.write('\n')
            print(f'Done. Check the file: {file_name}.{ext}')

        elif ext == 'pkl':
            with open(file, 'wb') as file:
                for i in vals:
                    new_table_list.append(loaded_files[file_name]['data'][i-1])
                new_table_dict = {file_name: {'headers': loaded_files[file_name]['headers'], 'data': new_table_list}}
                pickle.dump(new_table_dict[file_name], file)
            print(f'Done. Check the file: {file_name}.{ext}')

        elif ext == 'csv':
            with open(file, 'w', newline='') as file:
                new_table_list.append(loaded_files[file_name]['headers'])
                for i in vals:
                    new_table_list.append(loaded_files[file_name]['data'][i-1])
                new_table_dict = {file_name: {'headers': loaded_files[file_name]['headers'], 'data': new_table_list[1:]}}
                writer = csv.writer(file, delimiter=',')
                writer.writerows(new_table_list)
            print(f'Done. Check the file: {file_name}.{ext}')
           
    elif copy_table == True:
        new_file = 'new_' + file_name + f'.{ext}'
        new_file_name = 'new_' + file_name
        
        if ext == 'txt':
            with open(file, 'r', encoding='UTF-8') as file:
                for i in range(len(vals)):
                    new_table_list.append(loaded_files[file_name]['data'][i])
                new_table_dict = {new_file_name: {'headers': loaded_files[file_name]['headers'], 'data': new_table_list}}
            with open(new_file, 'w', encoding='UTF-8') as file:
                file.writelines(f'{i} ' for i in new_table_dict[new_file_name]['headers'])
                file.write('\n')
                for i in range(len(new_table_list)):
                    file.writelines(f'{j} ' for j in new_table_dict[new_file_name]['data'][i])
                    file.write('\n')
            print(f'Done. Check the file: {new_file}')

        elif ext == 'pkl':
            with open(file, 'rb') as file:
                for i in vals:
                    new_table_list.append(loaded_files[file_name]['data'][i-1])
                new_table_dict = {new_file_name: {'headers': loaded_files[file_name]['headers'], 'data': new_table_list}}
            with open(new_file, 'wb') as file:
                pickle.dump(new_table_dict[new_file_name], file)
            print(f'Done. Check the file: {new_file}')

        elif ext == 'csv':
            with open(file, 'r', newline='') as file:
                new_table_list.append(loaded_files[file_name]['headers'])
                for i in vals:
                    new_table_list.append(loaded_files[file_name]['data'][i-1])
                new_table_dict = {new_file_name: {'headers': loaded_files[file_name]['headers'], 'data': new_table_list[1:]}}
            with open(new_file, 'w', newline='') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerows(new_table_list)
            print(f'Done. Check the file: {new_file}')

    loaded_files.update(new_table_dict)
    save_table(loaded_files)


def vals_append(vals, loaded_files, file_name):
    vals.append([])
    for i in range(len(loaded_files[file_name]['types'][0]) - 1):
        vals.append([])
    j = 0
    while j != len(loaded_files[file_name]['types'][0]):
        b = 0
        vals_column = []
        while b != len(loaded_files[file_name]['types']):
            vals_column.append(loaded_files[file_name]['types'][b][j])
            b+=1
        vals[j] = vals_column
        j += 1
        
    return vals


def get_column_types(file, by_number=True) -> dict:
    loaded_files = load_table(file)
    file_name, ext = file_name_extension_checker(file=file)
    vals = []
    
    if by_number == True:
        keys = [i for i in range(len(loaded_files[file_name]['headers']))]
        vals = vals_append(vals, loaded_files, file_name)
    
    elif by_number == False:
        keys = [i for i in loaded_files[file_name]['headers']]
        vals = vals_append(vals, loaded_files, file_name)
        
    types_dict = dict(zip(keys, vals))
    return types_dict


def dict_input(types_dict):
    for i in list(types_dict.keys()):
        set_type = str(f"'{input('Set your column type: ')}'")
        if set_type != "''":
            types_dict[i] = '<class ' + set_type + '>'
        else:
            types_dict[i] = None
    return types_dict


def set_column_types(file, by_number=True):
    loaded_files = load_table(file)
    file_name, ext = file_name_extension_checker(file=file)
    
    if by_number == True:
        types_dict = get_column_types(file, by_number=True)
        new_types_dict = dict_input(types_dict)
            
    elif by_number == False:
        types_dict = get_column_types(file, by_number=False)
        new_types_dict = dict_input(types_dict)
    
    print('Setting completed.')
    return new_types_dict


def get_values(file, column=1) -> list:
    loaded_files = load_table(file)
    file_name, ext = file_name_extension_checker(file=file)
    vals = []

    if type(column) == int:
        if len(loaded_files[file_name]['data']) == 1:
            vals = get_value(file_name, column)

        else:
            if column > len(loaded_files[file_name]['headers']):
                raise ValueError('The number of columns is less than the specified number.')
            else:
                for i in range(len(loaded_files[file_name]['data'])):
                    vals.append((loaded_files[file_name]['data'][i][column-1]))

    elif type(column) == str:
        if len(loaded_files[file_name]['data']) == 1:
            vals = get_value(file_name, column)

        else:
            if column not in loaded_files[file_name]['headers']:
                raise ValueError('The specified column is missing.')
            else:
                index = loaded_files[file_name]['headers'].index(column)
                for i in range(len(loaded_files[file_name]['data'])):
                    vals.append((loaded_files[file_name]['data'][i][index]))

    else:
        raise TypeError('Only str or int type.')

    return vals


def get_value(file_name, column=1):
    loaded_files = load_table(file)
    vals = []
    if type(column) == int:
        if column > len(loaded_files[file_name]['headers']):
            raise ValueError('The number of columns is less than the specified number.')
        else:
            vals.append(loaded_files[file_name]['data'][0][column-1])

    elif type(column) == str:
        if column not in loaded_files[file_name]['headers']:
            raise ValueError('The specified column is missing.')
        else:
            index = loaded_files[file_name]['headers'].index(column)
            vals.append(loaded_files[file_name]['data'][0][index])

    else:
        raise TypeError('Only str or int type.')

    return vals


def set_values(file, values: list, column=1):
    file_name, ext = file_name_extension_checker(file=file)
    loaded_files = load_table(file)
    if len(loaded_files[file_name]['data']) == 1:
        loaded_files = set_value(file, values[0], column)
    else:
        for i in range(len(values)):
            loaded_files[file_name]['data'][i][column-1] = values[i]

    loaded_files.update(loaded_files[file_name])
    save_table(loaded_files)


def set_value(file, value, column=1):
    file_name, ext = file_name_extension_checker(file=file)    
    loaded_files = load_table(file)
    loaded_files[file_name]['data'][0][column-1] = value

    return loaded_files


def concat(file1, file2):
    loaded_files = load_table(file1, file2)
    file1_name, ext1 = file_name_extension_checker(file=file1)
    file2_name, ex2 = file_name_extension_checker(file=file2)

    new_table_name = file1_name + '_' + file2_name
    new_headers_list = loaded_files[file1_name]['headers'] + loaded_files[file2_name]['headers']

    new_data_list = []
    for i in range(max(len(loaded_files[file1_name]['data']), len(loaded_files[file2_name]['data']))):
        if len(loaded_files[file1_name]['data']) > len(loaded_files[file2_name]['data']):
            diff = len(loaded_files[file1_name]['data']) - len(loaded_files[file2_name]['data'])
            for j in range(diff):
                loaded_files[file2_name]['data'].append(['-'])
            for j in range(diff):
                loaded_files[file2_name]['data'][j-diff] += ['-']*(len(loaded_files[file2_name]['headers'])-1)
            new_data_list.append(loaded_files[file1_name]['data'][i] + loaded_files[file2_name]['data'][i])

            for j in range(diff):
                loaded_files[file2_name]['data'].pop(j-diff)
        
        elif len(loaded_files[file1_name]['data']) < len(loaded_files[file2_name]['data']):
            diff = len(loaded_files[file2_name]['data']) - len(loaded_files[file1_name]['data'])
            for j in range(diff):
                loaded_files[file1_name]['data'].append(['-'])
            for j in range(diff):
                loaded_files[file1_name]['data'][j-diff] += ['-']*(len(loaded_files[file1_name]['headers'])-1)
            new_data_list.append(loaded_files[file1_name]['data'][i] + loaded_files[file2_name]['data'][i])

            for j in range(diff):
                loaded_files[file1_name]['data'].pop(j-diff)
        
        else:
            new_data_list.append(loaded_files[file1_name]['data'][i] + loaded_files[file2_name]['data'][i])
        
    new_table_dict = {new_table_name: {'headers': new_headers_list, 'data': new_data_list}}

    print(f'Your table {new_table_name} is ready.')
    loaded_files.update(new_table_dict)   
    save_table(loaded_files)


if __name__ == "__main__":
    pass
