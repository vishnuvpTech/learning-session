# AWS Complete Learning Roadmap
## From Beginner to AWS Solutions Architect

**Version:** 1.0  
**Last Updated:** March 2026  
**Target Audience:** Backend developers, DevOps engineers, Cloud beginners  
**Prerequisites:** Basic Linux, networking, and programming knowledge  
**Goal:** AWS Solutions Architect Certification + Production Experience

---

## Table of Contents

1. [Learning Path Overview](#overview)
2. [Phase 1: AWS Fundamentals](#phase-1)
3. [Phase 2: Core Services - Compute & Storage](#phase-2)
4. [Phase 3: Networking & Security](#phase-3)
5. [Phase 4: Databases & Data Services](#phase-4)
6. [Phase 5: Application Services](#phase-5)
7. [Phase 6: DevOps & Automation](#phase-6)
8. [Phase 7: Advanced Architecture](#phase-7)
9. [Phase 8: Serverless & Modern Apps](#phase-8)
10. [Cost Optimization Strategies](#cost-optimization)
11. [Best Practices & Security](#best-practices)
12. [Learning Resources](#resources)

---

<a name="overview"></a>
## 1. Learning Path Overview

### 8-Stage Roadmap

```
Stage 1: AWS Fundamentals
         ├─ Account setup, IAM, billing
         └─ Core concepts, AWS console

Stage 2: Compute & Storage
         ├─ EC2, EBS, S3
         └─ Lambda basics

Stage 3: Networking & Security
         ├─ VPC, Security Groups, Route53
         └─ CloudFront, WAF

Stage 4: Databases & Data
         ├─ RDS, DynamoDB, ElastiCache
         └─ Data migration, backup

Stage 5: Application Services
         ├─ Load Balancers, Auto Scaling
         └─ SQS, SNS, Step Functions

Stage 6: DevOps & Automation
         ├─ CloudFormation, CDK, Terraform
         └─ CodePipeline, CodeDeploy

Stage 7: Advanced Architecture
         ├─ Multi-region, disaster recovery
         └─ Microservices patterns

Stage 8: Serverless & Modern
         ├─ API Gateway, Lambda advanced
         └─ Container services (ECS, EKS)
```

### Service Priority Map

**Master First (Core Services):**
- IAM - Security foundation
- EC2 - Virtual servers
- S3 - Object storage
- VPC - Networking
- RDS - Databases
- Lambda - Serverless compute

**Learn Next (Essential):**
- ELB - Load balancing
- Auto Scaling - Scaling
- CloudWatch - Monitoring
- CloudFront - CDN
- Route 53 - DNS
- SNS/SQS - Messaging

**Advanced (Later):**
- EKS/ECS - Containers
- Step Functions - Orchestration
- CloudFormation - IaC
- Systems Manager
- Organizations

---

<a name="phase-1"></a>
## 2. Phase 1: AWS Fundamentals

### 2.1 AWS Account Setup

**Step 1: Create AWS Account**
```bash
1. Visit aws.amazon.com
2. Click "Create an AWS Account"
3. Provide email and password
4. Add payment method (required but free tier available)
5. Verify identity
6. Select support plan (choose Free tier)
```

**Step 2: Secure Your Root Account**
```bash
# Enable MFA on root account
1. Sign in to AWS Console
2. Go to "My Security Credentials"
3. Click "Activate MFA"
4. Use Google Authenticator or Authy
5. NEVER use root account for daily tasks
```

**Step 3: Create Budget Alerts**
```bash
# Prevent surprise bills
1. Go to AWS Billing Dashboard
2. Click "Budgets" → "Create budget"
3. Set budget: $10-20/month
4. Set alert at 80% threshold
5. Add email for notifications
```

**Step 4: Enable Cost Explorer**
```bash
1. Billing Dashboard → Cost Explorer
2. Enable Cost Explorer (free)
3. Review daily to track spending
```

---

### 2.2 AWS Identity and Access Management (IAM)

**Core Concepts:**
- **Users** - Individual people
- **Groups** - Collection of users
- **Roles** - Permissions for services
- **Policies** - JSON documents defining permissions

**Create Admin User (Don't Use Root):**

```bash
# AWS CLI setup after creating IAM user
aws configure
# AWS Access Key ID: [Your Key]
# AWS Secret Access Key: [Your Secret]
# Default region: us-east-1
# Default output format: json
```

**IAM Policy Example:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:Describe*",
        "ec2:StartInstances",
        "ec2:StopInstances"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ]
    }
  ]
}
```

**Best Practices:**
```bash
# 1. Enable MFA for all users
# 2. Use groups for permissions
# 3. Principle of least privilege
# 4. Rotate credentials regularly
# 5. Use roles for EC2 instances
# 6. Never embed credentials in code
```

**Hands-On Practice:**
```bash
# Create IAM user with AWS CLI
aws iam create-user --user-name john-developer

# Create IAM group
aws iam create-group --group-name developers

# Add user to group
aws iam add-user-to-group \
  --user-name john-developer \
  --group-name developers

# Attach policy to group
aws iam attach-group-policy \
  --group-name developers \
  --policy-arn arn:aws:iam::aws:policy/PowerUserAccess

# Create access key
aws iam create-access-key --user-name john-developer
```

---

### 2.3 AWS Global Infrastructure

**Understanding Regions and Availability Zones:**

```
AWS Global Infrastructure:
├── Regions (30+)
│   └── Availability Zones (3-6 per region)
│       └── Data Centers (multiple per AZ)
├── Edge Locations (400+)
│   └── CloudFront, Route 53, WAF
└── Local Zones
    └── Ultra-low latency applications

Region Naming: us-east-1, eu-west-1, ap-southeast-1
AZ Naming: us-east-1a, us-east-1b, us-east-1c
```

**Choosing a Region:**
```bash
Factors to consider:
1. Latency - Closer to users
2. Services - Not all services in all regions
3. Compliance - Data sovereignty requirements
4. Cost - Pricing varies by region
5. Availability - Multiple AZs for HA

Example:
- US customers → us-east-1 (N. Virginia) or us-west-2 (Oregon)
- EU customers → eu-west-1 (Ireland) or eu-central-1 (Frankfurt)
- Asia customers → ap-southeast-1 (Singapore) or ap-northeast-1 (Tokyo)
```

---

### 2.4 AWS Free Tier

**Always Free Services:**
```
- Lambda: 1M requests/month
- DynamoDB: 25 GB storage
- S3: 5 GB storage (12 months)
- CloudWatch: 10 custom metrics
- SNS: 1M publishes/month
- SQS: 1M requests/month
```

**12-Month Free Tier:**
```
- EC2: 750 hours/month (t2.micro or t3.micro)
- RDS: 750 hours/month (db.t2.micro)
- S3: 5 GB storage
- EBS: 30 GB
- CloudFront: 50 GB data transfer
- ELB: 750 hours/month
```

**Practice Projects (Free Tier Safe):**
```
1. Static website on S3
2. EC2 instance with web server
3. RDS database with EC2
4. Lambda function with API Gateway
5. CloudFront distribution
```

---

<a name="phase-2"></a>
## 3. Phase 2: Core Services - Compute & Storage

### 3.1 Amazon EC2 (Elastic Compute Cloud)

**Launch Your First EC2 Instance:**

```bash
# Using AWS CLI
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \  # Amazon Linux 2
  --instance-type t2.micro \
  --key-name my-key-pair \
  --security-group-ids sg-0123456789abcdef0 \
  --subnet-id subnet-0123456789abcdef0 \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=MyWebServer}]'
```

**Instance Types:**
```
General Purpose: t3, t4g, m5, m6i
  - Use: Web servers, dev environments
  - Example: t3.micro (1 vCPU, 1 GB RAM)

Compute Optimized: c5, c6i, c7g
  - Use: Batch processing, ML inference
  - Example: c5.large (2 vCPU, 4 GB RAM)

Memory Optimized: r5, r6i, x2iedn
  - Use: Databases, caching
  - Example: r5.large (2 vCPU, 16 GB RAM)

Storage Optimized: i3, d2, h1
  - Use: Data warehousing, HDFS
  - Example: i3.large (2 vCPU, 15.25 GB RAM, 475 GB NVMe SSD)

GPU Instances: p3, p4, g4
  - Use: ML training, graphics
  - Example: p3.2xlarge (8 vCPU, 61 GB RAM, 1 GPU)
```

**EC2 User Data (Bootstrap Script):**
```bash
#!/bin/bash
# This script runs when instance first starts

# Update system
yum update -y

# Install Apache
yum install -y httpd

# Start Apache
systemctl start httpd
systemctl enable httpd

# Create sample page
echo "<h1>Hello from EC2!</h1>" > /var/www/html/index.html
```

**Connect to EC2 Instance:**
```bash
# SSH connection
chmod 400 my-key-pair.pem
ssh -i my-key-pair.pem ec2-user@ec2-12-34-56-78.compute-1.amazonaws.com

# Or use Session Manager (no SSH key needed)
aws ssm start-session --target i-1234567890abcdef0
```

**Instance Management:**
```bash
# Start instance
aws ec2 start-instances --instance-ids i-1234567890abcdef0

# Stop instance
aws ec2 stop-instances --instance-ids i-1234567890abcdef0

# Terminate instance
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0

# Describe instances
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running"
```

---

### 3.2 Amazon S3 (Simple Storage Service)

**Create S3 Bucket:**
```bash
# Create bucket
aws s3 mb s3://my-unique-bucket-name-12345

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket my-unique-bucket-name-12345 \
  --versioning-configuration Status=Enabled

# Enable encryption
aws s3api put-bucket-encryption \
  --bucket my-unique-bucket-name-12345 \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'
```

**Upload Files:**
```bash
# Upload single file
aws s3 cp myfile.txt s3://my-bucket/

# Upload directory
aws s3 sync ./local-folder s3://my-bucket/remote-folder/

# Upload with metadata
aws s3 cp myfile.txt s3://my-bucket/ \
  --metadata key1=value1,key2=value2

# Public read access (use carefully!)
aws s3 cp myfile.txt s3://my-bucket/ --acl public-read
```

**S3 Storage Classes:**
```
Standard: Frequent access, high availability
Standard-IA: Infrequent access, lower cost
One Zone-IA: Single AZ, lowest cost IA
Glacier Instant: Archive, instant retrieval
Glacier Flexible: Archive, minutes-hours retrieval
Glacier Deep Archive: Archive, 12-hour retrieval

Use Cases:
- Standard: Active website content, mobile apps
- Standard-IA: Backups, older data
- Glacier: Long-term archives, compliance
```

**S3 Lifecycle Policy:**
```json
{
  "Rules": [
    {
      "Id": "Move to IA after 30 days",
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        }
      ]
    },
    {
      "Id": "Delete old versions",
      "Status": "Enabled",
      "NoncurrentVersionExpiration": {
        "NoncurrentDays": 90
      }
    }
  ]
}
```

**Host Static Website on S3:**
```bash
# Enable static website hosting
aws s3 website s3://my-bucket/ \
  --index-document index.html \
  --error-document error.html

# Upload website files
aws s3 sync ./website s3://my-bucket/

# Make bucket public
aws s3api put-bucket-policy \
  --bucket my-bucket \
  --policy file://public-policy.json
```

**public-policy.json:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}
```

---

### 3.3 Amazon EBS (Elastic Block Store)

**EBS Volume Types:**
```
General Purpose SSD (gp3, gp2):
  - Use: Boot volumes, dev/test
  - Performance: 3,000-16,000 IOPS
  - Cost: $0.08/GB-month

Provisioned IOPS SSD (io2, io1):
  - Use: Databases, critical apps
  - Performance: Up to 64,000 IOPS
  - Cost: $0.125/GB-month + $0.065/IOPS

Throughput Optimized HDD (st1):
  - Use: Big data, data warehouses
  - Performance: 500 MB/s throughput
  - Cost: $0.045/GB-month

Cold HDD (sc1):
  - Use: Infrequent access
  - Performance: 250 MB/s throughput
  - Cost: $0.015/GB-month
```

**Create and Attach EBS Volume:**
```bash
# Create volume
aws ec2 create-volume \
  --availability-zone us-east-1a \
  --size 10 \
  --volume-type gp3 \
  --tag-specifications 'ResourceType=volume,Tags=[{Key=Name,Value=MyVolume}]'

# Attach to instance
aws ec2 attach-volume \
  --volume-id vol-0123456789abcdef0 \
  --instance-id i-1234567890abcdef0 \
  --device /dev/sdf

# Format and mount on Linux
sudo mkfs -t ext4 /dev/xvdf
sudo mkdir /data
sudo mount /dev/xvdf /data

# Make permanent (add to /etc/fstab)
echo "/dev/xvdf /data ext4 defaults,nofail 0 2" | sudo tee -a /etc/fstab
```

**EBS Snapshots:**
```bash
# Create snapshot
aws ec2 create-snapshot \
  --volume-id vol-0123456789abcdef0 \
  --description "My backup snapshot"

# Copy snapshot to another region
aws ec2 copy-snapshot \
  --source-region us-east-1 \
  --source-snapshot-id snap-0123456789abcdef0 \
  --destination-region us-west-2

# Create volume from snapshot
aws ec2 create-volume \
  --snapshot-id snap-0123456789abcdef0 \
  --availability-zone us-west-2a
```

---

### 3.4 AWS Lambda (Serverless Compute)

**Your First Lambda Function:**

**Python Example:**
```python
import json

def lambda_handler(event, context):
    """
    Lambda function to process API requests.
    """
    # Get data from event
    name = event.get('name', 'World')
    
    # Process
    message = f"Hello, {name}!"
    
    # Return response
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'message': message
        })
    }
```

**Node.js Example:**
```javascript
exports.handler = async (event) => {
    console.log('Event:', JSON.stringify(event, null, 2));
    
    const name = event.name || 'World';
    
    const response = {
        statusCode: 200,
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify({
            message: `Hello, ${name}!`
        })
    };
    
    return response;
};
```

**Deploy Lambda Function:**
```bash
# Package function
zip function.zip lambda_function.py

# Create function
aws lambda create-function \
  --function-name my-function \
  --runtime python3.11 \
  --role arn:aws:iam::123456789012:role/lambda-execution-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip

# Invoke function
aws lambda invoke \
  --function-name my-function \
  --payload '{"name": "AWS"}' \
  response.json

# View response
cat response.json
```

**Lambda with Environment Variables:**
```bash
# Update function configuration
aws lambda update-function-configuration \
  --function-name my-function \
  --environment Variables="{DB_HOST=mydb.example.com,DB_PORT=3306}"
```

**Lambda Layers (Shared Dependencies):**
```bash
# Create layer
zip -r layer.zip python/

aws lambda publish-layer-version \
  --layer-name my-dependencies \
  --zip-file fileb://layer.zip \
  --compatible-runtimes python3.11

# Add layer to function
aws lambda update-function-configuration \
  --function-name my-function \
  --layers arn:aws:lambda:us-east-1:123456789012:layer:my-dependencies:1
```

---

<a name="phase-3"></a>
## 4. Phase 3: Networking & Security

### 4.1 Amazon VPC (Virtual Private Cloud)

**VPC Architecture:**
```
VPC (10.0.0.0/16)
├── Public Subnet (10.0.1.0/24)
│   ├── Internet Gateway
│   ├── Web Servers
│   └── NAT Gateway
├── Private Subnet (10.0.2.0/24)
│   ├── Application Servers
│   └── Database Servers
└── Database Subnet (10.0.3.0/24)
    └── RDS Instances
```

**Create VPC:**
```bash
# Create VPC
aws ec2 create-vpc \
  --cidr-block 10.0.0.0/16 \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=MyVPC}]'

# Create Internet Gateway
aws ec2 create-internet-gateway \
  --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Name,Value=MyIGW}]'

# Attach to VPC
aws ec2 attach-internet-gateway \
  --internet-gateway-id igw-0123456789abcdef0 \
  --vpc-id vpc-0123456789abcdef0

# Create Subnets
aws ec2 create-subnet \
  --vpc-id vpc-0123456789abcdef0 \
  --cidr-block 10.0.1.0/24 \
  --availability-zone us-east-1a \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=PublicSubnet}]'

aws ec2 create-subnet \
  --vpc-id vpc-0123456789abcdef0 \
  --cidr-block 10.0.2.0/24 \
  --availability-zone us-east-1a \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=PrivateSubnet}]'
```

**Route Tables:**
```bash
# Create route table for public subnet
aws ec2 create-route-table \
  --vpc-id vpc-0123456789abcdef0 \
  --tag-specifications 'ResourceType=route-table,Tags=[{Key=Name,Value=PublicRT}]'

# Add route to Internet Gateway
aws ec2 create-route \
  --route-table-id rtb-0123456789abcdef0 \
  --destination-cidr-block 0.0.0.0/0 \
  --gateway-id igw-0123456789abcdef0

# Associate with subnet
aws ec2 associate-route-table \
  --route-table-id rtb-0123456789abcdef0 \
  --subnet-id subnet-0123456789abcdef0
```

**NAT Gateway (for private instances to access internet):**
```bash
# Allocate Elastic IP
aws ec2 allocate-address --domain vpc

# Create NAT Gateway
aws ec2 create-nat-gateway \
  --subnet-id subnet-0123456789abcdef0 \  # Public subnet
  --allocation-id eipalloc-0123456789abcdef0

# Add route in private route table
aws ec2 create-route \
  --route-table-id rtb-private \
  --destination-cidr-block 0.0.0.0/0 \
  --nat-gateway-id nat-0123456789abcdef0
```

---

### 4.2 Security Groups & NACLs

**Security Groups (Stateful):**
```bash
# Create security group
aws ec2 create-security-group \
  --group-name web-sg \
  --description "Security group for web servers" \
  --vpc-id vpc-0123456789abcdef0

# Allow HTTP traffic
aws ec2 authorize-security-group-ingress \
  --group-id sg-0123456789abcdef0 \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0

# Allow HTTPS traffic
aws ec2 authorize-security-group-ingress \
  --group-id sg-0123456789abcdef0 \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0

# Allow SSH from specific IP
aws ec2 authorize-security-group-ingress \
  --group-id sg-0123456789abcdef0 \
  --protocol tcp \
  --port 22 \
  --cidr 1.2.3.4/32

# Allow MySQL from app servers
aws ec2 authorize-security-group-ingress \
  --group-id sg-database \
  --protocol tcp \
  --port 3306 \
  --source-group sg-app-servers
```

**Common Security Group Patterns:**
```
Web Server Security Group:
  Inbound:
    - Port 80 (HTTP) from 0.0.0.0/0
    - Port 443 (HTTPS) from 0.0.0.0/0
    - Port 22 (SSH) from your IP
  Outbound:
    - All traffic

Application Server Security Group:
  Inbound:
    - Port 8080 from web-sg
    - Port 22 from bastion-sg
  Outbound:
    - All traffic

Database Security Group:
  Inbound:
    - Port 3306 from app-sg
  Outbound:
    - None needed
```

**Network ACLs (Stateless):**
```bash
# Create Network ACL
aws ec2 create-network-acl \
  --vpc-id vpc-0123456789abcdef0

# Add inbound rule
aws ec2 create-network-acl-entry \
  --network-acl-id acl-0123456789abcdef0 \
  --rule-number 100 \
  --protocol tcp \
  --port-range From=80,To=80 \
  --cidr-block 0.0.0.0/0 \
  --rule-action allow

# Add outbound rule (required for stateless)
aws ec2 create-network-acl-entry \
  --network-acl-id acl-0123456789abcdef0 \
  --rule-number 100 \
  --protocol tcp \
  --port-range From=1024,To=65535 \
  --egress \
  --cidr-block 0.0.0.0/0 \
  --rule-action allow
```

---

### 4.3 Route 53 (DNS Service)

**Register Domain and Create Hosted Zone:**
```bash
# Create hosted zone
aws route53 create-hosted-zone \
  --name example.com \
  --caller-reference $(date +%s)

# Create A record
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "www.example.com",
        "Type": "A",
        "TTL": 300,
        "ResourceRecords": [{"Value": "1.2.3.4"}]
      }
    }]
  }'
```

**Routing Policies:**
```
Simple: Single resource (one server)
Weighted: Traffic distribution (70% to v1, 30% to v2)
Latency: Lowest latency (route to nearest region)
Failover: Active-passive (backup server)
Geolocation: Based on user location
Geoproximity: Based on resource location
Multivalue: Multiple IPs with health checks
```

**Health Checks:**
```bash
# Create health check
aws route53 create-health-check \
  --health-check-config \
    IPAddress=1.2.3.4,Port=80,Type=HTTP,\
    ResourcePath=/health,RequestInterval=30,\
    FailureThreshold=3
```

---

### 4.4 CloudFront (CDN)

**Create CloudFront Distribution:**
```bash
# For S3 origin
aws cloudfront create-distribution \
  --distribution-config file://distribution-config.json
```

**distribution-config.json:**
```json
{
  "CallerReference": "unique-string-12345",
  "Origins": {
    "Quantity": 1,
    "Items": [{
      "Id": "S3-my-bucket",
      "DomainName": "my-bucket.s3.amazonaws.com",
      "S3OriginConfig": {
        "OriginAccessIdentity": ""
      }
    }]
  },
  "DefaultCacheBehavior": {
    "TargetOriginId": "S3-my-bucket",
    "ViewerProtocolPolicy": "redirect-to-https",
    "AllowedMethods": {
      "Quantity": 2,
      "Items": ["GET", "HEAD"]
    },
    "ForwardedValues": {
      "QueryString": false,
      "Cookies": {"Forward": "none"}
    },
    "MinTTL": 0,
    "DefaultTTL": 86400
  },
  "Enabled": true
}
```

**CloudFront Use Cases:**
```
Static Content: Images, CSS, JS files
Video Streaming: HLS, DASH
API Acceleration: Speed up API responses
Dynamic Content: With Lambda@Edge
Website: Full website distribution
```

---

<a name="phase-4"></a>
## 5. Phase 4: Databases & Data Services

### 5.1 Amazon RDS (Relational Database Service)

**Supported Engines:**
- MySQL
- PostgreSQL
- MariaDB
- Oracle
- SQL Server
- Amazon Aurora (MySQL/PostgreSQL compatible)

**Create RDS Instance:**
```bash
# Create MySQL RDS instance
aws rds create-db-instance \
  --db-instance-identifier mydb \
  --db-instance-class db.t3.micro \
  --engine mysql \
  --master-username admin \
  --master-user-password MySecurePassword123! \
  --allocated-storage 20 \
  --vpc-security-group-ids sg-0123456789abcdef0 \
  --db-subnet-group-name mydbsubnetgroup \
  --backup-retention-period 7 \
  --multi-az \
  --storage-encrypted

# Wait for instance to be available
aws rds wait db-instance-available \
  --db-instance-identifier mydb

# Get endpoint
aws rds describe-db-instances \
  --db-instance-identifier mydb \
  --query 'DBInstances[0].Endpoint.Address'
```

**Connect to RDS:**
```bash
# Connect from EC2 instance
mysql -h mydb.abcdefghij.us-east-1.rds.amazonaws.com \
      -P 3306 \
      -u admin \
      -p

# Or using Python
import pymysql

connection = pymysql.connect(
    host='mydb.abcdefghij.us-east-1.rds.amazonaws.com',
    user='admin',
    password='MySecurePassword123!',
    database='myapp',
    port=3306
)

cursor = connection.cursor()
cursor.execute("SELECT VERSION()")
version = cursor.fetchone()
print(f"Database version: {version}")
```

**RDS Best Practices:**
```
1. Enable Multi-AZ for production
2. Use Read Replicas for read-heavy workloads
3. Enable automated backups (7-35 days)
4. Use Parameter Groups for configuration
5. Monitor with CloudWatch metrics
6. Use IAM database authentication
7. Encrypt at rest and in transit
8. Regular snapshot testing
```

**Read Replicas:**
```bash
# Create read replica
aws rds create-db-instance-read-replica \
  --db-instance-identifier mydb-replica \
  --source-db-instance-identifier mydb \
  --db-instance-class db.t3.micro
```

---

### 5.2 Amazon DynamoDB (NoSQL)

**Create Table:**
```bash
# Create DynamoDB table
aws dynamodb create-table \
  --table-name Users \
  --attribute-definitions \
    AttributeName=UserId,AttributeType=S \
    AttributeName=Email,AttributeType=S \
  --key-schema \
    AttributeName=UserId,KeyType=HASH \
  --global-secondary-indexes \
    '[{
      "IndexName": "EmailIndex",
      "KeySchema": [{"AttributeName":"Email","KeyType":"HASH"}],
      "Projection": {"ProjectionType":"ALL"},
      "ProvisionedThroughput": {"ReadCapacityUnits":5,"WriteCapacityUnits":5}
    }]' \
  --provisioned-throughput \
    ReadCapacityUnits=5,WriteCapacityUnits=5
```

**CRUD Operations:**
```python
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

# Create (Put Item)
table.put_item(
    Item={
        'UserId': '12345',
        'Email': 'user@example.com',
        'Name': 'John Doe',
        'Age': 30,
        'Active': True
    }
)

# Read (Get Item)
response = table.get_item(
    Key={'UserId': '12345'}
)
user = response.get('Item')

# Update
table.update_item(
    Key={'UserId': '12345'},
    UpdateExpression='SET Age = :age, Active = :active',
    ExpressionAttributeValues={
        ':age': 31,
        ':active': False
    }
)

# Delete
table.delete_item(
    Key={'UserId': '12345'}
)

# Query
response = table.query(
    KeyConditionExpression='UserId = :userid',
    ExpressionAttributeValues={
        ':userid': '12345'
    }
)

# Scan (avoid for large tables)
response = table.scan(
    FilterExpression='Age > :age',
    ExpressionAttributeValues={
        ':age': 25
    }
)
```

**DynamoDB Best Practices:**
```
1. Use partition keys with high cardinality
2. Avoid hot partitions
3. Use GSIs for additional access patterns
4. Implement conditional writes
5. Use DynamoDB Streams for changes
6. Consider on-demand vs provisioned capacity
7. Batch operations when possible
8. Use TTL for automatic deletion
```

---

### 5.3 Amazon ElastiCache (Redis/Memcached)

**Create Redis Cluster:**
```bash
# Create Redis cluster
aws elasticache create-cache-cluster \
  --cache-cluster-id my-redis-cluster \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --engine-version 7.0 \
  --num-cache-nodes 1 \
  --cache-subnet-group-name my-subnet-group \
  --security-group-ids sg-0123456789abcdef0
```

**Connect to Redis:**
```python
import redis
import json

# Connect to ElastiCache Redis
r = redis.Redis(
    host='my-redis-cluster.abcdef.0001.use1.cache.amazonaws.com',
    port=6379,
    decode_responses=True
)

# Set value
r.set('user:1000', 'John Doe')

# Get value
name = r.get('user:1000')

# Set with expiration (TTL)
r.setex('session:abc123', 3600, 'user_data')

# Hash operations
r.hset('user:1000', mapping={
    'name': 'John Doe',
    'email': 'john@example.com',
    'age': 30
})

# List operations
r.lpush('queue:tasks', 'task1', 'task2')
task = r.rpop('queue:tasks')

# Use as cache
def get_user(user_id):
    # Try cache first
    cached = r.get(f'user:{user_id}')
    if cached:
        return json.loads(cached)
    
    # If not in cache, query database
    user = query_database(user_id)
    
    # Store in cache
    r.setex(f'user:{user_id}', 3600, json.dumps(user))
    
    return user
```

---

<a name="phase-5"></a>
## 6. Phase 5: Application Services

### 6.1 Elastic Load Balancing (ELB)

**Types of Load Balancers:**
```
Application Load Balancer (ALB):
  - Layer 7 (HTTP/HTTPS)
  - Host/path-based routing
  - WebSockets support
  - Use: Microservices, containers

Network Load Balancer (NLB):
  - Layer 4 (TCP/UDP)
  - Ultra-low latency
  - Static IP support
  - Use: High performance, gaming

Gateway Load Balancer:
  - Layer 3 (Network)
  - Third-party appliances
  - Use: Firewalls, IDS/IPS

Classic Load Balancer:
  - Legacy (being phased out)
  - Use: Existing apps only
```

**Create Application Load Balancer:**
```bash
# Create ALB
aws elbv2 create-load-balancer \
  --name my-alb \
  --subnets subnet-abc123 subnet-def456 \
  --security-groups sg-0123456789abcdef0 \
  --scheme internet-facing \
  --type application

# Create target group
aws elbv2 create-target-group \
  --name my-targets \
  --protocol HTTP \
  --port 80 \
  --vpc-id vpc-0123456789abcdef0 \
  --health-check-path /health \
  --health-check-interval-seconds 30

# Register targets
aws elbv2 register-targets \
  --target-group-arn arn:aws:elasticloadbalancing:... \
  --targets Id=i-1234567890abcdef0 Id=i-0987654321fedcba0

# Create listener
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:... \
  --protocol HTTP \
  --port 80 \
  --default-actions Type=forward,TargetGroupArn=arn:aws:...
```

**Path-Based Routing:**
```bash
# Create listener rules
aws elbv2 create-rule \
  --listener-arn arn:aws:elasticloadbalancing:... \
  --priority 1 \
  --conditions Field=path-pattern,Values='/api/*' \
  --actions Type=forward,TargetGroupArn=arn:aws:...:targetgroup/api-targets
```

---

### 6.2 Auto Scaling

**Create Launch Template:**
```bash
# Create launch template
aws ec2 create-launch-template \
  --launch-template-name my-template \
  --version-description "Version 1" \
  --launch-template-data '{
    "ImageId": "ami-0c55b159cbfafe1f0",
    "InstanceType": "t3.micro",
    "KeyName": "my-key",
    "SecurityGroupIds": ["sg-0123456789abcdef0"],
    "UserData": "IyEvYmluL2Jhc2gK...",
    "IamInstanceProfile": {
      "Arn": "arn:aws:iam::123456789012:instance-profile/my-role"
    }
  }'
```

**Create Auto Scaling Group:**
```bash
# Create ASG
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name my-asg \
  --launch-template LaunchTemplateName=my-template \
  --min-size 2 \
  --max-size 10 \
  --desired-capacity 2 \
  --vpc-zone-identifier "subnet-abc123,subnet-def456" \
  --target-group-arns arn:aws:elasticloadbalancing:...:targetgroup/my-targets \
  --health-check-type ELB \
  --health-check-grace-period 300

# Create scaling policy (target tracking)
aws autoscaling put-scaling-policy \
  --auto-scaling-group-name my-asg \
  --policy-name cpu-target-tracking \
  --policy-type TargetTrackingScaling \
  --target-tracking-configuration '{
    "PredefinedMetricSpecification": {
      "PredefinedMetricType": "ASGAverageCPUUtilization"
    },
    "TargetValue": 50.0
  }'
```

---

### 6.3 Amazon SQS (Simple Queue Service)

**Create Queue:**
```bash
# Create standard queue
aws sqs create-queue --queue-name my-queue

# Create FIFO queue
aws sqs create-queue \
  --queue-name my-queue.fifo \
  --attributes FifoQueue=true,ContentBasedDeduplication=true
```

**Send and Receive Messages:**
```python
import boto3
import json

sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/my-queue'

# Send message
response = sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=json.dumps({
        'order_id': '12345',
        'customer': 'john@example.com',
        'total': 99.99
    }),
    MessageAttributes={
        'OrderType': {
            'StringValue': 'Standard',
            'DataType': 'String'
        }
    }
)

# Receive messages
response = sqs.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=10,
    WaitTimeSeconds=20  # Long polling
)

for message in response.get('Messages', []):
    # Process message
    body = json.loads(message['Body'])
    print(f"Processing order: {body['order_id']}")
    
    # Delete message after processing
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=message['ReceiptHandle']
    )
```

**SQS Use Cases:**
```
- Decoupling microservices
- Job queues / task processing
- Order processing
- Log aggregation
- Event-driven architectures
- Buffer for database writes
```

---

### 6.4 Amazon SNS (Simple Notification Service)

**Create Topic and Subscribe:**
```bash
# Create SNS topic
aws sns create-topic --name my-notifications

# Subscribe with email
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:123456789012:my-notifications \
  --protocol email \
  --notification-endpoint user@example.com

# Subscribe with SMS
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:123456789012:my-notifications \
  --protocol sms \
  --notification-endpoint +1234567890

# Subscribe with Lambda
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:123456789012:my-notifications \
  --protocol lambda \
  --notification-endpoint arn:aws:lambda:us-east-1:123456789012:function:my-function
```

**Publish Messages:**
```python
import boto3
import json

sns = boto3.client('sns')
topic_arn = 'arn:aws:sns:us-east-1:123456789012:my-notifications'

# Publish simple message
response = sns.publish(
    TopicArn=topic_arn,
    Subject='Order Confirmation',
    Message='Your order #12345 has been shipped!'
)

# Publish with different formats per protocol
message = {
    'default': 'Default message',
    'email': 'Email version with HTML',
    'sms': 'SMS: Order shipped',
    'lambda': json.dumps({'order_id': '12345', 'status': 'shipped'})
}

response = sns.publish(
    TopicArn=topic_arn,
    Subject='Order Update',
    MessageStructure='json',
    Message=json.dumps(message)
)
```

---

<a name="phase-6"></a>
## 7. Phase 6: DevOps & Automation

### 7.1 AWS CloudFormation (Infrastructure as Code)

**Your First CloudFormation Template:**

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Simple web server stack'

Parameters:
  KeyName:
    Description: EC2 Key Pair for SSH
    Type: AWS::EC2::KeyPair::KeyName
  
  InstanceType:
    Description: EC2 instance type
    Type: String
    Default: t3.micro
    AllowedValues:
      - t3.micro
      - t3.small
      - t3.medium

Resources:
  # Security Group
  WebServerSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Enable HTTP and SSH
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0
  
  # EC2 Instance
  WebServer:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-0c55b159cbfafe1f0
      InstanceType: !Ref InstanceType
      KeyName: !Ref KeyName
      SecurityGroups:
        - !Ref WebServerSecurityGroup
      UserData:
        Fn::Base64: !Sub |
          #!/bin/bash
          yum update -y
          yum install -y httpd
          systemctl start httpd
          systemctl enable httpd
          echo "<h1>Hello from CloudFormation!</h1>" > /var/www/html/index.html
      Tags:
        - Key: Name
          Value: WebServer

Outputs:
  WebsiteURL:
    Description: URL of the web server
    Value: !Sub 'http://${WebServer.PublicDnsName}'
  
  InstanceId:
    Description: Instance ID
    Value: !Ref WebServer
```

**Deploy Stack:**
```bash
# Create stack
aws cloudformation create-stack \
  --stack-name my-web-stack \
  --template-body file://template.yaml \
  --parameters ParameterKey=KeyName,ParameterValue=my-key \
               ParameterKey=InstanceType,ParameterValue=t3.micro

# Wait for completion
aws cloudformation wait stack-create-complete \
  --stack-name my-web-stack

# Get outputs
aws cloudformation describe-stacks \
  --stack-name my-web-stack \
  --query 'Stacks[0].Outputs'

# Update stack
aws cloudformation update-stack \
  --stack-name my-web-stack \
  --template-body file://template-updated.yaml

# Delete stack
aws cloudformation delete-stack \
  --stack-name my-web-stack
```

---

### 7.2 AWS CDK (Cloud Development Kit)

**Install CDK:**
```bash
# Install CDK CLI
npm install -g aws-cdk

# Verify installation
cdk --version

# Bootstrap your account (one-time per region)
cdk bootstrap aws://ACCOUNT-NUMBER/REGION
```

**CDK Stack Example (Python):**

```python
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_rds as rds,
    RemovalPolicy
)
from constructs import Construct

class WebAppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC
        vpc = ec2.Vpc(
            self, "AppVPC",
            max_azs=2,
            nat_gateways=1
        )

        # RDS Database
        database = rds.DatabaseInstance(
            self, "Database",
            engine=rds.DatabaseInstanceEngine.mysql(
                version=rds.MysqlEngineVersion.VER_8_0_35
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3,
                ec2.InstanceSize.MICRO
            ),
            vpc=vpc,
            multi_az=True,
            allocated_storage=20,
            database_name="myapp",
            removal_policy=RemovalPolicy.SNAPSHOT
        )

        # ECS Cluster
        cluster = ecs.Cluster(
            self, "AppCluster",
            vpc=vpc
        )

        # Fargate Service with ALB
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "FargateService",
            cluster=cluster,
            cpu=256,
            memory_limit_mib=512,
            desired_count=2,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry("nginx"),
                container_port=80,
                environment={
                    "DB_HOST": database.db_instance_endpoint_address,
                }
            )
        )

        # Allow Fargate to connect to RDS
        database.connections.allow_from(
            fargate_service.service,
            ec2.Port.tcp(3306)
        )
```

**Deploy CDK Stack:**
```bash
# Initialize new project
cdk init app --language python

# Install dependencies
pip install -r requirements.txt

# Synthesize CloudFormation template
cdk synth

# Deploy
cdk deploy

# Destroy
cdk destroy
```

---

### 7.3 Terraform on AWS

**Terraform Configuration:**

```hcl
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.project_name}-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project_name}-igw"
  }
}

