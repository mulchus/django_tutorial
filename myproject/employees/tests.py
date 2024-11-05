import datetime

from myproject.api import router
from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from employees.models import Department, Employee
from ninja.testing import TestClient


class APITestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='admin', password='admin')
        cls.department = Department.objects.create(title='Department')
        cls.other_dep = Department.objects.create(title='Department2')
        cls.employee = Employee.objects.create(
            first_name='John',
            last_name='Doe',
            department_id=cls.department.id,
            birthdate='1990-01-01'
        )
        cls.login_client = Client()
        cls.login_client.login(username=cls.user.username, password=cls.user.password)

    def setUp(self):
        self.client = TestClient(router)

    def test_create_employee(self):
        payload = {
            "first_name": "Jane",
            "last_name": "Smith",
            "department_id": 1,
            "birthdate": "1990-01-01"
        }
        response = self.client.post("/employees", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json())

    def test_create_department(self):
        payload = {
            "title": "test_dep"
        }
        response = self.client.post("/departments", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json())

    def test_get_employee(self):
        response = self.client.get(f"/employees/{self.employee.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json())
        # with self.assertRaises(Http404):
        #     self.client.get(f"/employees/2")
        response = self.client.get(f"/employees/{self.employee.id + 1000}")
        self.assertEqual(response.status_code, 404)
        response = self.client.get(f"/employees/sdfgsdfgs")
        self.assertEqual(response.status_code, 422)

    def test_update_employee(self):
        new_employee = {
            "first_name": "Valera",
            "last_name": "Smith",
            "department_id": self.other_dep.id,
            "birthdate": datetime.date(1993, 1, 1)
        }
        response = self.client.put(f"/employees/{self.employee.id}", json=new_employee)
        self.assertEqual(response.status_code, 200)
        self.employee.refresh_from_db()
        for key, value in new_employee.items():
            self.assertEqual(getattr(self.employee, key), value)

    def test_update_non_existent_employee(self):
        new_employee = {
            "first_name": "Valera",
            "last_name": "Smith",
            "department_id": self.other_dep.id + 100,
            "birthdate": datetime.date(1993, 1, 1)
        }
        response = self.client.put(f"/employees/{self.employee.id}", json=new_employee)
        self.assertEqual(response.status_code, 404)
        self.employee.refresh_from_db()
        for key, value in new_employee.items():
            self.assertNotEqual(getattr(self.employee, key), value)

    def test_delete_employee(self):
        response = self.client.delete(f"/employees/{self.employee.id}")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Employee.objects.filter(id=self.employee.id).exists())

    def test_delete_nonexisting_employee(self):
        response = self.client.delete(f"/employees/{self.employee.id + 1000}")
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Employee.objects.filter(id=self.employee.id).exists())

    def test_me(self):
        response = self.client.get("/me")
        self.assertEqual(response.status_code, 403)
        client = Client()
        client.force_login(self.user)
        self.assertTrue(self.user.is_authenticated)
