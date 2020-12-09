from csv import reader
def agent_test():
    # read csv file as a list of lists
    with open('q_table.csv', 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Pass reader object to list() to get a list of lists
        q_table = list(csv_reader)
        #print(q_table)
    #for episodes in range(3):
        
    pass

agent_test()