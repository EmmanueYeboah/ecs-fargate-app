# ECS Fargate Containerized Application

A production-ready containerized application deployed on AWS ECS Fargate with complete infrastructure automation, auto-scaling, and security controls.

## Architecture

- **ECS Fargate**: Serverless container orchestration
- **Application Load Balancer**: Traffic distribution and health checks
- **Auto Scaling**: CPU and memory-based scaling (2-10 instances)
- **WAF**: Application-layer protection with managed rule sets
- **ECR**: Container image registry with vulnerability scanning
- **VPC**: Multi-AZ deployment across 2 availability zones

## Features

✅ **Zero-downtime deployments** via GitHub Actions  
✅ **Auto scaling** based on CPU (70%) and memory (80%) utilization  
✅ **WAF protection** with rate limiting (2000 req/5min per IP)  
✅ **OIDC authentication** for secure CI/CD  
✅ **Container vulnerability scanning** with Trivy  
✅ **Infrastructure as Code** with Terraform  

## Quick Start

### Prerequisites
- AWS CLI configured
- Terraform installed
- Docker installed
- Python 3 (for load testing)

### Deployment

1. **Deploy Infrastructure**
   ```bash
   cd terraform
   terraform init
   terraform apply
   ```

2. **Build & Deploy Application**
   - Push to `main` branch triggers automatic deployment
   - GitHub Actions builds Docker image and updates ECS service

3. **Access Application**
   ```bash
   curl http://ecs-fargate-alb-1462992800.us-east-2.elb.amazonaws.com
   ```

## Load Testing

Test auto-scaling behavior:

```bash
# Install dependencies
pip install requests

# Run 5-minute load test with 50 concurrent requests
python3 load-test.py 5 50
```

Monitor scaling in AWS Console:
- ECS → Clusters → ecs-fargate-cluster → Services
- CloudWatch → Metrics → ECS

## Infrastructure Components

### Networking
- **VPC**: Custom VPC with public subnets
- **Subnets**: 2 public subnets across different AZs
- **Security Groups**: Restricted access (ALB: 80, ECS: 8080)

### Compute
- **ECS Cluster**: Fargate cluster for serverless containers
- **Task Definition**: 256 CPU, 512 MB memory
- **Service**: Desired count 2, max 10 instances

### Security
- **WAF**: AWS managed rules + rate limiting
- **IAM**: Least privilege roles for ECS and GitHub Actions
- **ECR**: Image scanning enabled

### Monitoring
- **CloudWatch**: Container logs and metrics
- **ALB Health Checks**: Application health monitoring

## CI/CD Pipeline

### Terraform Deploy Workflow
- Triggers on push to `main`
- Deploys infrastructure changes
- Uses OIDC for secure authentication

### Docker Build & Push Workflow
- Triggers after successful Terraform deployment
- Builds Docker image with commit SHA tag
- Scans for vulnerabilities
- Pushes to ECR
- Updates ECS service
- Waits for deployment completion

## Auto Scaling Configuration

- **Min Capacity**: 2 instances
- **Max Capacity**: 10 instances
- **CPU Target**: 70% utilization
- **Memory Target**: 80% utilization
- **Scale-out**: Add instances when thresholds exceeded
- **Scale-in**: Remove instances when utilization drops

## WAF Rules

1. **AWS Managed Common Rule Set**: OWASP Top 10 protection
2. **Known Bad Inputs**: Malicious request patterns
3. **Rate Limiting**: 2000 requests per 5 minutes per IP

## Monitoring & Observability

- **Application Logs**: CloudWatch Logs `/ecs/ecs-fargate-app`
- **Metrics**: ECS service metrics in CloudWatch
- **WAF Metrics**: Request blocking and rate limiting stats
- **ALB Metrics**: Request count, latency, error rates

## Cost Optimization

- **Fargate**: Pay only for running containers
- **Auto Scaling**: Scales down during low traffic
- **Spot Instances**: Not used (Fargate doesn't support)
- **Resource Right-sizing**: 256 CPU, 512 MB memory

## Security Best Practices

- **Network Isolation**: Private subnets for containers
- **Least Privilege IAM**: Minimal required permissions
- **Container Scanning**: Vulnerability detection
- **WAF Protection**: Application-layer security
- **HTTPS**: SSL termination at ALB (configure certificate)

## Troubleshooting

### Common Issues

1. **Service not starting**: Check CloudWatch logs
2. **Health check failures**: Verify application port 8080
3. **Auto scaling not working**: Check CloudWatch metrics
4. **WAF blocking requests**: Review WAF logs

### Useful Commands

```bash
# Check ECS service status
aws ecs describe-services --cluster ecs-fargate-cluster --services ecs-fargate-service

# View container logs
aws logs tail /ecs/ecs-fargate-app --follow

# Check auto scaling policies
aws application-autoscaling describe-scaling-policies --service-namespace ecs
```

## Project Structure

```
ecs-fargate-app/
├── .github/workflows/          # CI/CD pipelines
│   ├── terraform-deploy.yml    # Infrastructure deployment
│   └── docker-push.yml         # Application deployment
├── terraform/                  # Infrastructure as Code
│   ├── main.tf                 # Main configuration
│   ├── vpc.tf                  # Networking
│   ├── ecs.tf                  # Container orchestration
│   ├── alb.tf                  # Load balancer
│   ├── autoscaling.tf          # Auto scaling policies
│   ├── waf.tf                  # Web Application Firewall
│   └── iam-github-oidc.tf      # OIDC authentication
├── application/                # Application code
│   ├── app.py                  # Flask application
│   ├── Dockerfile              # Container definition
│   └── requirements.txt        # Python dependencies
├── load-test.py                # Load testing script
└── README.md                   # This file
```

