# coding: utf-8
from django.contrib.admin import AdminSite
from django.test import TestCase
from core.admin import JobAdmin, SpeckAdmin, PackageAdmin
from core.models import Job, Spec, Package


class TestAdmin(TestCase):

    def setUp(self):
        self.site = AdminSite()

    def test_job_admin_works(self):
        JobAdmin(Job, self.site).validate(Job)

    def test_spec_admin_works(self):
        SpeckAdmin(Spec, self.site).validate(Spec)

    def test_package_admin_works(self):
        PackageAdmin(Package, self.site).validate(Package)

