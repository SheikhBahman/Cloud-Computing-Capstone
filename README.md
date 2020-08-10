# Cloud-Computing-Capstone
This is my capstone project for CS 598: Cloud Computing Capstone at UIUC


# Overview

The goal of the Capstone Project is to work on a transportation dataset from the US Bureau of Transportation Statistics (BTS) that is hosted as an Amazon EBS volume snapshot.
The dataset used in the Project contains data and statistics from the US Department of Transportation on aviation, maritime, highway, transit, rail, pipeline, bike/pedestrian, and other modes of transportation in CSV format. The data is described in more detail by the Bureau of Transportation Statistics. (Note that the dataset we are using does not extend beyond 2008, although more recent data is available from the previous link.) In this Project, we will concentrate exclusively on the aviation portion of the dataset, which contains domestic flight data such as departure and arrival delays, flight times, etc. 

I will be answering a common set of questions in different stacks/systems – in a batch processing system (Apache Hadoop / Spark), and in a stream processing system (Apache Storm / Spark Streaming / Flink). So I will conduct the project on two scenarios:

* **Task1: Batch processing system**

* **Task2: Stream processing system**

There are a set of questions which will be answered using the dataset. These questions involve discovering useful information such as the best day of week to fly to minimize delays, the most popular airports, the most on-time airlines, etc. 

# For eack task I have recorded the steps I followed to setup my cloud system on AWS (please see the video)

# Task 1

**1.	Brief overview of data extraction and cleaning**

As mentioned in the project description in this project we were asked to work on the dataset from the US Bureau of Transportation Statistics (BTS). The dataset was hosted as an Amazon EBS volume snapshot with US Snapshot ID (Linux/Unix): snap-e1608d88 and size of 15 GB. Therefore, I have decided to utilize the AWS-EC2 to copy and extract the data. After extracting the data and selecting the necessary fields I have assembled all the data from different files to a single csv file and store it into AWS-S3 (shown in Fig. 1). I have followed the following steps as also shown in Fig. 1 to extract and prepare the data:

1.	Create an EC2 instance: (Amazon Linux 2 AMI) (t2.medium) (SSD 20 GB).

2.	Copy the EBS snapshot (snap-e1608d88) and create a volume from it.

3.	Attach the EBS volume to the EC2 instance.

4.	SSH to the EC2 and mount the EBS volume to the EC2 instance using following commands: 

                      sudo mkdir /data  
                      sudo mount /dev/xvdf /data
                      
5.	To efficiently extract the data I have prepared a python code (please see Appendix A) to go over the data folders and subfolders, open the zip files in each subfolders, read the csv file and combine all the data to a single csv file as an output. Also as I realized I don’t need all the columns in the original data, to be more efficient, I have decided to collect only the following columns of the data: Year, Month, Origin, ArrTime, DepTime, Dest, ArrDelay, UniqueCarrier, DayOfWeek, DepDelay, and Cancelled. The python code is provided as Appendix A.

6.	The prepared csv file collected from all the zip files then stored in a AWS-S3 bucket:

*	To connect the S3 and EC2 the IAM policy should be created and also both EC2 and S3 should be created in the same region.
*	Access Key for the bucket should be set in EC2 using the following command:

                                          aws configure
*	Then we can use the following command to copy the file from EC2 to S3

            aws s3 cp CleanedData.csv s3://cloudcoursecap/aviation/
            
7.	Further cleaning the data: I observed that there are some null values in the data also I wanted to filter out the cancelled flights from the data but I realized that the part of the results provided to us in “Task 1 Example Solutions” to check our results were calculated without these filtrations. So my results for group 1 and question-1 of group 2 are based on no further cleaning but for group2 question 2, 3, 4 and group 3 questions I have further cleaned the data and omit the cancelled flights or any null data. I have decided to use pySpark queries: data rows with null values omitted from the dataset and also data rows with Cancelled column values equal to 1 are not considered to provide part of the results.

![GitHub Logo](/IMG/1.png)


[![Watch the video](https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.theverge.com%2F2019%2F8%2F13%2F20803418%2Fyoutube-demonetization-appeals-pilot-program-creators&psig=AOvVaw0CepMVpfDcdFIm9Lnngg-O&ust=1597190123209000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCLDkibv4kesCFQAAAAAdAAAAABAD)](https://youtu.be/-U5e7SN_v8g)


