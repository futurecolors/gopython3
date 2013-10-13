# coding: utf-8
import factory
from .models import Job, Package, Spec


class JobFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Job

    @factory.post_generation
    def specs(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for spec in extracted:
                self.specs.add(spec)


class PackageFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Package


class SpecFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Spec
    package = factory.SubFactory(PackageFactory)