# Public Subnet
resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-public-${count.index + 1}"
  }
}

# EC2 Instance
resource "aws_instance" "web" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.public[0].id
  
  vpc_security_group_ids = [aws_security_group.web.id]

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y httpd
              systemctl start httpd
              systemctl enable httpd
              echo "<h1>Hello from Terraform!</h1>" > /var/www/html/index.html
              EOF

  tags = {
    Name = "${var.project_name}-web-server"
  }
}

# Security Group
resource "aws_security_group" "web" {
  name        = "${var.project_name}-web-sg"
  description = "Security group for web server"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.admin_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-web-sg"
  }
}

# Data Sources
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}
```

**Deploy with Terraform:**
```bash
# Initialize
terraform init

# Plan
terraform plan -var="admin_cidr=1.2.3.4/32"

# Apply
terraform apply -var="admin_cidr=1.2.3.4/32"

# Destroy
terraform destroy
```

---

### 7.4 AWS CodePipeline (CI/CD)

**buildspec.yml for CodeBuild:**
```yaml
version: 0.2

phases:
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
      - REPOSITORY_URI=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/myapp
      - COMMIT_HASH=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)
      - IMAGE_TAG=${COMMIT_HASH:=latest}
  
  build:
    commands:
      - echo Build started on `date`
      - echo Building the Docker image...
      - docker build -t $REPOSITORY_URI:latest .
      - docker tag $REPOSITORY_URI:latest $REPOSITORY_URI:$IMAGE_TAG
  
  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing the Docker images...
      - docker push $REPOSITORY_URI:latest
      - docker push $REPOSITORY_URI:$IMAGE_TAG
      - echo Writing image definitions file...
      - printf '[{"name":"myapp","imageUri":"%s"}]' $REPOSITORY_URI:$IMAGE_TAG > imagedefinitions.json

