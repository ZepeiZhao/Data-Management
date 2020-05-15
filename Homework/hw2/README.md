# Exploring HDFS Metadata Using XML & XPath

## Task

Export the metadata stored in the specified fsimage to an XML file. 

### a. Write a Python program "invert.py"

    Produce an index file (XML document) which lists for each token, inumbers of files and directories whose name contain the token (case insensitive)
    
### b. Write a python file " search.py" 

    Take a fsimage file, its index file, a search query
    
    Return the full path whose name contains all keywords
    
    Show the metadata (type, mtime, blocks (id)) in the JSON format 
    
