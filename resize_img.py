import os
import multiprocessing
from multiprocessing import Pool
from skimage.transform import resize
from skimage import io, img_as_ubyte
from tqdm import tqdm
import pickle
import pandas as pd


img_file_list = pd.read_parquet('file_list_for_resize.parquet.gzip')
img_file_list = img_file_list['HashId'].values.tolist()

# Check path for downloded image
IMG_PATH = r"./meme_img/" # name of the folder
try: # try to check if the folder is exits.
    os.listdir(IMG_PATH)
except: # create the folder if it is not exits.
    print("Can't find folder")
    os.exit(0)
    
# Check path for downloded image
RESIZE_IMG_PATH = r"./meme_for_train_resize/" # name of the folder
try: # try to check if the folder is exits.
    os.listdir(RESIZE_IMG_PATH)
except: # create the folder if it is not exits.
    os.mkdir("meme_for_train_resize")
    
# Create the function to download the image    
def resize_(img_):
    try:
        io.imsave(RESIZE_IMG_PATH+img_,img_as_ubyte(resize(io.imread(IMG_PATH + img_), (224, 224))))
    except:
        pass

# Parallel resize the image
if __name__ == "__main__":
    with Pool(multiprocessing.cpu_count()-1) as p:
        for _ in tqdm(p.imap_unordered(resize_, img_file_list), total=len(img_file_list)):
            pass
    pickle.dump(os.listdir(RESIZE_IMG_PATH),open('resized_file_list.pkl','wb'))