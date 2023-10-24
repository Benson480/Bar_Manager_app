import os

# List of packages to install
packages_to_install = [
    "django",
    "django-admin-interface",
    "PyYAML",
    "django-crispy-forms",
    "django-flat-responsive",
    "django-flat-theme",
    "django-admin-menu",
    "django-axes",
    "django-crispy-bootstrap",
    "crispy_bootstrap4",
    "django-widget-tweaks",
    "django-allauth",
    "django-allauth==0.48.0",
    "django-allauth[google]",
    "matplotlib",
    "djangorestframework",
    "django-mpesa",

]

# Loop through the list and install each package
for package in packages_to_install:
    os.system(f"pip install {package}")
