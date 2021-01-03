import pandas as pd
import json
import os


class Writer():
    def __init__(self, folder='data'):
        self.folder = folder
        # self.path = os.environ['PWD'] + os.sep + self.folder + os.sep
        self.path = self.folder + '/'


    def to_package(self, df, filename, compression=True, echo=True):
        """
        A helper function that writes both zipped csv and pickled files
        :param df: a pandas dataframe
        :param filename: a string like 'mydata'
        :param compression: default to true, write as zipped
        :param echo: default to true, print status
        :return: None, writes data to file
        """
        print('Packaging Writer')
        self.to_csv(df, filename, compression, echo)
        self.to_pickle(df, filename, compression, echo)

    def to_csv(self, df, filename='file.csv', compression=True, echo=True):
        """
        :param df: a pandas dataframe
        :param filename: a string like file.csv
        :param compression: default to true, writes csv as a zipped csv
        :param echo: default to true (print statements and preview head)
        :return: None, writes a csv file
        """
        csv = '.csv'
        zipped = '.zip'

        self.filename = filename

        if csv not in filename:
            filename_csv = str(filename + csv)
            self.filename = filename_csv

        # path = self.path + self.filename
        # path = 'data/' + self.filename
        path = os.sep.join([self.folder, filename])

        if compression:

            compression_opts = dict(method='zip',
                                    archive_name=self.filename)

            filename_zip = str(filename + zipped)

            self.filename = filename_zip
            # path = self.path + self.filename
            # path = 'data/' + self.filename
            path = os.sep.join([self.folder, self.filename])

            df.to_csv(path, index=False,
                      compression=compression_opts)

            if echo:
                print('Compressed dataframe to', path)
                print()

        else:
            df.to_csv(path)

            if echo:
                print('Wrote dataframe to', path)
                print()

    def to_pickle(self, df
                  , filename='file.pickle'
                  , compression=True
                  , echo=True
                  ):
        """
        :param df: a pandas dataframe
        :param filename: a string like file.pickle
        :param echo: default to true (print statements and preview head)
        :return: None, writes a pickled file
        """
        pickle = '.pickle'
        method = '.bz2'

        self.filename = filename

        if pickle not in filename:
            filename_ammended = str(filename + pickle)
            self.filename = filename_ammended

        if compression:

            filename_zip = str(filename + method)

            self.filename = filename_zip
            # path = self.path + self.filename
            # path = 'data/' + self.filename
            path = os.sep.join([self.folder, self.filename])

            df.to_pickle(path, compression='infer', protocol=2)

            if echo:
                print('Compressed dataframe to', path)
                print()

        else:

            # path = self.path + self.filename
            # path = 'data/' + self.filename
            path = os.sep.join([self.folder, self.filename])

            df.to_pickle(path)

            if echo:
                print('Wrote dataframe to', path)
                print()

    def to_json(self, df, filename='file.json', orient='columns', echo=True):
        # self.filename = os.sep.join(['data', filename])
        # path = self.path + self.filename
        path = os.sep.join([self.folder, filename])
        df.to_json(path, orient=orient)
