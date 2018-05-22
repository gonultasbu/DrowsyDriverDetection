import os

def evaluate_everything(input_dir):
    result_file = open("DETAILED_EVALUATION.eval", 'w')
    sleepy_success_counter = 0.0
    sleepy_success_accumulator = 0.0

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
                s_File = open(os.path.join(root,name), 'r')
                sleepy_string = s_File.read()
                sleepy_list=sleepy_string.split(" ")
                sleepy_success_rate=float(sleepy_list[15])
                s_File.close()
                sleepy_success_accumulator = sleepy_success_accumulator + sleepy_success_rate
                result_file.write(str(os.path.join(root, name) + "\n" + str(sleepy_success_rate) + "\n\n" ))
            else:
                pass

    result_file.write ("TOTAL NONSLEEPY SUCCESS RATE = " + str(nonsleepy_success_accumulator / nonsleepy_success_counter))
    result_file.write ("\n" + "TOTAL SLEEPY SUCCESS RATE = " + str(sleepy_success_accumulator / sleepy_success_counter))
    print ("TOTAL NONSLEEPY SUCCESS RATE = " + str(nonsleepy_success_accumulator / nonsleepy_success_counter))
    print ("TOTAL SLEEPY SUCCESS RATE = " + str(sleepy_success_accumulator / sleepy_success_counter))

    result_file.close()
evaluate_everything('C:\\Users\\Mert\\Dropbox\\ITU\\2017 BITIRME\\DATASETS\\COMPOUND_DATASET')