artifacts:
  files:
    - imagedefinitions.json
```

---

<a name="phase-7"></a>
## 8. Phase 7: Advanced Architecture

### 8.1 Multi-Region Architecture

**Multi-Region Deployment Strategy:**

```
Primary Region (us-east-1):
├── Application Stack
│   ├── ALB + EC2/ECS
│   ├── RDS (Multi-AZ)
│   └── ElastiCache
├── Route 53 Health Checks
└── CloudWatch Alarms

Secondary Region (us-west-2):
├── Application Stack (standby)
├── RDS Read Replica
└── S3 Cross-Region Replication

Global Services:
├── Route 53 (Failover routing)
├── CloudFront (Global CDN)
└── S3 (Cross-region replication)
```

---

### 8.2 Disaster Recovery Strategies

**RTO/RPO Matrix:**
```
Strategy          | RTO      | RPO      | Cost | Use Case
------------------|----------|----------|------|------------------
Backup & Restore  | Hours    | Hours    | $    | Non-critical apps
Pilot Light       | Minutes  | Minutes  | $$   | Core services
Warm Standby      | Seconds  | Seconds  | $$$  | Business critical
Multi-Site Active | None     | None     | $$$$ | Mission critical
```

---

### 8.3 Microservices Architecture

**Service Mesh Pattern:**

```
API Gateway
    ↓
