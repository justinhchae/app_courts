# appleseed/courts

## Courts (Initiation and Disposition)

See [/data](https://github.com/justinhchae/appleseed/tree/master/courts/data).

Included as compressed csv or pandas pickle files:

1. change logs for transformations
2. modified initiation and disposition subsets of source data from SAO
3. main table is a combination of initiation left-join disposition
4. calculated pending disposition time for cases without a disposition date
5. calculated case length based on received date and disposition date
6. calculated delta between original charge class from initiation and new charge class from disposition

### Courts Data Reference

A brief expalanation of modified or derived columns that deviate from source data. 

1. Charge Class Categorical Values. During analysis, the charge class are assigned values from 0 to 11 where 11 is the most severe class and 0 is the least severe; -1 is for Null values. The category data type is preserved in the pickled formats.

* List of Charge Class (semantic): 'M', 'X', '1', '2', '3', '4', 'A', 'B', 'C', 'O', 'P', 'Z'
* List of Charge Class (numeric): 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0

2. Charge Class Difference. The severity of the allegation often changes from initation to disposition. Given the numeric categorical class values, it is possible to compute the magnitude of the delta. 

* Meaning: A positive score indicates that the charge severity increased while a low score means the severity decreased from initiation to disposition. Zero means no change.
* Evaluation: (Disposition Charged Class) - (Initiation Charged Class) = Charge Class Difference
* Null values if there is no disposition charged class

3. Case Length. The length of a given case from Received Date to Disposition Date as number of days. 

* Evaluation: (Disposition Date) - (Received Date) = Case Length
* Null values if there is no disposition date

4. Disposition Date Days Pending. The length of time pending from Received date to current Date as number of days IF there is no disposition date. 

* Evaluation: (Current Date) - (Received Date) = Disposition Date Days Pending
* Null values if there is a disposition date

5. Table Join for main.zip. The source Initiation and Disposition tables are left joined on a selection of columns. All other columns, if duplicate, are appened with a suffix of "_init" or "_disp".

* Meaning: The intent is to capture each row as a unique object (a case with a person and a charge) as a measure of events in the court system
* Key values for join: 'case_id', 'case_participant_id', 'received_date', 'offense_category'

6. Imputed Dates. Source tables had a number of erroneous dates for initiation and disposition such as 2109. In these cases, it appears that the date was meant to be 2019, for example. 

* Rationale: For initiation event date and disposition date, if any date values exceed the year 2020, they are replaced with an imputed value
* Evaluation: Initiation event date: if > 2020 or if event date < 2010, then replace the year value with the same year as the received date.
* Evaluation: Disposition date: if > 2020, then replace the year value with the rolling mode of the difference between received date and disposition date. 
