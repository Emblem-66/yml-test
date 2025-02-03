import yaml
import subprocess

# Load the YAML configuration
with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

# Extract configurations
base_image = config.get("image", "quay.io/fedora/fedora-silverblue:latest")
copr_repos = config.get("copr", {}).get("enable", [])
include_packages = config.get("packages", {}).get("include", [])
exclude_packages = config.get("packages", {}).get("exclude", [])
systemd_services = config.get("systemd", {}).get("enable", [])

# Generate base Dockerfile
with open("Dockerfile", "w") as dockerfile:
    dockerfile.write(f"FROM {base_image}\n")
    dockerfile.write("RUN dnf -y install dnf-plugins-core\n")
    dockerfile.write("RUN dnf -y install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm\n")
    
    # Enable COPR repositories
    for repo in copr_repos:
        dockerfile.write(f"RUN dnf copr enable -y {repo}\n")
    
    # Install packages
    if include_packages:
        packages = " ".join(include_packages)
        dockerfile.write(f"RUN dnf -y install {packages}\n")
    
    # Exclude packages
    if exclude_packages:
        packages = " ".join(exclude_packages)
        dockerfile.write(f"RUN dnf -y remove {packages}\n")
    
    # Enable systemd services
    for service in systemd_services:
        dockerfile.write(f"RUN systemctl enable {service}\n")
