# a2-QIXIN-ACT

## 1. Scalable Serverless Architectures

### (abc)

+ Jupyter notebook with all necessary steps and annotations to ensure reproducibility: [q1_main.ipynb](https://github.com/macs30123-s24/a2-QIXIN-ACT/blob/main/q1/q1_main.ipynb)

+ Lambda function .py file for preview: [q1c_lambda.py](https://github.com/macs30123-s24/a2-QIXIN-ACT/blob/main/q1/q1c_lambda.py)
  
+ Lambda function .zip file for deployment: [q1c_lambda.zip](https://github.com/macs30123-s24/a2-QIXIN-ACT/blob/main/q1/q1c_lambda.zip)

### (d)

I'll express my understanding about my PI's concerns about the system potentially crashing if all participants submit their surveys at the same time, then reassure my PI that using AWS's cloud infrastructure can prevent such issues and ensure smooth operation during high traffic periods.

+ **AWS Auto Scaling**: This feature automatically adjusts the computing capacity to maintain consistent performance. During times of sudden spikes in survey submissions, AWS Auto Scaling can dynamically launch additional instances to handle the increased load and then scale down when the submissions decrease *(AWS documentation - What is Amazon EC2 Auto Scaling, https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html)*. This elasticity ensures that the infrastructure can cope with peak loads without human intervention.
+ **AWS Lambda and Elastic Load Balancing**: Leveraging AWS Lambda for processing survey submissions allows each submission to trigger a separate instance of your function, ensuring that the system's performance remains stable even under heavy loads *(AWS documentation - What is AWS Lambda, https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)*. Elastic Load Balancing optimally distributes incoming traffic among Lambda functions, which prevents any single function from becoming overwhelmed and ensures smooth handling of requests *(AWS documentation - What is Elastic Load Balancing, https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html)*.
+ **Amazon S3 and DynamoDB**: For data storage, Amazon S3 is used to store raw survey data, providing highly durable storage that automatically replicates data across multiple physical locations *(AWS documentation - What is Amazon S3, https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)*. Amazon DynamoDB is used for real-time data access needs, storing processed results with automatic scaling and performance management *(AWS documentation - What is Amazon Dynamo DB, https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)*. This dual approach leverages S3’s durability and DynamoDB’s low-latency data access, ensuring no data is lost and all data is quickly accessible.

This modern cloud-based architecture offers both scalability and reliability, ensuring that the research data is secure and consistently accessible.

## 2. Parallel Web Scraping

### (a)

+ Jupyter notebook with all necessary steps and annotations to ensure reproducibility: [q2_main.ipynb](https://github.com/macs30123-s24/a2-QIXIN-ACT/blob/main/q2/q2_main.ipynb)

+ Lambda function .py file for preview: [lambda_function.py](https://github.com/macs30123-s24/a2-QIXIN-ACT/blob/main/q2/lambda_function.py)
  
+ Lambda function .zip file for deployment: [q2-deployment-package.zip](https://github.com/macs30123-s24/a2-QIXIN-ACT/blob/main/q2/q2-deployment-package.zip)

### (b)

+ # Enhancing Web Scraping with AWS Lambda: Strengths, Weaknesses, and Improvements

  **Strengths of the Parallel Approach**:

  1. **Increased Throughput**: Parallel processing allows for scraping multiple pages simultaneously, speeding up data collection *(AWS documentation - Scaling and concurrency in Lambda, https://docs.aws.amazon.com/lambda/latest/operatorguide/scaling-concurrency.html).*
  2. **Cost Efficiency**: Users pay only for the actual compute time used, making it a cost-effective solution for web scraping projects *(AWS documentation - Billing and Cost, https://docs.aws.amazon.com/account-billing/)*.
  3. **Ease of Deployment**: Lambda functions are straightforward to deploy and scale, requiring no server maintenance, thus simplifying system management *(AWS documentation - Performance optimization, https://docs.aws.amazon.com/lambda/latest/operatorguide/perf-optimize.html)*.

  **Weaknesses of the Parallel Approach**:

  1. **Lambda Limits**: When scaling up, AWS Lambda's ***concurrency limits (!!!)*** can hinder performance by throttling additional function invocations once the set limits are reached. This can lead to increased latency or even failure of new invocations if the demand spikes suddenly *(AWS documentation - Lambda function scaling, https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html)*.
  2. **Network and Database Bottlenecks**:
     - **Network Latency**: The distributed nature of AWS Lambda may lead to network latency as data moves between Lambda functions and other services (like databases or external APIs). Strategies to mitigate this include optimizing network architecture, such as using AWS's VPC endpoints to keep traffic within the AWS network and reduce exposure to Internet-related delays.
     - **Database Write Conflicts**: If multiple Lambda functions write to the same database, it can cause write conflicts or locking issues, particularly with relational databases. This is exacerbated during high throughput scenarios where many functions attempt to write simultaneously.

  **Improvements for Scalability**:

  1. **Database Optimization**: Transitioning to a NoSQL database like DynamoDB can provide better scalability and performance for applications with high write and read demands. DynamoDB, for instance, offers automatic scaling capabilities and handles large volumes of requests without the need for manual intervention *(AWS documentation - Managing throughput capacity automatically with DynamoDB auto scaling, https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/AutoScaling.html)*.

  2. **Error Handling**: Add advanced error handling and retry mechanisms to improve data scraping reliability. This ensures that temporary issues such as network glitches or transient database unavailability do not cause the entire process to fail.

  

## 3. Identifying Most-Used Words

+ Python code to run: [q3.py](https://github.com/macs30123-s24/a2-QIXIN-ACT/blob/main/q3/q3.py) - Use "python q3.py descriptions.txt > output.txt" to run locally with a python version under 3.12

+ Top 10 most-used words

  | Word    | Count |
  | ------- | ----- |
  | "new"   | 956   |
  | "one"   | 953   |
  | "life"  | 823   |
  | "world" | 648   |
  | "book"  | 538   |
  | "love"  | 524   |
  | "time"  | 460   |
  | "story" | 417   |
  | "first" | 413   |
  | "years" | 393   |

## 4. Propose a Final Project Topic

+ # Final Project Proposal: Analyzing Perceived Identity in Gig Worker Profile Image Using Large-Scale Computing

  ### Introduction

  In this project, I aim to analyze the impact of perceived racial and gender attributes on the professional visibility of gig workers on platforms such as Fiverr and Upwork. Utilizing the FairFace dataset and Dask, I will process and analyze over 24,000 gig worker profiles, with a goal to expand the dataset to include a broader demographic across multiple platforms.

  ### Relevance to Social Science

  This study examines how perceived identity attributes affect professional interactions and opportunities within the digital gig economy. Through facial recognition technology, I aim to provide insights into discrimination and bias in both AI-based and non-AI-based environments, thereby enriching the discourse on social dynamics within gig work platforms.

  ### Data Collection and Expansion

  My current dataset includes over 24,000 profiles. To deepen my understanding of the gig economy, I plan to expand this dataset from platforms like Fiverr, which hosts over 380,000 active sellers, and Upwork, with its 12 million freelancers. As these platforms do not provide demographic data, it would be helpful to use large-scale computing to do facial recognition to infer racial and gender attributes.

  ### Scalable Data Processing with Dask

  I will use Accelerating Dask for efficient and scalable data processing. Dask allows for the parallel processing of large data volumes by dividing tasks into smaller chunks, which enhances performance and adapts dynamically to the size of the dataset and available computing resources.

  ### Research Schedule

  May 6-8: Data preprocessing and initial model testing.
  May 9-16: Implement and refine parallel computing with Dask.
  May 17-24: Conclude data analysis, finalize GitHub documentation, and prepare the project presentation.
