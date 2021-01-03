import pandas as pd
import json
import os


class Writer():
    def __init__(self, folder='data'):
        self.root = folder

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
        csvd = '.csv'
        zipped = '.zip'

        path = os.sep.join([self.root, filename])

        if compression:
            compression_opts = dict(method='zip', archive_name=filename)

            filename_zip = str(filename + zipped)

            path = os.sep.join([self.root, filename_zip])

            df.to_csv(path, index=False,
                      compression=compression_opts)

            if echo:
                print('Compressed dataframe to', path)
                print()

        else:

            filename_csvd = str(filename + csvd)
            path = os.sep.join([self.root, filename_csvd])

            df.to_csv(path)

            if echo:
                print('Wrote dataframe to', path)
                print()

    def to_pickle(self, df
                  , filename='file.pickle'
                  , compression=True
                  , echo=True
                  , protocol=2
                  ):
        """
        :param df: a pandas dataframe
        :param filename: a string like file.pickle
        :param echo: default to true (print statements and preview head)
        :return: None, writes a pickled file
        """
        pickled = '.pickle'
        bz = '.bz2'

        if compression:

            filename_bz = str(filename + bz)

            path = os.sep.join([self.root, filename_bz])

            df.to_pickle(path, compression='infer', protocol=protocol)

            if echo:
                print('Compressed dataframe to', path)
                print()

        else:

            filename_pickled = str(filename + pickled)
            path = os.sep.join([self.root, filename_pickled])

            df.to_pickle(path)

            if echo:
                print('Wrote dataframe to', path)
                print()

    def to_json(self, df, filename='file.json', orient='columns', echo=True):

        path = os.sep.join([self.root, filename])
        df.to_json(path, orient=orient)

        if echo:
            print('Wrote dataframe to', path)
            print()
