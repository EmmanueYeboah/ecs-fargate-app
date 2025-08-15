terraform {
  # Using local backend for now
  # backend "s3" {
  #   bucket         = "your-terraform-state-bucket"
  #   key            = "ecs-fargate-app/terraform.tfstate"
  #   region         = "us-east-2"
  #   dynamodb_table = "terraform-lock-table"
  #   encrypt        = true
  # }
}



output "ecs_cluster_name" {
  value = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  value = aws_ecs_service.app.name
}
