resource "aws_vpc" "portfolio_project_vpc" {
    cidr_block = "10.0.0.0/16"

    tags = {
        Name = "portfolio-project-vpc"
    }
}

resource "aws_subnet" "portfolio_project_subnet" {
    vpc_id            = aws_vpc.portfolio_project_vpc.id
    cidr_block        =  "10.0.1.0/24"
    availability_zone = "ap-south-1a"
    tags = {
        Name = "portfolio-project-subnet"
    }
}


resource "aws_internet_gateway" "portfolio_project_igw" {
  vpc_id = aws_vpc.portfolio_project_vpc.id

  tags = {
    Name = "portfolio-project-igw"
  }
}

resource "aws_route_table" "portfolio_project_route_table" {
  vpc_id = aws_vpc.portfolio_project_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.portfolio_project_igw.id
  }
}

resource "aws_route_table_association" "portfolio_project_route_table_association" {
  subnet_id      = aws_subnet.portfolio_project_subnet.id
  route_table_id = aws_route_table.portfolio_project_route_table.id
}



resource "aws_security_group" "k8s_sg" {
name        = "k8s-sg"
description = "Security Group for Kubernetes Cluster"
vpc_id      = aws_vpc.portfolio_project_vpc.id

ingress {
description = "SSH"
from_port   = 22
to_port     = 22
protocol    = "tcp"
cidr_blocks = ["0.0.0.0/0"]
}

ingress {
description = "HTTP"
from_port   = 80
to_port     = 80
protocol    = "tcp"
cidr_blocks = ["0.0.0.0/0"]
}

ingress {
description = "HTTPS"
from_port   = 443
to_port     = 443
protocol    = "tcp"
cidr_blocks = ["0.0.0.0/0"]
}

ingress {
description = "Jenkins"
from_port   = 8080
to_port     = 8080
protocol    = "tcp"
cidr_blocks = ["0.0.0.0/0"]
}

ingress {
description = "Kubernetes API Server"
from_port   = 6443
to_port     = 6443
protocol    = "tcp"
cidr_blocks = ["0.0.0.0/0"]
}

ingress {
description = "Kubelet"
from_port   = 10250
to_port     = 10250
protocol    = "tcp"
cidr_blocks = ["0.0.0.0/0"]
}

ingress {
description = "NodePort Services"
from_port   = 30000
to_port     = 32767
protocol    = "tcp"
cidr_blocks = ["0.0.0.0/0"]
}

egress {
from_port   = 0
to_port     = 0
protocol    = "-1"
cidr_blocks = ["0.0.0.0/0"]
}

tags = {
Name = "k8s-sg"
}
}


resource "aws_instance" "master_ec2" {
    ami           = "ami-006f82a1d5a27da54"
    instance_type = "t2.medium"
    key_name      = "k8s-key"
    vpc_security_group_ids = [aws_security_group.k8s_sg.id]
    subnet_id = aws_subnet.portfolio_project_subnet.id
    associate_public_ip_address = true

    tags = {
        Name = "Master-EC2"
    }
  
}

resource "aws_instance" "worker_ec2" {
    ami           = "ami-006f82a1d5a27da54"
    instance_type = "t2.medium"
    key_name      = "k8s-key"
    vpc_security_group_ids = [aws_security_group.k8s_sg.id]
    subnet_id = aws_subnet.portfolio_project_subnet.id
    associate_public_ip_address = true

    tags = {
        Name = "Worker-EC2"
    }
  
}

output "master_ip" {
  value = aws_instance.master_ec2.public_ip
}

output "worker_ip" {
  value = aws_instance.worker_ec2.public_ip
}