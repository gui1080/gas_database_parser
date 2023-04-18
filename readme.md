# Dealing with the data representation

Every "row" in csv reader is a list that contains the data of a certain row

```
[0] = REF_AREA
[1] = TIME_PERIOD
[2] = ENERGY_PRODUCT
[3] = FLOW_BREAKDOWN
[4] = UNIT_MEASURE
[5] = OBS_VALUE
[6] = ASSESSMENT_CODE
```

Csv file is sorted by [0], [2], [3], [4], [6].
Every json has the values of [1] and [5].

### Example 

For every [0], [2], [3], [4], [6] value that matches when iterating over csv file...

```
['ZA', '2016-10', 'NATGAS', 'TOTDEMO', 'TJ', '397.64', '1']
['ZA', '2018-08', 'NATGAS', 'TOTDEMO', 'TJ', '6', '1']
['ZA', '2018-08', 'NATGAS', 'TOTDEMC', 'TJ', '15821', '1']
```
    
JSON of this data should look like:

```
"series_id" : "some_id_here"
"points": [
    [str(TIME_PERIOD_0), float(OBS_VALUE_0)],
    [str(TIME_PERIOD_1), float(OBS_VALUE_1)],
    ...
    [str(TIME_PERIOD_N), float(OBS_VALUE_N)]
],
"fields":{
    "ref_area": str(REF_AREA),
    "en_product": str(ENERGY_PRODUCT), 
    "flow_breakd": str(FLOW_BREAKDOWN), 
    "unit": str(UNIT_MEASURE), 
    "code": str(ASSESSMENT_CODE)
} 

```

# How to run the file

Given that *Python 3* is installed and up to date, run:

> python3 xxxxx