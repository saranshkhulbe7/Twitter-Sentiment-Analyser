import matplotlib.pyplot as plt                                                             #Importing Modules
import pandas as pd

punctuation_chars = ["'", '"', ",", ".", "!", ":", ";", '#', '@']      

def strip_punctuation(word):                                                                #strip_punctuation() Removes Punctuators In A Particular Word
    for c in word:
        if c in punctuation_chars:
            word = word.replace(c,"")
    return word
    
positive_words = []        #List Of All Positive Words
with open("positive_words.txt") as pos_f:
    for lin in pos_f:
        positive_words.append(lin.strip())
def get_pos(s):                                                                             #get_pos() Gives The Count Of Positive Words In A String Of Text
    s = s.lower()
    count = 0
    words = s.split()
    for word in words:
        word = strip_punctuation(word)
        if word in positive_words:
            count = count + 1
    return count

negative_words = []       #List Of All Negative Words
with open("negative_words.txt") as pos_f:
    for lin in pos_f:
        negative_words.append(lin.strip())
def get_neg(s):                                                                             #get_neg() Gives The Count Of Negative Words In A String Of Text
    s = s.lower()
    count = 0
    words = s.split()
    for word in words:
        word = strip_punctuation(word)
        if word in negative_words:
            count = count + 1
    return count

raw_csv_file = "Donald_J_Trump_Twitter_Data.csv"
result_csv_file = raw_csv_file[:-4] + "_result.csv"
ptdr = open(raw_csv_file,"r")
rd = open(result_csv_file,'w')
lines = ptdr.readlines()
rd_header = "Number of Retweets,Number of Replies,Positive Score,Negative Score,Net Score"
total_positive = 0                                                                          #Counter For All Postive Words In All The Tweets So Far
total_negative = 0                                                                          #Counter For All Negative Words In All The Tweets So Far
total_positive_impact = 0
total_negative_impact = 0                                                                         
for i in range(len(lines)):
    if i == 0:
        rd.write(rd_header)
        rd.write("\n")
    else:
        line = lines[i]
        line = line.strip()
        line_content_list = line.split(",")
        Nrt = line_content_list[1]
        Nrp = line_content_list[2]
        pos_count = get_pos(line_content_list[0])
        total_positive = total_positive + pos_count
        total_positive_impact = total_positive_impact + pos_count * int(Nrt)
        neg_count = get_neg(line_content_list[0])
        total_negative = total_negative + neg_count
        total_negative_impact = total_negative_impact + neg_count * int(Nrt)
        net_score = pos_count - neg_count
        row_string = "{},{},{},{},{}".format(Nrt,Nrp,pos_count,neg_count,net_score)
        rd.write(row_string)
        rd.write("\n")
        
d = pd.read_csv(result_csv_file)                                                                    #Plotting Scatter Plot
Nrt = d["Number of Retweets"]
Net = d["Net Score"]
plt.xlabel("Net Sentiment Score")
plt.ylabel("Number of Retweets")
plt.scatter(Net, Nrt)
plt.title("Sentiment Analysis")
plt.show()

pie_data1 = [total_positive,total_negative]                                                          #Plotting Pie Chart
Sentiments = ["%Positive Sentiments","%Negative Sentiments"]
explode = (0.1, 0)
colors1 = ["yellowgreen", 'lightcoral']
fig = plt.figure(figsize =(10, 7)) 
plt.pie(pie_data1, labels = Sentiments,shadow = True,autopct='%1.2f%%',explode=explode,colors = colors1)

colors2 = ["green", 'coral']
pie_data2 = [total_positive_impact,total_negative_impact]
Impacts = ["%Positive Impact On People","%Negative Impact On People"]
fig = plt.figure(figsize =(10, 7)) 
plt.pie(pie_data2, labels = Impacts,shadow = True,autopct='%1.2f%%',explode=explode,colors = colors2)
