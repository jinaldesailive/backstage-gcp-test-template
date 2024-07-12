##########################################
# REQUIRED INPUTS
##########################################

variable "project_id" {
  type        = string
  description = "GCP Project ID to provision resources in."
}

variable "app_name" {
  type        = string
  description = "Cloud Run Service name"
}
##########################################
# OPTIONAL INPUTS
##########################################

variable "region" {
  type        = string
  description = "GCP Region to provision resources in."
  default     = "us-east4"
}

# variable "dockerimage" {
#   type        = string
#   description = "Docker image URL"
# }