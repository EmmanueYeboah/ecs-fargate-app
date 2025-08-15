variable "aws_region" {
  default = "us-east-2"
}

variable "ecr_repo_name" {
  default = "my-ecs-app"
}

variable "tags" {
  type = map(string)
  default = {
    Project     = "ecs-fargate-app"
    Environment = "dev"
    ManagedBy   = "Terraform"
  }
}
