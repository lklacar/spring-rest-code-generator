import glob
import os
from jinja2 import Template


class Generator(object):
    def __init__(self, base_package, model_package_path, dao_package_path, service_package_path, templates_path):
        self.model_package_path = model_package_path
        self.dao_package_path = dao_package_path
        self.service_package_path = service_package_path
        self.templates_path = templates_path

        print self.generate_dao_interface("Employee")

    def get_model_names(self):
        models = []
        for model_path in self.get_model_paths():
            models.append(model_path.split(os.path.sep)[-1].split(".")[0])
        return models

    def get_model_paths(self):
        print os.path.join(self.model_package_path, "*.java")
        return glob.glob(os.path.join(self.model_package_path, "*.java"))

    def generate_dao_interface(self, model_name):
        t = Template(open(os.path.join(self.templates_path, "DaoTemplate.jinja2"), "r").read())
        return t.render({"model_name": model_name})


if __name__ == "__main__":
    base_package = os.path.join("..", "code", "recenzija")
    model_package_path = os.path.join(base_package, "model")
    dao_package_path = os.path.join(base_package, "dao")
    service_package_path = os.path.join(base_package, "service")
    templates_path = os.path.join("..", "templates")

    generator = Generator(base_package, model_package_path, dao_package_path, service_package_path, templates_path)

    print generator.get_model_names()
