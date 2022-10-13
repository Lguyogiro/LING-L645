import requests
import zipfile
import time
import os
from io import BytesIO

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def download_file_and_unzip():
    URL = "https://www.manythings.org/anki/deu-eng.zip"
    # manythings server requries user agent
    ua = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

    zip_file_name = "deu-eng.zip"
    if (os.path.isfile(zip_file_name)):
            print("File exists")
    else:
        print("\nFile does not exist. Downloading...\n")
        tic = time.time()
        r = requests.get(URL, stream=True, allow_redirects=True, headers={"User-Agent": ua})
        if r.status_code == 200:
            print("\nFile downloaded. Unzipping file.\n")
            zip_ref = zipfile.ZipFile(BytesIO(r.content))
            zip_ref.extractall('./')
            zip_ref.close()
            toc = time.time()
            print("\nFile unzip completed. Time taken- {:.2f} sec".format((toc-tic)))
        else:
            print("Download failed!")

def prepare_train_test_val_files():
    colnames = ['source_sentence', 'target_sentence', 'unk']
    usecols = ['source_sentence', 'target_sentence']
    data_df = pd.read_csv("deu.txt", sep="\t", engine="python", quotechar='"', names=colnames, header=None, usecols=usecols, on_bad_lines='skip')

    train, test = train_test_split(data_df, test_size=0.3)
    val, test = train_test_split(test, test_size=0.5)

    print(f"train : {round(len(train)/len(data_df), 2)}, {round(len(val)/len(data_df), 2)}, {round(len(test)/len(data_df), 2)}")

    # download as tab-separate file
    train.to_csv("train.tsv", index=False,sep = '\t', header = False)
    val.to_csv("val.tsv", index=False, sep = '\t', header = False)
    test.to_csv("test.tsv", index=False, sep = '\t', header = False)
    print("File saved to disk.")

if __name__ == '__main__':
    download_file_and_unzip()
    prepare_train_test_val_files()


