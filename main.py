import json
from pathlib import Path
from abc import ABC, abstractmethod

DATA_DIR = Path(__file__).parent / "data"


class Employee(ABC):
    def __init__(self, emp_id, name, base_salary, bonus_code):
        self.emp_id = emp_id
        self.name = name
        self.base_salary = float(base_salary)
        self.bonus_code = bonus_code

    def calculate_bonus(self):
        bonus_rules = {"PERF2026": 0.05, "SENIOR10": 0.10, "LEAD2026": 0.15}
        return self.base_salary * bonus_rules.get(self.bonus_code, 0)

    @abstractmethod
    def calculate_salary(self):
        pass

    def show_data(self):
        return {
            "ID": self.emp_id,
            "Nama": self.name,
            "Status": self.__class__.__name__,
            "Gaji Pokok": self.base_salary,
            "Bonus": self.calculate_bonus(),
            "Total Gaji": self.calculate_salary()
        }


class PermanentEmployee(Employee):
    def calculate_salary(self):
        allowance = self.base_salary * 0.10
        return self.base_salary + allowance + self.calculate_bonus()


class ContractEmployee(Employee):
    def calculate_salary(self):
        return self.base_salary + self.calculate_bonus()


def create_employee(data):
    employee_class = PermanentEmployee if data["is_permanent"] else ContractEmployee
    return employee_class(data["emp_id"], data["name"],
                          data["base_salary"], data["bonus_code"])


class Sensor(ABC):
    def __init__(self, sensor_id, location, temperature, operator_id):
        self.sensor_id = sensor_id
        self.location = location
        self.temperature = float(temperature)
        self.operator_id = operator_id

    @abstractmethod
    def get_status(self):
        pass

    @abstractmethod
    def get_action(self):
        pass

    def show_data(self):
        return {
            "ID Sensor": self.sensor_id,
            "Lokasi": self.location,
            "Suhu": self.temperature,
            "Status": self.get_status(),
            "Operator": self.operator_id,
            "Tindakan": self.get_action()
        }


class DangerSensor(Sensor):
    def get_status(self):
        return "DANGER"

    def get_action(self):
        return "Alarm dan pemeriksaan segera"


class WarningSensor(Sensor):
    def get_status(self):
        return "WARNING"

    def get_action(self):
        return "Periksa dan pantau suhu"


class NormalSensor(Sensor):
    def get_status(self):
        return "NORMAL"

    def get_action(self):
        return "Kondisi normal"


def create_sensor(data):
    temperature = float(data["temperature"])
    if temperature >= 85:
        sensor_class = DangerSensor
    elif temperature >= 65:
        sensor_class = WarningSensor
    else:
        sensor_class = NormalSensor

    return sensor_class(data["sensor_id"], data["location"],
                        temperature, data["operator_id"])


def load_json(filename):
    with (DATA_DIR / filename).open("r", encoding="utf-8") as file:
        return json.load(file)


def process_employees():
    data = load_json("employee.json")
    employees = [create_employee(item) for item in data["employees"]]

    print("\n" + "=" * 90)
    print("HASIL PENGOLAHAN DATA KARYAWAN")
    print("=" * 90)
    for employee in employees:
        result = employee.show_data()
        print(f'{result["ID"]} | {result["Nama"]} | {result["Status"]} | '
              f'Gaji Pokok: Rp{result["Gaji Pokok"]:,.0f} | '
              f'Bonus: Rp{result["Bonus"]:,.0f} | '
              f'Total: Rp{result["Total Gaji"]:,.0f}')

    total_gaji = sum(employee.calculate_salary() for employee in employees)
    print("-" * 90)
    print(f"Jumlah karyawan: {len(employees)}")
    print(f"Total penggajian: Rp{total_gaji:,.0f}")

    with (DATA_DIR / "employee_results.json").open("w", encoding="utf-8") as file:
        json.dump([employee.show_data() for employee in employees],
                  file, indent=4, ensure_ascii=False)


def process_sensors():
    data = load_json("sensor_logs.json")
    sensors = [create_sensor(item) for item in data["readings"]]

    print("\n" + "=" * 90)
    print("HASIL PEMANTAUAN SENSOR")
    print("=" * 90)
    for sensor in sensors:
        result = sensor.show_data()
        print(f'{result["ID Sensor"]} | {result["Lokasi"]} | '
              f'Suhu: {result["Suhu"]:.1f} C | {result["Status"]} | '
              f'Operator: {result["Operator"]} | {result["Tindakan"]}')

    danger = sum(sensor.get_status() == "DANGER" for sensor in sensors)
    warning = sum(sensor.get_status() == "WARNING" for sensor in sensors)
    normal = sum(sensor.get_status() == "NORMAL" for sensor in sensors)

    print("-" * 90)
    print(f"Jumlah sensor: {len(sensors)}")
    print(f"DANGER: {danger} | WARNING: {warning} | NORMAL: {normal}")

    with (DATA_DIR / "sensor_results.json").open("w", encoding="utf-8") as file:
        json.dump([sensor.show_data() for sensor in sensors],
                  file, indent=4, ensure_ascii=False)


def main():
    try:
        process_employees()
        process_sensors()
        print("\nProgram berhasil dijalankan.")
        print("Hasil tersimpan di folder data.")
    except FileNotFoundError as error:
        print(f"File tidak ditemukan: {error}")
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"Terjadi kesalahan pada data: {error}")


if __name__ == "__main__":
    main()
