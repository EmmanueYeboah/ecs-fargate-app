terraform {
  backend "s3" {
    bucket  = "terraform-state-apple-1755178786"
    key     = "ecs-fargate-app/terraform.tfstate"
    region  = "us-east-2"
    encrypt = true
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