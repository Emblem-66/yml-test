# python script to translate config.yml for fedora image build wia github actions and podman from Containerfile

import yaml
import subprocess

# Load the YAML configuration
with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

# config.yml structure
'''
name: pyblue
description: Silverblue variants built using Python

image:
  - quay.io/fedora-ostree-desktops/base-atomic:rawhide
  #- quay.io/fedora/silverblue:latest

setup:
  copy_files: True
  auto_updates: True
  flathub: True

  repositories:
    rpmfusion: True
    terra: True
    copr:
      - author/repo

  desktop:
    - gnome
    #- hyprland

  modules:
    - module.yml

  packages:
    include:
      - package
    exclude:
      - package

  services:
    enable:
      - service.service
    disable:
      - service.service
'''

# Extract configurations
image_name = config.get("name", [])
base_image = config.get("image", [])
files_to_copy = config.get("files", [])
repositories = config.get("repositories", {})
copr_repos = config.get("repositories", {}).get("copr", [])
include_packages = config.get("packages", {}).get("include", [])
exclude_packages = config.get("packages", {}).get("exclude", [])
local_packages = config.get("packages", {}).get("local", [])
modules = config.get("modules", [])
autoupdates = config.get("services", {}).get("autoupdates", False)
systemd_services = config.get("services", {}).get("enable", [])

# Generate base Containerfile
with open("Containerfile", "w") as Containerfile:
    # Write base image and release
    Containerfile.write(f"FROM {base_image}:{release}\n")
    Containerfile.write("RUN dnf -y install dnf-plugins-core\n")
    
    
    # Copy files
    if repositories.get("copy_files", False):
    Containerfile.write("COPY rootfs/ /\n")
    # Auto updates
    if repositories.get("auto_updates", False):

    # Setup Flathub
    if repositories.get("flathub", False):

    
    # Enable repositories (rpmfusion, terra, etc.)
    if repositories.get("rpmfusion", False):
        Containerfile.write("RUN dnf -y install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm\n")
    if repositories.get("terra", False):
        Containerfile.write("RUN dnf -y install --nogpgcheck --repofrompath 'terra,https://repos.fyralabs.com/terra$releasever' terra-release\n")
    for repo in copr_repos:
        Containerfile.write(f"RUN dnf copr enable -y {repo}\n")

    # Desktop module 


    # Handle modules (complex installs)
    for module in modules:
        # Assuming modules are pre-existing YAML files that describe complex installations
        Containerfile.write(f"# Including module {module}\n")
        # (You'd need logic to apply the module configs, depending on your use case)

    # Install packages
    if include_packages:
        packages = " ".join(include_packages)
        Containerfile.write(f"RUN dnf -y install {packages}\n")
    
    # Exclude packages
    if exclude_packages:
        packages = " ".join(exclude_packages)
        Containerfile.write(f"RUN dnf -y remove {packages}\n")
    
    # Handle local packages (e.g., custom RPMs)
    if local_packages:
        # Assuming you'd manually copy local RPM files before building
        #Containerfile.write("COPY local-rpm/ /tmp/\n")
        Containerfile.write("RUN dnf -y install /tmp/*.rpm\n")
    
    # Enable systemd services (if applicable)
    if systemd_services:
        for service in systemd_services:
            Containerfile.write(f"RUN systemctl enable {service}\n")
    
    # Handle autoupdates service (if enabled)
    if autoupdates:
        Containerfile.write("RUN systemctl enable rpm-ostreed-automatic.service\n")

# Optionally, push the image or build it in GitHub Actions or manually via CLI.