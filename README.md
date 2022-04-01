# tweets_manual_annotation
Given a dataset with tweet IDs and tweets related to the COVID-19 vaccine, perform manual annotation on the dataset for a possible NLP stance detection task. 
Each annotator labels each tweet with a 0, 1, -1 or X where 0 denotes neutral, 1 denotes pro-vaccine, -1 denotes anti-vaccine and X denotes that the tweet is not useful in the stance detection task. 
Once the dataset is annotated, we explore the usefulness of the annotations using measure of inter-rater relatability - Krippendorff's Alpha. 

A nice explanation of the calculation can be found at https://repository.upenn.edu/cgi/viewcontent.cgi?article=1043&context=asc_papers

Although the calculation can be done as small as in a single line with the simpledorff library (https://github.com/LightTag/simpledorff), we took a manual approach to understand the nuances of the calculation. 

The repo has the annotated dataset with tweet ID, annotations by each annotator and a final annotation decided upon by all the three annotators. 
Also present is a python script, which reads the above csv through command line and prints out the Krippendorff's alpha and percentage agreement between the three annotators to the standard out, and a report which explores the various questions that came up during the annotation task. 
