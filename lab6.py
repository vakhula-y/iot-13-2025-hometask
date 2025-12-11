import yaml
import os


class FileNotFound(Exception):
    pass


class FileCorrupted(Exception):
    pass


class InvalidAge(Exception):
    pass

class AgeValidator:
    @staticmethod
    def validate(age):
        if age < 0:
            raise InvalidAge("Вік не може бути від’ємним!")

class YamlManager:

    def __init__(self, filename):
        self.filename = filename

        if not os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as f:
                yaml.dump({}, f)    

            raise FileNotFound(f"Файл '{filename}' не існував. Створений тільки що")

    def read(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except yaml.YAMLError:
            raise FileCorrupted("Файл пошкоджений або містить неправильний yaml")

    def write(self, data: dict):
        if "age" in data:
            AgeValidator.validate(data["age"])

        with open(self.filename, "w", encoding="utf-8") as f:
            yaml.dump(data, f)

    def append(self, key, value):
        if key == "age":
            AgeValidator.validate(value)

        data = self.read()
        if not isinstance(data, dict):
            data = {}

        data[key] = value

        with open(self.filename, "w", encoding="utf-8") as f:
            yaml.dump(data, f)


def main():

    try:
        mgr = YamlManager("data.yaml")
    except FileNotFound as e:
        print(e)
        mgr = YamlManager("data.yaml")

    print("Файл створюється тут:", os.path.abspath("data.yaml"))

    print("\nПочаткові дані:", mgr.read())

    print("\nЗаписуємо основні дані")
    mgr.write({"name": "Alice", "age": 20})
    print("Y файлі:", mgr.read())

    print("Додаємо місто")
    mgr.append("city", "Kyiv")
    print("Y файлі:", mgr.read())

    try:
        mgr.append("age", -5)
    except InvalidAge:
        pass


if __name__ == "__main__":
    main()
