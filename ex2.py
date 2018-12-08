
import math



VOCABULARY_SIZE=300000
LIDSTONE_TRAIN_PERCENTAGE = 0.9
HELD_TRAIN_PERCENTAGE = 0.5
WORD_NOT_IN_TRAIN = '__WORD_NOT_IN_TRAIN__'


def main(dev_set_filename,test_set_filename,input_word,output_filename):
    # organize data
    init_output_file(dev_set_filename,test_set_filename,input_word,output_filename)
    lines=read_data_from_file(dev_set_filename)
    events=insert_events_to_list(lines)
    # Lidstone part
    train_list,validation_list=split_data_list(LIDSTONE_TRAIN_PERCENTAGE,events)
    train_freq = set_event_frequency(train_list)
    preprocessing(events,train_list,validation_list,train_freq,input_word,output_filename)
    prep_min, best_lambda = get_best_preplixity(train_freq, train_list, 0.01, 2, 0.01, validation_list)
    lidstone_output(train_freq,train_list,validation_list,input_word,output_filename,prep_min,best_lambda)
    # Held out part
    T_list,H_list=split_data_list(HELD_TRAIN_PERCENTAGE,events)
    T_freq=set_event_frequency(T_list)
    H_freq = set_event_frequency(H_list)
    T_freq_event_dic=get_freq_event_dic(T_freq)
    held_out_word_prob=calculate_held_out_prob(input_word,T_freq,H_freq,H_list,T_freq_event_dic)
    held_out_unseen_prob = calculate_held_out_prob("__unseen_word__",T_freq,H_freq,H_list,T_freq_event_dic)
    held_out_output(T_list,H_list,output_filename,held_out_word_prob,held_out_unseen_prob)
    #check sum prob
    event_prob=lidstone_calculation(train_freq,train_list,best_lambda)
    print(check_event_probability_sum(event_prob))
    print(check_held_out_prop_sum(T_freq,H_freq,H_list,T_freq_event_dic,held_out_unseen_prob))
    # test set evalutation
    test_lines=read_data_from_file(test_set_filename)
    test_events=insert_events_to_list(test_lines)
    prep_lid = calculate_lidstone_preplixity(train_freq, train_list, best_lambda, test_events)
    prep_held = calcualte_held_out_preplexity(T_freq,H_freq,H_list,T_freq_event_dic,test_events)
    best_prep= 'L'
    if prep_held<prep_lid:
        best_prep = 'H'
    test_evaluation_output(output_filename,test_events,prep_lid,prep_held,best_prep)
    write_table_result(output_filename,train_freq,train_list,event_prob,T_list,T_freq,H_freq,H_list,T_freq_event_dic)







def init_output_file(dev_filename,test_file_name,input_word,output_filename):
    with open(output_filename,'w') as f:
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
    if input_word in train_dic:
        freq=train_dic[input_word]
    else:
        freq=0
    with open(output_filename, 'a') as f:
        f.write("#Output7   " + str(events_size) + "\n")
        f.write("#Output8   " + str(val_size) + "\n")
        f.write("#Output9   " + str(train_size) + "\n")
        f.write("#Output10   " + str(train_dic_size) + "\n")
        f.write("#Output11   " + str(freq) + "\n")
    f.close()

