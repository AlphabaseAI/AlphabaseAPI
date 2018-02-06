# -*- coding: utf-8 -*-
#
"""

This module provides a simple API for users to download dataset from alphabase.ai,
and upload predictions to alphabase.ai for evaluation.

Example:
    An Example demonstrating how to use the API can be found together with this
    API, and its name is example.py.

.. alphabase website:
   https://alphabase.ai/

"""


import json
import time
import zipfile
import getpass
import requests
from os import path
from datetime import datetime


class AlphabaseAPI:
    """ alphabase API for data downloading and predictions submission """

    def __init__(self, working_dir=None):
        """initialize alphabase API wrapper for Python

        Args: 
            working_dir (path): where the downloaded dataset should locate
        """
        self.download_url = "https://alphabase.ai/download_API.php"
        self.upload_url = "https://alphabase.ai/upload_API.php"
        self.working_dir = working_dir


    def download(self, username=None, password=None, dest_path=".", unzip=True):
        """function to download current round dataset

        Args:
            username (str): username for loging into alphabase.ai
            password (str): password for loging into alphabase.ai
            dest_path (path): dataset location can be changed using dest_path if working_dir is not provided
            unzip (bool): if True, will unzip the downloaded zip file automatically
        """
        print("Preapring to download...\n")

        agree_t = 'agree'
        if agree_t == 'agree':
            time.sleep(1)
            if username is None:
                print("please provide your username to process download.")
                username = input("username: ")
            if password is None:
                print("and password: ")
                password = getpass.getpass("password: ")

            print("Starting to download, please wait...\n")

            # set up download path
            now = datetime.now().strftime("%Y%m%d")
            dataset_name = "alpha_dataset_{0}".format(now)
            file_name = "{0}.zip".format(dataset_name)

            # unzipped files location
            if(self.working_dir==None):
                self.working_dir = dest_path
            zip_file_path = "{0}/{1}".format(self.working_dir, file_name)
            unzipped_location = self.working_dir

            # send login request and download dataset
            post_data = {"username": username, "password": password}
            r_download = requests.post(self.download_url, data = post_data)
            r_download.raise_for_status()

            # save dataset
            with open(zip_file_path, "wb") as f:
                for chunk in r_download.iter_content(1024):
                   f.write(chunk)

            print("Download completed")
            print("-------------------------\n")
            time.sleep(1)

            # unzip dataset
            if unzip:
                self.unzip_data(zip_file_path, unzipped_location)


    def unzip_data(self, full_path, unzipped_location):
    	"""function used to unzip zip file

    	full_path (path): location pointing to the zip file 
		unzipped_location (path): location where the unzipped files will be in
    	"""
        print("Start unzipping data set...\n")

        # extract data
        with zipfile.ZipFile(full_path, "r") as u:
            u.extractall(unzipped_location)

        print("Finished unzipping data set")
        print("-------------------------\n")
        return True


    def upload(self, username, password, pred_path):
    	"""upload function for predictions submission
		
		username (str): username for loging into alphabase.ai
		password (str): password for loging into alphabase.ai
		path (path): location pointing to the prediction needed to bu submitted
    	"""
        print("Preparing for uploading...")
        if username is None:
            print("please provide your username to process upload.")
            username = input("username: ")
        if password is None:
            print("and password: ")
            password = getpass.getpass("password: ")
        if pred_path is None:
            print("please provide your submission file to process upload.")
            pred_path = input("submission csv location: ")
    	
    	# upload prediction
        post_data = {"username": username, "password": password}
        file_upload = {'fileToUpload': (path.basename(pred_path), open(pred_path, 'rb'))}
        r_upload = requests.post(self.upload_url, files = file_upload, data = post_data)

        print("Upload complete")
        print("-------------------------\n")
        return r_upload.json()

