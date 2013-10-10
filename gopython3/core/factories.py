# coding: utf-8
import factory
from .models import Job, Package, Spec


class JobFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Job


class PackageFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Package


class SpecFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Spec
    package = factory.SubFactory(PackageFactory)
