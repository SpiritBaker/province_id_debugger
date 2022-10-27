
import os
from pathlib import Path


terrain_file_path = Path("map/terrain.txt")
continent_file_path = Path("map/continent.txt")
area_file_path = Path("map/area.txt")
trade_nodes_file_path = Path("common/tradenodes/00_tradenodes.txt")
province_history_path = Path("history/provinces/")
terrain_id = []
continent_id = []
area_id = []
trade_nodes_id = []
terrain_present = False
continent_present = False
area_present = False
trade_nodes_present = False


if terrain_file_path.is_file():
    terrain_present = True
if continent_file_path.is_file():
    continent_present = True
if area_file_path.is_file():
    area_present = True
if trade_nodes_file_path.is_file():
    trade_nodes_present = True
else:
    pass


def terrain_file():
    file_output = []
    start = 'terrain_override = {'
    end = '}'
    path = terrain_file_path
    found_type = False
    with open(path, 'r', encoding='utf8' ) as f:
        for line in f:
            if start in line.strip():
                found_type = True
                continue 

            if found_type:
                if end in line.strip():
                    found_type = False
                else:
                    comment = '#'
                    line = line.split(comment, 1)[0]
                    temp_line = str(line).rstrip('\n').strip().split() 
                    file_output += temp_line
    return file_output


def continent_file():
    file_output = []
    start = '{'
    end = '}'
    path = continent_file_path
    found_type = False
    with open(path, 'r', encoding='utf8' ) as f:
        for line in f:
            if start in line.strip():
                found_type = True
                continue 

            if found_type:
                if end in line.strip():
                    found_type = False
                else:
                    temp_line = str(line).rstrip('\n').strip().split() 
                    file_output += temp_line
    return file_output

    
def area_file():
    file_output = []
    start = '{'
    end = '}'
    path = area_file_path
    found_type = False
    with open(path, 'r', encoding='utf8' ) as f:
        for line in f:
            if start in line.strip():
                found_type = True
                continue 

            if found_type:
                if end in line.strip():
                    found_type = False
                else:
                    comment = '#'
                    line = line.split(comment, 1)[0]
                    temp_line = str(line).rstrip('\n').strip().split() 
                    file_output += temp_line
    return file_output
    

def trade_nodes_file():
    file_output = []
    start = 'members={'
    end = '}'
    path = trade_nodes_file_path
    found_type = False
    with open(path, 'r', encoding='utf8' ) as f:
        for line in f:
            if start in line.strip():
                found_type = True
                continue 

            if found_type:
                if end in line.strip():
                    found_type = False
                else:
                    comment = '#'
                    line = line.split(comment, 1)[0]
                    temp_line = str(line).rstrip('\n').strip().split() 
                    file_output += temp_line
    return file_output


def filter_list(file_output):
    province_id = [token for token in file_output if all(char.isdigit() or char == int for char in token)]
    return province_id


def find_duplicate(province_id):
    duplicate = []
    uniques = []
    for number in province_id:
        if number not in uniques:
            uniques.append(number)
        else:
            duplicate.append(number)
    return duplicate


def province_history_files(province_history_path):
    province_history_names = [f.name for f in os.scandir(province_history_path) if f.is_file()]
    province_history_id = [x[:4] for x in province_history_names]
    province_history_id = [x.replace('-', '').replace(' ', '') for x in province_history_id]
    return province_history_id
    

def missing_province_id(province_history_id,province_id):
    missing_id = list(set(province_history_id).difference(province_id))
    return missing_id


if province_history_path.is_dir():
    province_history_id = province_history_files(province_history_path)
    print("Loading File names from history/provinces/")
    if terrain_present is True:
        file_output = terrain_file()
        province_id = filter_list(file_output)
        missing_province_id(province_history_id, province_id)
        missing_id = missing_province_id(province_history_id, province_id)
        duplicate = find_duplicate(province_id)
        print(f"Terrain.txt Missing id:{missing_id}{os.linesep}Duplicate id:{duplicate}{os.linesep}")
    if continent_present is True:
        file_output = continent_file()
        province_id = filter_list(file_output)
        continent_id = filter_list(file_output)
        duplicate = find_duplicate(province_id)
        missing_province_id(province_history_id, province_id)
        missing_id = missing_province_id(province_history_id, province_id)
        print(f"Continent.txt Missing id: {missing_id}{os.linesep}Duplicate id:{duplicate}{os.linesep}")
    if area_present is True:
        file_output = area_file()
        province_id = filter_list(file_output)
        area_id = filter_list(file_output)
        duplicate = find_duplicate(province_id)
        missing_province_id(province_history_id,province_id)
        missing_id = missing_province_id(province_history_id, province_id)
        print(f"Area.txt Missing id: {missing_id}{os.linesep}Duplicate id:{duplicate}{os.linesep}")
    if trade_nodes_present is True:
        file_output = trade_nodes_file()
        province_id = filter_list(file_output)
        trade_nodes_id = filter_list(file_output)
        duplicate = find_duplicate(province_id)
        missing_province_id(province_history_id, province_id)
        missing_id = missing_province_id(province_history_id, province_id)
        print(f"TradeNodes.txt Missing id: {missing_id}{os.linesep}Duplicate id:{duplicate}{os.linesep}")
    else:
        pass
else:
    if terrain_present is True:
        file_output = terrain_file()
        province_id = filter_list(file_output)
        duplicate = find_duplicate(province_id)
        print(f"Terrain.txt Duplicate id:{duplicate}{os.linesep}")
    if continent_present is True:
        file_output = continent_file()
        province_id = filter_list(file_output)
        continent_id = filter_list(file_output)
        duplicate = find_duplicate(province_id)
        print(f"Continent.txt Duplicate id:{duplicate}{os.linesep}")
    if area_present is True:
        file_output = area_file()
        province_id = filter_list(file_output)
        area_id = filter_list(file_output)
        duplicate = find_duplicate(province_id)
        print(f"Area.txt Duplicate id:{duplicate}{os.linesep}")
    if trade_nodes_present is True:
        file_output = trade_nodes_file()
        province_id = filter_list(file_output)
        trade_nodes_id = filter_list(file_output)
        duplicate = find_duplicate(province_id)
        print(f"TradeNodes.txt Duplicate id:{duplicate}{os.linesep}")

