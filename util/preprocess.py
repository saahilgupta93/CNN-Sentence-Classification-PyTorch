import os
import tarfile
import zipfile
from six.moves.urllib import request
import re 

class MovieReview():
    """
        Handling movie review dataset
        
        Dataset
            Movie Review Data
            Available at : http://www.cs.cornell.edu/people/pabo/movie-review-data/
        
        Example
            >> MR = MovieReview()
            >> MR.raw_data["pos"][:10] # get 10 examples
    """
    def __init__(self):
        """
            Download dataset and parsing it
        """
        if not os.path.exists("./data/"):
            os.makedirs("./data/")
        self.download_file("http://www.cs.cornell.edu/people/pabo/movie-review-data/rt-polaritydata.tar.gz","./data/rt-polaritydata.tar.gz")
        self.extract_file("./data/rt-polaritydata.tar.gz")
        self.raw_data = dict()
        self.raw_data["pos"] = self.get_pos_data("./data/rt-polaritydata/rt-polarity.pos")
        self.raw_data["neg"] = self.get_neg_data("./data/rt-polaritydata/rt-polarity.neg")

    def download_file(self, url, path):
        """
            Downlaod file at path
        """
        if not os.path.exists(path):
            request.urlretrieve(url, path)     

    def extract_file(self, path, to_directory="./data/"):
        """
            Extract file
        """
        if path.endswith('.zip'):
            opener, mode = zipfile.ZipFile, 'r'
        elif path.endswith('.tar.gz') or path.endswith('.tgz'):
            opener, mode = tarfile.open, 'r:gz'
        elif path.endswith('.tar.bz2') or path.endswith('.tbz'):
            opener, mode = tarfile.open, 'r:bz2'
        else: 
            raise (ValueError, "Could not extract `%s` as no appropriate extractor is found" % path)

        file = opener(path, mode)
        try: 
            file.extractall(path = to_directory)
        finally: 
            file.close()
            
    def clean_str(self, string):
        """
            Cleaning string
        """
        # Original : https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
        # Tips for handling string in python : http://agiantmind.tistory.com/31
        string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
        string = re.sub(r"\'s", " \'s", string)
        string = re.sub(r"\'ve", " \'ve", string)
        string = re.sub(r"n\'t", " n\'t", string)
        string = re.sub(r"\'re", " \'re", string)
        string = re.sub(r"\'d", " \'d", string)
        string = re.sub(r"\'ll", " \'ll", string)
        string = re.sub(r",", " , ", string)
        string = re.sub(r"!", " ! ", string)
        string = re.sub(r"\(", " ( ", string)
        string = re.sub(r"\)", " ) ", string)
        string = re.sub(r"\?", " ? ", string)
        string = re.sub(r"\s{2,}", " ", string)
        return string.strip()
    
    def get_pos_data(self, path):
        """
            return positive review data
        """
        # UnicodeDecodeError: 'utf-8' codec can't decode byte
        # https://stackoverflow.com/questions/19699367/unicodedecodeerror-utf-8-codec-cant-decode-byte
        with open("./data/rt-polaritydata/rt-polarity.pos", encoding="ISO-8859-1") as f:
            data = [self.clean_str(line) for line in f]
        return data
    
    def get_neg_data(self, path):
        """
            return negative review data
        """
        with open("./data/rt-polaritydata/rt-polarity.neg", encoding="ISO-8859-1") as f:
            data = [self.clean_str(line) for line in f]
        return data