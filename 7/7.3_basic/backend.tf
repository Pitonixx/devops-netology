terraform {
  backend "s3" {
    bucket = "pitonix-trf-state"
    key    = "main/terraform.tfstate"
    region = "eu-west-2"
  }
}