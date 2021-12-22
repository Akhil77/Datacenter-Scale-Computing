**Data Center Scale Computing - Lab 2 Report by Srinivas Akhil Mallela**

**Solution**:  
  I have implemented a Java solution by:    
 1. Implementing a Regex matcher in the mapper function to fetch all the text and match accordingly. Only the subgroup needed is written to the context.
 

        Pattern pattern = Pattern.compile("href=\"([^\"]*)\"");
        Matcher matcher = pattern.matcher(value.toString());
    
	    // check all occurances
    
	    while (matcher.find()) {
    
	    word.set(matcher.group(1));//Fetch the sub group inside ( )
    
	    context.write(word, one);
	    }

 3. Modifying the reducer function to return only texts with sum greater than 5.
 4.  Changed the combiner function to write all results and corresponding sums( removing check of greater than 5) to context. 
 5. Modifications to makefile on make/make run to produce JAR file and to run the **UrlCount.java** program.

**Software**:
    

 - Coding.csel.io to run Hadoop locally
 - Google Cloud Platform dataproc cluster (1 master node with 2/4 worker nodes).  

**Output**:

    #cite_note-releases-2 7
    /wiki/Doi_(identifier) 17
    /wiki/ISBN_(identifier) 18
    /wiki/MapReduce 6
    mw-data:TemplateStyles:r999302996 110

**Combiner**:
If the combiner function remains the same as the modified reducer function(With count check > 5), we will be missing certain results after the map phase as the combiner will omit any results with counts less than 5 leading the reducer to have wrong input and then subsequently the final output will not be as expected.
We can correct this by: 

 - Removing the combiner and job.setCombinerClass call. (OR)
 - Creating a new combiner function that returns all results. This is the solution I went with. The job.setCombinerClass in java file has to be updated accordingly.

**Comparision on DataProc with 2/4 node clusters:**

    Ranges for 2 Worker Node Cluster execution runtime by executing time command 4 times: 
        real    0m29.016s to 0m34.544s
        user    0m7.781s to 0m8.043s
        sys     0m0.353s to 0m0.425s
    Ranges for 4 Worker Node Cluster execution runtime by executing time command 4 times: 
        real    0m26.044s to 0m30.274s
        user    0m7.669s to 0m7.995s
        sys     0m0.359s to 0m0.424s
        
Comparing the two results, the improvement in performance is marginal. I believe this is a certain overhead(File I/O, network etc..) in maintaining a 4 node cluster as opposed to two nodes and there seems to be no real advantage of using a 4 node cluster here as the input size is small and we’d need a much larger input size to see a noticeable improvement in execution time when using the 4 worker node cluster.
The number of output files generated(7 in total) were exactly the same on both clusters. The number of reduce tasked launched were also the same with 7 in total.

**Sources:**  
•	https://piazza.com/class/ksav0i6vtu1pc?cid=40  
•	http://www.vogella.com/tutorials/JavaRegularExpressions/article.html  
•	https://medium.com/stackera/java-regex-part-6-group-and-subgroup-2985dc2d42d4  
•	Collaborated with Aravind B Srinivas, Hemanth Chenna

