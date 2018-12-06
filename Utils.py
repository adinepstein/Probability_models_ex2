


def read_data_from_file(file_path):
    with open(file_path) as f:
        lines= f.readlines()
    f.close()
    desired_lines=lines[3::4]
    return desired_lines


def insert_events_to_list(lines):
    event_list=[]
    for line in lines:
        line=line.strip().split()
        for event in line:
            event_list.append(event)
    return event_list

def split_data_list(train_percentage,data_list):
    size=len(data_list)
    train_size=round(train_percentage*size);
    train_data=data_list[:train_size]
    validation_data=data_list[train_size:]
    return train_data,validation_data

def set_event_frequency(data_list):
    event_frequency={}
    for event in data_list:
        if event in event_frequency:
            event_frequency[event]+=1
        else:
            event_frequency[event]=1
    return event_frequency