Service Mesh (AWS App Mesh)
    ├── User Service (ECS/Fargate)
    │   ├── DynamoDB
    │   └── ElastiCache
    ├── Order Service (ECS/Fargate)
    │   ├── RDS
    │   └── SQS
    ├── Payment Service (Lambda)
    │   └── External API
    └── Notification Service (Lambda)
        ├── SNS
        └── SES
```

---

<a name="phase-8"></a>
## 9. Phase 8: Serverless & Modern Apps

### 9.1 Advanced Lambda Patterns

**Lambda with API Gateway:**

```python
# lambda_function.py
import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

def lambda_handler(event, context):
    """
    RESTful API handler for user management.
    """
    http_method = event['httpMethod']
    path = event['path']
    
    try:
        if http_method == 'GET' and path == '/users':
            return get_users()
        elif http_method == 'GET' and path.startswith('/users/'):
            user_id = path.split('/')[-1]
            return get_user(user_id)
        elif http_method == 'POST' and path == '/users':
            body = json.loads(event['body'])
            return create_user(body)
        elif http_method == 'PUT' and path.startswith('/users/'):
            user_id = path.split('/')[-1]
            body = json.loads(event['body'])
            return update_user(user_id, body)
        elif http_method == 'DELETE' and path.startswith('/users/'):
            user_id = path.split('/')[-1]
            return delete_user(user_id)
        else:
            return response(404, {'error': 'Not found'})
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return response(500, {'error': 'Internal server error'})

