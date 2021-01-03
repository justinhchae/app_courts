import pandas as pd
from do_data import writer

class Redacter():
    def __init__(self):
        self.write = writer.Writer()


    def export_redacted(self, df):
        df = self._extract_times(df)
        df = self._drop_columns(df)
        df = df.reset_index(drop=True)
        
        return df
    
    def _extract_times(self, df):
       
        df['arrest_year'] = df['arrest_date'].dt.year
        df['arrest_month'] = df['arrest_date'].dt.month
        
        df['arrest_time'] = df['arrest_date'].dt.time
        df['lockup_time'] = df['received_in_lockup'].dt.time
        df['release_time'] = df['released_from_lockup'].dt.time

        return df
    
    def _drop_columns(self, df):
        df = df.drop(columns=['cb_no'])
        df = df.drop(columns=['arrest_date'])
        df = df.drop(columns=['received_in_lockup'])
        df = df.drop(columns=['released_from_lockup'])
        df = df.drop(columns=['bond_date'])
        df = df.drop(columns=['age'])
        
        return df
