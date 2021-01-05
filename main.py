from do_data.getter import Reader
from do_data.writer import Writer
from do_data.joiner import Joiner

from clean_data.maker import Maker
# from analyze_data.eda import EDA

from app.app import App


if __name__ == '__main__':
    reader = Reader()
    writer = Writer()
    joiner = Joiner()
    maker = Maker()
    app = App()
    # eda = EDA()

    def read_source(open_source=False):

        if open_source:
            initiation = reader.to_df('Initiation.zip'
                                      , clean_initiation=True
                                      , preview=False
                                      , classify=True
                                      )
            disposition = reader.to_df('Dispositions.zip'
                                       , clean_disposition=True
                                       , preview=False
                                       , classify=True
                                       )

            initiation = maker.make_disposition_pending(df1=initiation
                                                        , df2=disposition
                                                        , source='received_date'
                                                        , target='disposition_date')

            disposition = maker.make_class_diff(df1=disposition
                                                , df2=initiation
                                                , col1='disposition_charged_class'
                                                , col2='class')

            writer.to_package(initiation, 'initiation_modified')
            writer.to_package(disposition, 'disposition_modified')

        else:

            initiation = reader.to_df('initiation_modified.bz2'
                                      , preview=False)
            disposition = reader.to_df('disposition_modified.bz2'
                                       , preview=False)

            main = joiner.initiation_disposition(initiation, disposition)
            writer.to_package(main, 'main')
            sample = main.sample(n=500000, random_state=0)
            writer.to_package(sample, 'sample')

    # read_source(open_source=False)

    def run_app():
        df = reader.to_df('sample.bz2'
                          , preview=False
                          , echo=False
                          , classify=False
                          )
        app.run_app(df)

    run_app()

    # eda.s3(df)