def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body)
    }
```

---

### 9.2 Step Functions (Workflow Orchestration)

**Order Processing Workflow:**

```json
{
  "Comment": "Order processing workflow",
  "StartAt": "ValidateOrder",
  "States": {
    "ValidateOrder": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:ValidateOrder",
      "Next": "CheckInventory",
      "Catch": [{
        "ErrorEquals": ["ValidationError"],
        "Next": "OrderFailed"
      }]
    },
    "CheckInventory": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:CheckInventory",
      "Next": "ProcessPayment"
    },
    "ProcessPayment": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:ProcessPayment",
      "Next": "OrderComplete"
    },
    "OrderComplete": {
      "Type": "Succeed"
    },
    "OrderFailed": {
      "Type": "Fail"
    }
  }
}
```

---

### 9.3 Amazon ECS (Elastic Container Service)

**Create ECS Service:**

```bash
# Create cluster
aws ecs create-cluster --cluster-name myapp-cluster

# Register task definition
aws ecs register-task-definition \
  --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
  --cluster myapp-cluster \
  --service-name myapp-service \
  --task-definition myapp-task:1 \
  --desired-count 2 \
  --launch-type FARGATE
```

---

### 9.4 Amazon EKS (Elastic Kubernetes Service)

**Create EKS Cluster:**

```bash
# Create cluster with eksctl
eksctl create cluster \
  --name myapp-cluster \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 3

