from django.test import TestCase

# Create your tests here.
import pkg_resources
print(pkg_resources.get_distribution("django-cors-headers").version)