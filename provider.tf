terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Course     = "Engenharia de Software"
      IaCTool    = "Terraform"
      Repository = "terraform-cloudbolt-iac-lab"
    }
  }
}

