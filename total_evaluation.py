import os

def evaluate_everything(input_dir):
    result_file = open("DETAILED_EVALUATION.eval", 'w')
    sleepy_success_counter = 0.0
    sleepy_success_accumulator = 0.0
    epsilon=0.00000000001
    true_positive_accumulator=0.0
    true_positive_counter=0.0
    false_positive_accumulator=0.0
    false_positive_counter=0.0
    true_negative_accumulator=0.0
    true_negative_counter=0.0
    false_negative_accumulator=0.0
    false_negative_counter=0.0

    nonsleepy_success_counter = 0.0
    nonsleepy_success_accumulator = 0.0
    for root, dirs, files in os.walk(input_dir, topdown=False):
        for name in files:
            if (name.endswith("nonsleepyCombination.eval")):
                nonsleepy_success_counter=nonsleepy_success_counter+1
                ns_File = open(os.path.join(root,name), 'r')
                nonsleepy_string=ns_File.read()
                nonsleepy_list=nonsleepy_string.split(" ")
                nonsleepy_success_rate=float(nonsleepy_list[3])
                ns_File.close()
                nonsleepy_success_accumulator=nonsleepy_success_accumulator+nonsleepy_success_rate
                result_file.write(str(os.path.join(root,name) + "\n" + str(nonsleepy_success_rate) + "\n\n" ))

            elif (name.endswith("sleepyCombination.eval")):
                sleepy_success_counter=sleepy_success_counter+1
                true_negative_counter=true_negative_counter+1
                true_positive_counter=true_positive_counter+1
                false_negative_counter=false_negative_counter+1
                false_positive_counter=false_positive_counter+1
                s_File = open(os.path.join(root,name), 'r')
                sleepy_string = s_File.read()
                sleepy_list=sleepy_string.split(" ")
                sleepy_success_rate=float(sleepy_list[15])
                true_positive = float(sleepy_list[3].split("\n")[0])
                true_negative = float(sleepy_list[6].split("\n")[0])
                false_positive = float(sleepy_list[9].split("\n")[0])
                false_negative = float(sleepy_list[12].split("\n")[0])
                true_positive_rate = true_positive / (true_positive+false_positive+epsilon)
                true_negative_rate = true_negative / (true_negative+false_negative+epsilon)
                false_positive_rate = false_positive / (true_positive+false_positive+epsilon)
                false_negative_rate = false_negative / (true_negative+false_negative+epsilon)
                s_File.close()
                sleepy_success_accumulator = sleepy_success_accumulator + sleepy_success_rate
                true_positive_accumulator = true_positive_accumulator + true_positive_rate
                true_negative_accumulator = true_negative_accumulator + true_negative_rate
                false_positive_accumulator = false_positive_accumulator + false_positive_rate
                false_negative_accumulator = false_negative_accumulator + false_negative_rate
                result_file.write(str(os.path.join(root, name) + "\n" + str(sleepy_success_rate) + "\n\n" ))
            else:
                pass

    result_file.write ("MEAN NONSLEEPY SUCCESS RATE = " + str(nonsleepy_success_accumulator / nonsleepy_success_counter))
    result_file.write ("\n" + "MEAN SLEEPY SUCCESS RATE = " + str(sleepy_success_accumulator / sleepy_success_counter))
    result_file.write("\n" + "MEAN TPR = " + str(true_positive_accumulator / true_positive_counter))
    result_file.write("\n" + "MEAN FPR = " + str(false_positive_accumulator / false_positive_counter))
    result_file.write("\n" + "MEAN TNR = " + str(true_negative_accumulator / true_negative_counter))
    result_file.write("\n" + "MEAN FNR = " + str(false_negative_accumulator / false_negative_counter))

    print ("MEAN NONSLEEPY SUCCESS RATE = " + str(nonsleepy_success_accumulator / nonsleepy_success_counter))
    print ("MEAN SLEEPY SUCCESS RATE = " + str(sleepy_success_accumulator / sleepy_success_counter))
    print ("MEAN TPR = " + str(true_positive_accumulator / true_positive_counter))
    print ("MEAN FPR = " + str(false_positive_accumulator / false_positive_counter))
    print ("MEAN TNR = " + str(true_negative_accumulator / true_negative_counter))
    print ("MEAN FNR = " + str(false_negative_accumulator / false_negative_counter))
    result_file.close()
evaluate_everything('C:\\Users\\Mert\\Dropbox\\ITU\\2017 BITIRME\\DATASETS\\COMPOUND_DATASET')