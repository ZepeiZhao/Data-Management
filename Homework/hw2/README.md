# Exploring HDFS Metadata Using XML & XPath

## Task

Export the metadata stored in the specified fsimage to an XML file. 
Work with EC2, HDFS, python, XML, Xpath

### a. Write a Python program "invert.py"

    Produce an index file (XML document) which lists for each token, inumbers of files and directories whose name contain the token (case insensitive)
    
### b. Write a python file " search.py" 

    Take a fsimage file, its index file, a search query
    
    Return the full path whose name contains all keywords
    
    Show the metadata (type, mtime, blocks (id)) in the JSON format 

## Submission

### a. python3 invert.py fsimage.xml index.xml
    output: index.xml
### b. python3 search.py fsimage.xml index.xml core site
    output: /user/ZepeiZhao/input/httpfs-site.xml/
                {"id": "16393", "type": "FILE", "mtime": "1582104489031", "blocks": ["1073741829"]}
               /user/ec2-user/input/kms-acls.xml/
                {"id": "16415", "type": "FILE", "mtime": "1582770036687", "blocks": ["1073741848"]}

## How to get your own fsimage.xml

### a. Find fsimage.xml under current directory
     mypath: /tmp/hadoop-ec2-user/dfs/name/current/fsimage_0000000000000000564
     # note that fsimage is changing when you are using hdfs, so memorize the fsimage name you want to export
### b. Export the file to EC2 dir
     [ec2-user@ip-172-31-43-91 hadoop-3.1.2]$ bin/hdfs oiv -i /tmp/hadoop-ec2-user/dfs/name/current/fsimage_0000000000000000564 -o fsimage564.xml -p XML
        # now the file is under /ec2-user/hadoop-3.1.2 
### c. Use scp, download to local dir
     scp -i "xxx.pem" ec2-user@dns:/home/ec2-user/hadoop-3.1.2/fsimage564.xml /target_path
     For example:
     scp -i "INF551_ZZP.pem" ec2-user@ec2-18-216-51-88.us-east-2.compute.amazonaws.com:/home/ec2-user/hadoop-3.1.2/fsimage564.xml /users/pz/Desktop/inf551/LAB 