def lidstone_output(train_freq,train_list,validation_list,input_word,output_filename,prep_min,best_lambda):
    mle_no_smoothing=0
    if input_word in train_freq:
        mle_no_smoothing = train_freq[input_word]
    event_prop= lidstone_calculation(train_freq,train_list,0.1)
    mle_smoothing= get_smoothing_mle(event_prop,input_word)
    mle_unseen_word= event_prop[WORD_NOT_IN_TRAIN]
    prep1 = calculate_lidstone_preplixity(train_freq,train_list,0.01,validation_list)
    prep2 = calculate_lidstone_preplixity(train_freq, train_list, 0.1, validation_list)
    prep3 = calculate_lidstone_preplixity(train_freq, train_list, 1, validation_list)
    with open(output_filename, 'a') as f:
        f.write("Output12   " + str(mle_no_smoothing) + "\n")
        f.write("Output13   " + str(0) + "\n")
        f.write("Output14   " + str(mle_smoothing) + "\n")
        f.write("Output15   " + str(mle_unseen_word) + "\n")
        f.write("Output16   " + str(prep1) + "\n")
        f.write("Output17   " + str(prep2) + "\n")
        f.write("Output18   " + str(prep3) + "\n")
        f.write("Output19   " + str(best_lambda) + "\n")
        f.write("Output20   " + str(prep_min) + "\n")
    f.close()

def held_out_output(T_list,H_list,output_filename,word_prob,unseen_prob):
    with open(output_filename, 'a') as f:
        f.write("Output21   " + str(len(T_list)) + "\n")
        f.write("Output22   " + str(len(H_list)) + "\n")
        f.write("Output23   " + str(word_prob) + "\n")
        f.write("Output24   " + str(unseen_prob) + "\n")
    f.close()

def test_evaluation_output(output_filename,test_events,prep_lid,prep_held,best_prep):
    with open(output_filename, 'a') as f:
        f.write("Output25   " + str(len(test_events)) + "\n")
        f.write("Output26   " + str(prep_lid) + "\n")
        f.write("Output27   " + str(prep_held) + "\n")
        f.write("Output28   " + best_prep + "\n")
    f.close()

def write_table_result(output_filename,train_freq,train_list,event_prob,T_list,T_freq,H_freq,H_list,t_freq_event_dic):
    size_lid_train=len(train_list)
    size_held_train=len(T_list)
    f=open(output_filename, 'a')
    f_lambda = get_smoothing_mle(event_prob, "__unseen_word__") * size_lid_train
    f_H = calculate_held_out_prob("__unseen_word__",T_freq,H_freq,H_list,t_freq_event_dic)* size_held_train
    N_0 = VOCABULARY_SIZE - (len(T_freq) - 1)
    t_0= calculate_t0(T_freq,H_freq)
    f.write(str(0) + "  " +  str(round(f_lambda,5)) + " " + str(round(f_H,5))+ "    " + str(N_0) + "    " + str(t_0) + "\n")
    for i in range(1,10):
        f_lambda= get_smoothing_mle(event_prob,find_word_with_r_freq(train_freq,i))*size_lid_train
        f_H= calculate_held_out_prob(find_word_with_r_freq(T_freq,i),T_freq,H_freq,H_list,t_freq_event_dic)* size_held_train
        t_r= calcualte_t_r(t_freq_event_dic,H_freq,i)
        N_r = len(t_freq_event_dic[i])
        f.write(str(i) + "  " +  str(round(f_lambda,5)) + " " + str(round(f_H,5))+ "    " + str(N_r) + "    " + str(t_r) +"\n")
    f.close()

def find_word_with_r_freq(freq_dic,r):
    for event in freq_dic:
        if freq_dic[event]==r:
            return event

def get_smoothing_mle(event_prop,input_word):
    if input_word in event_prop:
        mle= event_prop[input_word]
    else:
        mle = event_prop[WORD_NOT_IN_TRAIN]
    return mle

def lidstone_calculation(train_freq,train_list,lambda_var):
    event_probability={}
    train_size=len(train_list)
    for event in train_freq:
        probability= (train_freq[event] + lambda_var) / (train_size + (lambda_var*VOCABULARY_SIZE))
        event_probability[event]=probability
    event_probability[WORD_NOT_IN_TRAIN]= lambda_var / (train_size + (lambda_var*VOCABULARY_SIZE))
    return event_probability

