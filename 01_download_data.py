import os
import multiprocessing
from multiprocessing import Pool
import pandas as pd
from tqdm import tqdm
import requests
import pickle

# To download data, please visit: https://www.kaggle.com/abhishtagatya/imgflipscraped-memes-caption-dataset

# Import data
df = pd.read_csv('memes_data.tsv',sep='\t',usecols=['ImageURL','HashId'])

# Check path for downloded image
IMG_PATH = r"./meme_train/" # name of the folder
try: # try to check if the folder is exits.
    os.listdir(IMG_PATH) 
except: # create the folder if it is not exits.
    os.mkdir("meme_train")

# Create the function to download the image
def download(element_):
    try:
        with open(f'{IMG_PATH}{element_[1]}.png','wb') as f:
            f.write(requests.get('https:'+element_[0]).content)
    except Exception as e:
        print(e)

# Parallel download the image, the number of threads is equals to #CPU cores - 1
if __name__ == "__main__":
    with Pool(multiprocessing.cpu_count()-1) as p:
        for _ in tqdm(p.imap_unordered(download, df.values), total=df.shape[0]):
            pass
    pickle.dump(os.listdir(IMG_PATH),open('meme_file_list.pkl','wb'))
