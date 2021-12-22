# Assignment #3 - Complex Joins using SQL

## Objectives:

This lab is designed to have you do a complex "join" using SQL. The goal of this assignmwnt is understand how *joins* play a common role in many data analysis problems. In the past, I've had students solve this problem using Hadoop and then using Spark;
Hadoop is (rightfully) becoming less important so we're going to solve it using SQL and then solve it using Spark.

It's difficult to implement joins in Hadoop manually
so I'm going to walk through a solution using Hadoop in class, 
but you'll be asked to produce a single SQL query that produces 
the desired output below. In the next lab assignment you will be asked to implement it in Spark using RDD's and then using SparkSQL.

## Datasets

You will use the description of the
`acite75_99.zip` and `apat63_99.txt` files (see
[http://data.nber.org/patents](http://data.nber.org/patents) for documentation).

The `Makefile` in this repository should include steps to retrieve the `acite75_99.zip`
and `apat63_99.txt` files; [starter code](Lab03-sqlite-patent.ipynb) includes
code that creates an Sqlite3 database named `patents.sq3` that will contain both database.

The `apat63_99.txt` file contains the patent number, an (optional)
state in which the patent is filed and the total number of citations
made.
![patents-example](patents-example.png)


The `cite75_99.txt` file contains a citation index, of the form

![citations-example](citations-example.png)

where both CITING and CITED are integers representing patent numbers. Each line
indicates that patent number CITING cites patent CITED.

Your job is augment the data in
patent data to include a column indicating the number of patents
  cited that originate from the same state. Obviously, this data can
  only be calculated for patents that have originating state information
  and only for cited patents that provide that information.

Example: patent 6009554 (the last patent in apat63_99.txt) is from NY and it cited 9 other patents. Those CITED patents are from NY, NY, Great Britain (no state), NY, NY, NY, NY, NY, NY. There are 8 cited patents from NY, the same state of the citing patent. You would then produce a new record for patent 6009554 with a new column CO_CITED_COUNT with the value 8.

To do this, you will first need do a "data join” of the citations and the patent data - for each cited patent, you'll need to determine the state of the cited patent.

See [the starter code](Lab03-sqlite-patent.ipynb) for more details.

To check your solution look at the image `final-output.png` (in this repo). The table in this image is sorted by the final column CO_CITED_COUNT. CO_CITED_COUNT indicates the number of cited patents that originate from the same state as the citing patent. Your query should produce the CO_CITED_COUNT for each patent in `pat63_99.txt`. The `final-output.png` shows the 13 patents with the most CO_CITED_COUNT. Just like the photo, you should ORDER your output in decending order and limit it to show the top 13, or so, patents. 

## What and how to turn in your work

You should turn in your work by commiting your changes to starter code ( Lab03-sqlite-patent.ipynb ) and check it in. You can do this using:
```
git commit -a -m'final version'
git push
```

Your should **NOT** add the `patents.sq3` database file to your git repo -- in other words,
do NOT do something like:
```
git add *
git commit -m'you just made a huge mistake'
```
If you do this, you will have checked a huge file into your Git repo and you won't be able
to push it to github. If you make this mistake [you can fix it yourself](https://medium.com/analytics-vidhya/tutorial-removing-large-files-from-git-78dbf4cf83a).
