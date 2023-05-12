import argparse
import os

from google.cloud import compute


def create_vm(project_id, zone, machine_type, image_name, name):
  """Creates a VM on Google Cloud with the specified specifications.

  Args:
    project_id: The ID of the Google Cloud project.
    zone: The zone where the VM should be created.
    machine_type: The machine type of the VM.
    image_name: The name of the image to use for the VM.
    name: The name of the VM.

  Returns:
    The VM object.
  """

  client = compute.Client()

  # Create the VM instance.
  instance = client.instances().create(
      project=project_id,
      zone=zone,
      machine_type=machine_type,
      image=image_name,
      name=name,
      metadata={
          'startup-script': """
            sudo apt-get update
            sudo apt-get install -y chromium-browser firefox selenium-server-standalone cypress jest
            echo "Hello, world!" > /home/user/hello.txt
          """
      })

  # Wait for the VM to be created.
  instance.wait_until_ready()

  return instance


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--project_id', type=str, required=True)
  parser.add_argument('--zone', type=str, required=True)
  parser.add_argument('--machine_type', type=str, required=True)
  parser.add_argument('--image_name', type=str, required=True)
  parser.add_argument('--name', type=str, required=True)

  args = parser.parse_args()

  # Create the VM.
  vm = create_vm(
      args.project_id,
      args.zone,
      args.machine_type,
      args.image_name,
      args.name)

  # Print the VM's IP address.
  print(vm.network_interfaces[0].access_configs[0].assigned_nat_ip)
