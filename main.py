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

    def read_source():
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
        writer.to_package(initiation, 'initiation_modified')
        writer.to_package(disposition, 'disposition_modified')

    # read_source()

    def make_data():
        initiation = reader.to_df('initiation_modified.bz2'
                                  , preview=False)
        disposition = reader.to_df('disposition_modified.bz2'
                                   , preview=False)

        df = joiner.joiner(initiation, disposition)
        writer.to_package(df, filename='main', compression=True)
        df = df.sample(n=250000, random_state=0)
        writer.to_package(df, filename='sample')

    # make_data()

    def run_app():
        df = reader.to_df('main.bz2'
                          , preview=False
                          , echo=False
                          , classify=False
                          )
        app.run_app(df)

    run_app()

    # eda.s3(df)



