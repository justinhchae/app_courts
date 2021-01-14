import streamlit as st

from application.ov1 import OV_1

class Featured():
    def __init__(self):
        pass

    def narrative(self):
        st.markdown('**The COVID Court Cliff**')
        st.write(
            'In 2020, the COVID-19 Pandemic brought the world to a grinding halt across all sectors of business and government.',
            'Similarly, court systems reduced their availability and services while doing their part to support public health measures.',
            'However, unlike schools and businesses, some court systems have struggled to resume operations.',
            'The result, so far, has been a growing backlog of cases as individuals wait on the courts.')

        st.write(
            'Exactly how many cases are in the backlog? It depends on which phase of the court system you are investigating.',
            'On a monthly basis over the past 10 years; however, the backlog may be the difference between the projected trend (given by a logistic regression) and an actual count of cases.',
            )

        st.plotly_chart(OV_1().timeseries())

        st.write(
            'As one example of court volume and backlog over time, Cook County courts has seen a severe drop-off in cases across multiple phases of the system.',
            'In 2020, Cook County managed to process about half as many cases in prior years (at best).',
            'For instance, monthly court volumes are down as much as 90% on a monthly basis.')

        st.markdown('**The Issue**')

        st.write(
            'Given the opportunity for alternative remote hearings (i.e. "Zoom Courts"), at issue is whether courts are not meeting their obligation to process cases during the Pandemic.',
            'As just one example of the impact of delayed court proceedings, individuals, who have yet to be convicted of any crime, remain in limbo while waiting on the courts.',
            'In some cases, people are in some form of incarceration (Jail or Electronic Monitoring) or are anxiously waiting for their day in court.',
            'This dashboard might answer questions regarding the operation of the courts over time.'
            )