# Update kubeconfig
aws eks update-kubeconfig \
  --region us-east-1 \
  --name myapp-cluster

# Verify
kubectl get nodes
```

---

<a name="cost-optimization"></a>
## 10. Cost Optimization Strategies

### Monthly Cost Estimates

**Free Tier Project:**
```
EC2 (t2.micro, 750 hrs/month): $0
RDS (db.t2.micro, 750 hrs/month): $0
S3 (5 GB): $0
Total: $0/month
```

**Small Production App:**
```
EC2 (2x t3.small): $30
RDS (db.t3.small, Multi-AZ): $70
ALB: $20
S3 (100 GB): $2.30
CloudFront (1 TB): $85
Total: ~$207/month
```

**Medium Production App:**
```
ECS Fargate (4 tasks): $100
RDS (db.r5.large, Multi-AZ): $350
ElastiCache (cache.t3.micro): $25
ALB: $20
S3 (1 TB): $23
CloudFront (10 TB): $850
Total: ~$1,368/month
```

### Cost Optimization Tips

**1. Right-Sizing:**
```bash
# Use AWS Compute Optimizer
aws compute-optimizer get-ec2-instance-recommendations
```

**2. Reserved Instances & Savings Plans:**
```
EC2 Reserved Instances:
- 1-year: 40% savings
- 3-year: 60% savings

