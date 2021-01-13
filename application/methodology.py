import streamlit as st


class Methodology():
    def __init__(self):
        pass

    def data_methodology(self):
        st.markdown('**Notes on Methodology**')

        st.write(
            'Across all phases, cases are uniquely identified by Case IDs. In each case, there may be one or more individuals that are party to the case, given by Case Participant ID.',
            'To provide high-level insights into court volumes, this dataset is filtered to identify aggregated measures of unique cases and individuals.',
            'For instance, for what might be considered a sigular event, a person may be charged with multiple allegations and multiple counts of a given crime.',
            'Although the severity of such circumstances is not taken lightly, counting each of these instances may overstate a characterization of court volumes.',
            'As a result, to avoid double-counting, this analysis filters Initiation and Disposition records in two key ways.')

        st.write(
            'For Initiation Events, the original source table of approximately 1 million records is reudced to about 350k records where the Primary Charge Flag == True.',
            'For Disposition Hearings, the original source table of approximately 700k records is reduced to about 350k records by the most severe charge in the case.',
            'For example, in Initiation Events, the most severe criminal charge or allegation is usually the most severe charge if there are multiple counts and multiple charges.',
            'In another example for Disposition Hearings, the most severe charge associated with a given case may not be the primary charge due to pleadings and other intricacies of the court system.',
            )
