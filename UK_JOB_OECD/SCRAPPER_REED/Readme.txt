I get the data from the Reed API
In order to to get the data run the REED_SCRAPER.py

You would need to provide the API key which is free to create. the script scraps 10000 adverts
in one go. Which I think is the daily limit as well, as I have not ran the script in 2 consecutive days

The data is missing one important factor, it does not have the SOC code, we would like to have ideally
2 digit and 4 digit soc code, but as we don't have it so we will generate it, so in order to 
generate the dummy soc code we have been using the script called. synthetic_soc_data.py it requires
the reed dataset which we downloaded and stored in the Data folder.

the logic is pretty simple it is a rule based soc allocation we are checking the description of each 
job advert for example if description has these values assign them these soc code

    "data entry": "4112",
    "data analytics": "2425",
    "data science": "3421"


for rest just assign them a random value between 1000 and 9999

Now this will generate a file called enriched_with_soc.csv this is what we are going to
use for the next steps, now we basically want to do the cosine similarity check and want 
to first get all the nouns in the job description and then we are going to basically do a cosine 
similarity for that we have to run the bgt_gb_noun_chunks.py and it will generate a file called
noun_chunks_with_similarity.csv


Now to get the filtered_chunks.csv, job_level_aggregated.csv, soc_level_aggregated.csv

We will run the job_classification.py

and after that we will also need SUT_UK.CSV which we have the dummy one and has these values.

sector,GVA,Investment
Technology,950000000,52000000
Health,850000000,32000000
Transport,600000000,15000000
Retail,500000000,25000000
Admin,400000000,18000000


and then we also have soc_to_sector mapping which we have in the mapping folder and has the 
following values.

soc_code,sector
2136,Technology
2421,Health
3535,Transport
4111,Retail
3411,Retail
1219,Admin


Then we run the sector_analysis_with_fake_mapping.py which will generate the
sector_level_intensity.csv

Then for visualisation we will run visualisation.py 
which require sector_level_intensity.csv and will generate the charts.
