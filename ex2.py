import Utils



VOCABULARY_SIZE=300000
TRAIN_PERCENTAGE = 0.9
WORD_NOT_IN_TRAIN = '__WORD_NOT_IN_TRAIN__'


def main(dev_set_filename,test_set_filename,input_word,output_filename):
    init_output_file(dev_set_filename,test_set_filename,input_word,output_filename)
    lines=Utils.read_data_from_file(dev_set_filename)
    events=Utils.insert_events_to_list(lines)
    train_list,validation_list=Utils.split_data_list(TRAIN_PERCENTAGE,events)
    train_dic = Utils.set_event_frequency(train_list)
    preprocessing(events,train_list,validation_list,train_dic,input_word,output_filename)







def init_output_file(dev_filename,test_file_name,input_word,output_filename):
    with open(output_filename,'a') as f:
        f.write("#Students	Aviad Fux	Adin Epstein	302593421	021890876\n")
        f.write("#Output1   " + dev_filename + "\n")
        f.write("#Output2   " + test_file_name + "\n")
        f.write("#Output3   " + input_word + "\n")
        f.write("#Output4   " + output_filename + "\n")
        f.write("#Output5   " + str(VOCABULARY_SIZE) + "\n")
        f.write("#Output6   " + str(1/VOCABULARY_SIZE) + "\n")
    f.close()


def preprocessing(events,train_list,validation_list,train_dic,input_word,output_filename):
    events_size=len(events)
    train_size= len(train_list)
    val_size= len(validation_list)
    train_dic_size= len(train_dic)
    with open(output_filename, 'a') as f:
        f.write("#Output7   " + str(events_size) + "\n")
        f.write("#Output8   " + str(val_size) + "\n")
        f.write("#Output9   " + str(train_size) + "\n")
        f.write("#Output10   " + str(train_dic_size) + "\n")
        f.write("#Output11   " + str(train_dic[input_word]) + "\n")
    f.close()

def lidstone_calculation(train_dic,train_list,lambda_var):
    event_probability={}
    train_size=len(train_list)
    for event in train_dic:
        probability= (train_dic[event] + lambda_var) / (train_size + (lambda_var*VOCABULARY_SIZE))
        event_probability[event]=probability
    event_probability[WORD_NOT_IN_TRAIN]= lambda_var / (train_size + (lambda_var*VOCABULARY_SIZE))
    return event_probability

def check_event_probability(event_probability):
    sum_prob=0
    for event in event_probability:
        sum_prob+= event_probability[event]
    words_not_in_train= VOCABULARY_SIZE- len(event_probability)
    sum_prob += words_not_in_train * event_probability[WORD_NOT_IN_TRAIN]
    if sum_prob==1:
        return True
    else:
        return False


