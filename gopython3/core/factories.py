# coding: utf-8
import factory
from .models import Job, Package, Spec, Line


class JobFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Job

    @factory.post_generation
    def lines(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for line in extracted:
                LineFactory(job=self, text=line)

    @factory.post_generation
    def specs(self, create, extracted, **kwargs):
        # TODO: merge with lines
        if not create:
            return

        if extracted:
            for line in extracted:
                name, version = line.split('==')
                spec = SpecFactory(version=version, package__name=name)
                LineFactory(job=self, spec=spec, text=line, status='parsed')


class PackageFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Package


class SpecFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Spec
    package = factory.SubFactory(PackageFactory)


class LineFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Line
