import sys
import json;
import string;

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    #hw()
    #lines(sent_file)
    #lines(tweet_file)
	
	# build dictionary from AFINN-111.txt
    AFINN_scores = {};
    for line in sent_file:
        term, score = line.split("\t");
        AFINN_scores[term] = int(score);

    # build Non-AFINN dictionary
    NAFFIN_scores = {};

    # scan output streams
    count = 0;
    line_score = 0;
    my_dict = [];
    ctrl_ch = "";
    ctrl_i = 1;
    word_list = [];
    decode_flag = "ascii";

    # build punctuation and control character tables
    punct_ch = set(string.punctuation);
    while (ctrl_i < 0x20):
        ctrl_ch += chr(ctrl_i);
        ctrl_i += 1;

    # process tweet file
    for line in tweet_file:
        #print "line", count+1, ":";
        if (count > 0):
            json_dict = json.loads(line);
            if "text" in json_dict:
                decode_dict = json_dict["text"].encode(decode_flag, "ignore");
                clean_dict = "".join(ch for ch in decode_dict if ch not in punct_ch).translate(None, ctrl_ch);
                split_dict = clean_dict.lower().split(" ");
                my_dict = filter(None, split_dict);  # remove empty strings in the list
                #print my_dict;
        for word in my_dict:
            try: # word in AFINN dictionary
                line_score += AFINN_scores[word];
                #print word, AFINN_scores[word];
            except KeyError: # word NOT in AFINN dictionary
                # create temp non-AFINN dictionary
                # {"word": [pos_cnt, neg_cnt, tot_cnt]}
                word_list.append(word);
                continue;

        count += 1;
        #print line_score;

        # merge NAFFIN dictionaries
        for word in word_list:
            try:
                cnt = NAFFIN_scores[word];
                if (line_score > 0): # increment pos_cnt
                    NAFFIN_scores[word][0] += 1;
                elif (line_score < 0): # increment neg_cnt
                    NAFFIN_scores[word][1] += 1;
                #else: # no positive or negative sentiment in the tweet
                NAFFIN_scores[word][2] += 1; # increment tot_cnt
                #print word, NAFFIN_scores[word];
            except KeyError:
                if (line_score > 0): # increment pos_cnt
                    NAFFIN_scores[word] = [1,0,1];
                elif (line_score < 0): # increment neg_cnt
                    NAFFIN_scores[word] = [0,1,1];
                else: # no positive or negative sentiment in the tweet
                    NAFFIN_scores[word] = [0,0,1];
                #print word, NAFFIN_scores[word];
                continue;
        
        line_score = 0;  # reset line score
        word_list = [];  # reset temp NAFINN dict

    # calculate opinion sentiment
    for word in NAFFIN_scores:
        # increment all counts by 1 to avoid division by 0
        NAFFIN_scores[word][0] += float(1);
        NAFFIN_scores[word][1] += float(1);
        NAFFIN_scores[word][2] += float(1);

        frequency = (NAFFIN_scores[word][0]/NAFFIN_scores[word][2]) / (NAFFIN_scores[word][1]/NAFFIN_scores[word][2]);
        print_sentiment(word, frequency);

def print_sentiment(word, freq):
    sentiment = "POSITIVE" if freq > 1 else "NEGATIVE" if freq < 1 else "NEUTRAL";
    print "(%s: %s, %s)" % (sentiment, word, str(freq));

if __name__ == '__main__':
    main()