Compute Savings Plans:
- Flexible across instance types
- Up to 66% savings
```

**3. Spot Instances:**
```bash
# Launch spot instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.micro \
  --instance-market-options '{
    "MarketType": "spot",
    "SpotOptions": {
      "MaxPrice": "0.01"
    }
  }'
```

---

<a name="best-practices"></a>
## 11. Best Practices & Security

### Security Best Practices

**1. IAM Security:**
```
✓ Enable MFA for all users
✓ Use IAM roles, not access keys
✓ Implement least privilege
✓ Rotate credentials regularly
✓ Use IAM Access Analyzer
✓ Enable CloudTrail logging
✗ Never commit credentials to code
✗ Don't use root account
```

**2. Network Security:**
```
✓ Use private subnets for databases
✓ Implement NACLs and Security Groups
✓ Use VPN or Direct Connect
✓ Enable VPC Flow Logs
✓ Use WAF for web applications
✓ Implement DDoS protection (Shield)
```

**3. Data Protection:**
```
✓ Encrypt data at rest (KMS)
✓ Encrypt data in transit (TLS)
✓ Enable S3 versioning
✓ Use S3 Object Lock for compliance
✓ Regular backups and snapshots
✓ Test disaster recovery procedures
```

### Well-Architected Framework

**Five Pillars:**

**1. Operational Excellence**
- Automate changes
- Respond to events
- Define standards

**2. Security**
- Implement defense in depth
- Enable traceability
- Apply security at all layers

**3. Reliability**
- Test recovery procedures
- Scale horizontally
- Manage change through automation

**4. Performance Efficiency**
- Use appropriate technology
- Go global in minutes
- Use serverless architectures

**5. Cost Optimization**
- Adopt consumption model
- Measure overall efficiency
- Use managed services

---

<a name="resources"></a>
## 12. Learning Resources

### Official AWS Resources

**Free Training:**
- AWS Skill Builder (free tier)
- AWS Technical Essentials
- AWS Cloud Quest (gamified learning)
- AWS Workshops (hands-on labs)

**Documentation:**
- AWS Documentation
- AWS Architecture Center
- AWS Whitepapers
- AWS Well-Architected Framework

**Community:**
- AWS re:Invent videos (YouTube)
- AWS Forums
- Reddit: r/aws, r/AWSCertifications
- AWS User Groups (local meetups)

### Online Courses

**Video Courses:**
1. **A Cloud Guru / Pluralsight**
   - Comprehensive coverage
   - Hands-on labs
   - $29-49/month

2. **Udemy - Stephane Maarek**
   - Solutions Architect course
   - Developer course
   - $10-20 (on sale)

3. **Coursera - AWS Fundamentals**
   - Free to audit
   - University-backed
   - Self-paced

### Practice Platforms

1. **TutorialsDojo**
   - Practice exams
   - Detailed explanations
   - $15-20 per exam

2. **Whizlabs**
   - Practice tests
   - Hands-on labs
   - $20-30

3. **AWS Free Tier Account**
   - Hands-on practice
   - Real environment
   - 12 months free

---

## Conclusion

This roadmap provides a comprehensive path from AWS beginner to Solutions Architect. Key success factors:

1. **Consistent Practice**: Hands-on experience is crucial
2. **Budget Management**: Use free tier wisely
3. **Build Projects**: Portfolio demonstrates skills
4. **Get Certified**: Validates your knowledge
5. **Stay Updated**: AWS launches new services constantly
6. **Join Community**: Learn from others' experiences

**Next Steps:**
1. Create your AWS account today
2. Start with Phase 1
3. Build your first project
4. Join AWS community forums
5. Schedule your certification exam

Good luck on your AWS journey!

---

**Additional Resources:**
- AWS Blog: https://aws.amazon.com/blogs/
- AWS News: https://aws.amazon.com/new/
- AWS Events: https://aws.amazon.com/events/
- AWS Training: https://aws.amazon.com/training/

**Support:**
- AWS Support Plans: https://aws.amazon.com/premiumsupport/
- AWS Forums: https://forums.aws.amazon.com/
- Stack Overflow: [aws] tag