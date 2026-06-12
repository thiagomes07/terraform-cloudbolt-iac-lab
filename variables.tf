variable "region" {
  type        = string
  description = "AWS region used in the lab."
  default     = "us-east-1"
}

variable "ami_id" {
  type        = string
  description = "Optional AMI override. When null, Terraform selects the latest Amazon Linux 2023 AMI."
  default     = null
  nullable    = true
}

variable "instance_type" {
  type        = string
  description = "EC2 instance size used in the practical lab."
  default     = "t3.micro"

  validation {
    condition     = contains(["t2.micro", "t3.micro"], var.instance_type)
    error_message = "Use t2.micro or t3.micro to keep the lab small and low cost."
  }
}

variable "instance_name" {
  type        = string
  description = "Name tag for the EC2 instance."
  default     = "terraform-cloudbolt-lab-ec2"
}

variable "project_name" {
  type        = string
  description = "Project tag used to find all resources created by this activity."
  default     = "terraform-cloudbolt-iac-lab"
}
