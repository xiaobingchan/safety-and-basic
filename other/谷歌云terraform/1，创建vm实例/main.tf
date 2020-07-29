provider "google" {
 credentials = file("tertest-284114-3ad39311086e.json")
 project     = "tertest-284114"
 region      = "us-central1"
}

resource "random_id" "instance_id" {
 byte_length = 8
}

resource "google_compute_instance" "default" {
 name         = "flask-vm-${random_id.instance_id.hex}"
 machine_type = "f1-micro"
 zone         = "us-central1-a"

metadata = {
   ssh-keys = "root:${file("~/.ssh/id_rsa.pub")}"
 }
 
 boot_disk {
   initialize_params {
     image = "centos-7-v20200714"
   }
 }

metadata_startup_script = "yum install -y build-essential python-pip; pip install flask"

network_interface {
   network = "default"
   access_config {

   }
 }
}
output "ip" {
  value = google_compute_instance.default.network_interface[0].access_config[0].nat_ip
}