def check_event_probability_sum(event_probability):
    sum_prob=0
    for event in event_probability:
        sum_prob+= event_probability[event]
    words_not_in_train= VOCABULARY_SIZE- len(event_probability)
    sum_prob += words_not_in_train * event_probability[WORD_NOT_IN_TRAIN]
    print(sum_prob)
    if sum_prob==1:
        return True
    else:
        return False

def check_held_out_prop_sum(T_freq,H_freq,H_list,t_freq_event_dic,unseen_word_prob):
    sum=0
    for freq in t_freq_event_dic:
        prob= calculate_held_out_prob(t_freq_event_dic[freq][0],T_freq,H_freq,H_list,t_freq_event_dic)
        N_r = len(t_freq_event_dic[freq])
        sum+=N_r* prob
    N_0 = VOCABULARY_SIZE -(len(T_freq)-1)
    sum += N_0 * unseen_word_prob
    print (sum)
    if sum==1:
        return True
    else:
        return False


def calculate_preplixity_total_lidstone(train_prob,validation_list):
    multiple = 1
    for val in validation_list:
        if val in train_prob:
            p=train_prob[val]
        else:
            p=train_prob[WORD_NOT_IN_TRAIN]
        multiple+= math.log(p)
    multiple /= -len(validation_list)
    multiple = 2** multiple
    return multiple

def calculate_lidstone_preplixity(train_freq,train_list,lambda_var,test_list):
    event_prob=lidstone_calculation(train_freq,train_list,lambda_var)
    preplixity= calculate_preplixity_total_lidstone(event_prob,test_list)
    return preplixity

def get_best_preplixity(train_freq,train_list,min_lamba,max_lambda,jump,validatoin_list):
    min_prep=100000000
    best_lambda=0
    for l in frange(min_lamba,max_lambda,jump):
        prep=calculate_lidstone_preplixity(train_freq,train_list,l,validatoin_list)
        if(prep<min_prep):
            min_prep=prep
            best_lambda=l
    return min_prep,best_lambda

def frange(x, y, jump):
    while x < y:
        yield round(x,2)
        x += jump

def get_freq_event_dic(data_freq):
    freq_event_dic= {}
    for event in data_freq:
        freq=data_freq[event]
        if freq in freq_event_dic:
            freq_event_dic[freq].append(event)
        else:
            list=[event]
            freq_event_dic[freq]= list
    return freq_event_dic

def calcualte_t_r(freq_event_dic,H_freq,r):
    sum=0
    if r in freq_event_dic:
        list= freq_event_dic[r]
        for event in list:
            if event in H_freq:
                sum+=H_freq[event]
    return sum
def calculate_held_out_prob(input_word,T_freq,H_freq,H_list,t_freq_event_dic):
    if input_word in T_freq:
        r= T_freq[input_word]
        t_r= calcualte_t_r(t_freq_event_dic,H_freq,r)
        N_r= len(t_freq_event_dic[r])
    else:
        t_r=calculate_t0(T_freq,H_freq)
        N_r = VOCABULARY_SIZE -(len(T_freq)-1)
    prob = t_r / (N_r * len(H_list))
    return prob

def calcualte_held_out_preplexity(T_freq,H_freq,H_list,t_freq_event_dic,test_list):
    multiple =1
    for event in test_list:
        p=calculate_held_out_prob(event,T_freq,H_freq,H_list,t_freq_event_dic)
        multiple += math.log(p)
    multiple /= -len(test_list)
    multiple = 2 ** multiple
    return multiple

def calculate_t0(T_freq,H_freq):
    sum=0
    for event in H_freq:
        if event in T_freq:
            pass
        else:
            sum+= H_freq[event]
    return sum

def read_data_from_file(file_path):
    with open(file_path) as f:
        lines= f.readlines()
    f.close()
    desired_lines=lines[2::4]
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
        event_frequency[WORD_NOT_IN_TRAIN]=0
    return event_frequency

if __name__ == '__main__':
    main("develop.txt","test.txt","honduras","output.txt")
