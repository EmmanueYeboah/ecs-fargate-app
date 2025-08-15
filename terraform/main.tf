terraform {
  backend "s3" {
    bucket         = "your-terraform-state-bucket"
    key            = "ecs-fargate-app/terraform.tfstate"
    region         = "us-east-2"
    dynamodb_table = "terraform-lock-table"
    encrypt        = true
  }
}

provider "aws" {
  region = "us-east-2"
}

resource "aws_ecr_repository" "app_repo" {
  name                 = "ecs-fargate-app"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

output "ecr_repository_url" {
  value = aws_ecr_repository.app_repo.repository_url
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  value = aws_ecs_service.app.name
}
