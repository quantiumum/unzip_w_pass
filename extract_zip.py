import pyzipper
import os
# import threading
import multiprocessing
import logging
from tqdm import tqdm



class SearchZip:
    def __init__(self, base_dir: int, exclude_list = list()) -> None:
        self.base_dir = base_dir
        self.zip_list = list()
        self.exclude_list = exclude_list

    def search_zip(self, base_dir: str , max_depth: int, inner_depth: int = 0) -> list:
        if inner_depth > max_depth:
            return self.zip_list
        else:
            inner_depth += 1
        if os.path.exists(base_dir):
            for item in os.listdir(base_dir):
                inner_item = f"{base_dir}/{item}"
                red_flag = False
                for exclude in self.exclude_list:
                    if exclude in inner_item:
                        red_flag = True
                if red_flag == True: continue
                if os.path.isdir(inner_item) and inner_depth < max_depth:
                    self.search_zip(inner_item, max_depth, inner_depth)
                elif os.path.isfile(inner_item) and pyzipper.is_zipfile(inner_item):
                    self.zip_list.append(inner_item)

class ZipUnarchive:
    def __init__(self, filepath: str, password) -> None:
        self.filepath  = filepath
        self.password = password
        self.dirpath = os.path.dirname(self.filepath)
        self.filename = os.path.basename(self.filepath)
    
    def unarchive(self, remove: bool = False, progressbar: bool = True, pos: int = 0):
        logging.debug(f"Start unzip for {self.filepath}")
        with pyzipper.AESZipFile(self.filepath, 'r', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zip:
            if progressbar == True:
                inside_files = zip.namelist()
                for member in tqdm(iterable = inside_files, total = len(inside_files), desc = self.filename, position = pos, leave=T):
                    zip.extract(member, pwd = str.encode(self.password), path = f'{self.dirpath}/{self.filename[:-4]}')

            elif progressbar == False:
                zip.extractall(pwd=str.encode(self.password), path = f'{self.dirpath}/{self.filename[:-4]}')

        logging.debug(f"Ended unzip for {self.filepath}")
        if remove == True:
            logging.debug(f"Start removing file {self.filepath}")
            os.remove(self.filepath)

