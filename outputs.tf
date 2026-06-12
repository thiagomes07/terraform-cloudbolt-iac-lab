output "instance_id" {
  description = "ID of the EC2 instance managed by Terraform."
  value       = aws_instance.my_vm.id
}

output "instance_state" {
  description = "Current state reported for the EC2 instance."
  value       = aws_instance.my_vm.instance_state
}

output "availability_zone" {
  description = "Availability zone chosen by AWS for the instance."
  value       = aws_instance.my_vm.availability_zone
}

output "public_ip" {
  description = "Public IP assigned to the instance, when available."
  value       = aws_instance.my_vm.public_ip
}

output "selected_ami" {
  description = "AMI used to create the EC2 instance."
  value       = aws_instance.my_vm.ami
}

