import random
import string

from django.test import TestCase

from crm.contractors.tests.factories import ContractorFactory


class ContractorTest(TestCase):
    def random_name(self, length):
        letters = string.ascii_lowercase
        name = "".join(random.choice(letters) for _ in range(length))
        return name

    def create_contractor_name(self, name):
        contractor = ContractorFactory()
        contractor.name = name
        contractor.save()
        return contractor

    def create_contractor_code(self):
        contractor = ContractorFactory()
        contractor.code = None
        contractor.save()
        return contractor

    def test_split_name_contractor(self):
        lengths = [10, 49, 50, 51, 75, 100, 125]
        for i in lengths:
            name = self.random_name(i)
            contractor = self.create_contractor_name(name)
            name1 = contractor.name
            name2 = None
            name3 = None
            if len(contractor.name) > 50:
                name1 = contractor.name[:50]
                if len(contractor.name) > 100:
                    name2 = contractor.name[51:100]
                    name3 = contractor.name[100:]
                else:
                    name2 = contractor.name[51:]

            self.assertEqual(contractor.name, name)
            self.assertEqual(contractor.name1, name1)
            self.assertEqual(contractor.name2, name2)
            self.assertEqual(contractor.name3, name3)

    def test_code_contractor(self):
        contractor = self.create_contractor_code()
        self.assertEqual(contractor.code, contractor.tax_number)

    def test_str_contractor(self):
        contractor = ContractorFactory()
        self.assertEqual(contractor.name, contractor.__str__())
