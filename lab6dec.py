import yaml
import os
import logging
from functools import wraps

class FileNotFound(Exception):
    pass


class FileCorrupted(Exception):
    pass


def logged(exception, mode):
    """
    exception — the type of exception to be caught
    mode — either 'console' or 'file'
    """

  
    logger = logging.getLogger("yaml_manager_logger")
    logger.setLevel(logging.ERROR)

    if not logger.handlers:
      
        if mode == "console":
            handler = logging.StreamHandler()
        elif mode == "file":
            handler = logging.FileHandler("logs.txt", encoding="utf-8")
        else:
            raise ValueError("Mode must be 'console' or 'file'.")

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception as e:
                logger.error(f"Caught exception: {str(e)}")
                raise
        return wrapper

    return decorator


class YamlManager:

    @logged(FileNotFound, "console")
    def __init__(self, filename):
        self.filename = filename

    
        if not os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as f:
                yaml.dump({}, f)

            print(f"Файл '{filename}' не існував — створено автоматично.")

    @logged(FileCorrupted, "file")
    def read(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            return data
        except yaml.YAMLError:
            raise FileCorrupted("Файл пошкоджений або має некоректний YAML.")

    @logged(Exception, "console")
    def write(self, data: dict):
        with open(self.filename, "w", encoding="utf-8") as f:
            yaml.dump(data, f)

    @logged(Exception, "file")
    def append(self, key, value):
        data = self.read()
        if not isinstance(data, dict):
            data = {}

        data[key] = value

        with open(self.filename, "w", encoding="utf-8") as f:
            yaml.dump(data, f)


def main():
    print("=== Демонстрація роботи YAML-менеджера ===")

    mgr = YamlManager("data.yaml")

    print("Початковий вміст:", mgr.read())

    mgr.write({"name": "Alice", "age": 21})
    print("Після write:", mgr.read())

    mgr.append("city", "Kyiv")
    print("Після append:", mgr.read())


if __name__ == "__main__":
    main()

