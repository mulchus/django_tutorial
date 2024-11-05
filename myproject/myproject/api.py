from typing import List

from django.shortcuts import get_object_or_404
from employees.models import Employee, Department
from employees.schemas import UserSchema, Error, DepartmentIn, EmployeeIn, EmployeeOut, OkSchema
from ninja import NinjaAPI, Router

api = NinjaAPI()
router = Router()


@router.post("/departments")
def create_department(request, payload: DepartmentIn):
    department = Department.objects.create(**payload.dict())
    return {"id": department.id}


@router.post("/employees")
def create_employee(request, payload: EmployeeIn):
    employee = Employee.objects.create(**payload.dict())
    return {"id": employee.id}


@router.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee


@router.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    return Employee.objects.all()


@router.put("/employees/{employee_id}", response={200: OkSchema, 404: Error})
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    department = Department.objects.filter(id=payload.department_id).exists()
    if not department:
        return 404, Error(message="Department not found")
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return OkSchema


@router.delete("/employees/{employee_id}", response={200: OkSchema, 404: Error})
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return OkSchema


@router.get("/me", response={200: UserSchema, 403: Error})
def me(request):
    if not request.user.is_authenticated:
        return 403, {"message": "Please sign in first"}
    return request.user


api.add_router("", router)
