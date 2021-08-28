""" Single Responsibility Principle

The principle implies that module class or function should be responsible only for a single part of the functionality.
Robert Martin states that a class or module should have only one reason to be changed (i.e. refactored).

Following the principle makes classes/modules less fragile, more reusable, and maintainable.
"""

import abc
import dns

from typing import Type

""" Consider the following high-level DNS zone class:
It is capable of:
    - creating a backup of DNS zone
    - restoring the backup
    - checking if DNS zone has valid syntax
    - incrementing SOA
    - giving you access to low-level representation of zone (dnspython)
"""


class DNSZone(abc.ABC):
    zone_name: str

    def __init__(self, zone_name: str):
        self.zone_name = zone_name

    @property
    def zone(self) -> dns.zone.Zone:
        pass

    def backup(self):
        pass

    def restore(self):
        pass

    def is_valid(self):
        pass

    def increment_soa(self):
        pass


"""Now let's imagine that we want to extend the class and add a possibility
to set up an abstract CDN.
"""


class DNSZone(abc.ABC):
    zone_name: str

    def __init__(self, zone_name: str):
        self.zone_name = zone_name

    @property
    def zone(self) -> dns.zone.Zone:
        pass

    def backup(self):
        pass

    def restore(self):
        pass

    def is_valid(self):
        pass

    def increment_soa(self):
        pass

    def setup_cdn(self, domain: str):
        pass

    def disable_cdn(self, domain: str):
        pass

    def enable_cdn(self, domain: str):
        pass


""" The mere fact that we have to add a suffix `_cdn` to each CDN-related method
should bring us to a thought that we are doing something wrong.

A new version of class DNSZone is responsible for more than one thing, thus, violates SRP:
    - manages DNS zone
    - performs high-level business-related operations (configure CDN) 

The second iteration of the class has more than one reason to change. You will come back to it
more frequently, touching code you don't need to.

Now consider the design below.
"""


class CdnManager(abc.ABC):
    domain: str
    zone: Type[DNSZone]

    def __init__(self, domain: str):
        self.domain = domain
        self.zone = DNSZone(domain)

    def setup(self):
        pass

    def disable(self):
        pass

    def enable(self):
        pass


"""
CDN-related business logic is encapsulated in a separate class. Should anything CDN-related change, you don't need
to touch the DNSZone class.
"""
