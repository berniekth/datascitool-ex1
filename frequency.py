import sys
import json;
import string;

def main():
    tweet_file = open(sys.argv[1])
    
    # scan output streams
    line_cnt = 0;
    my_dict = [];
    ctrl_ch = "";
    ctrl_i = 1;
    occurrence_map = {};
    word_cnt = 0;

    # build punctuation and control character tables
    punct_ch = set(string.punctuation);
    while (ctrl_i < 0x20):
        ctrl_ch += chr(ctrl_i);
        ctrl_i += 1;

    # process tweet file
    for line in tweet_file:
        if (line_cnt > 0):
            json_dict = json.loads(line);
            if "text" in json_dict:
                utf8_dict = json_dict["text"].encode("ascii", "ignore");  # or pure "ascii"
                clean_dict = "".join(ch for ch in utf8_dict if ch not in punct_ch).translate(None, ctrl_ch);
                split_dict = clean_dict.lower().split(" ");
                my_dict = filter(None, split_dict);  # remove empty strings in the list
        for word in my_dict:
            try:
                occurrence_map[word] += 1;
            except KeyError:
                occurrence_map[word] = 1;
                continue;
            word_cnt += 1;
        line_cnt += 1;

    # print occurrence_map
    for word in occurrence_map:
        print "%s %f: (%d/%d)" % (word, occurrence_map[word]/float(word_cnt), occurrence_map[word], word_cnt);

if __name__ == '__main__':
    main()
