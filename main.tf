data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }
}

resource "aws_instance" "my_vm" {
  ami           = coalesce(var.ami_id, data.aws_ami.amazon_linux.id)
  instance_type = var.instance_type

  tags = {
    Hello     = "World"
    Name      = var.instance_name
    Project   = var.project_name
    ManagedBy = "Terraform"
    Owner     = "Thiago Gomes"
  }
}
