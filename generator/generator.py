import glob
import os
from dircache import listdir

from jinja2 import Template
from os.path import isfile, join


class Generator(object):
    def __init__(self, base_package, model_package_path, dao_package_path, service_package_path, templates_path):
        self.model_package_path = model_package_path
        self.dao_package_path = dao_package_path
        self.service_package_path = service_package_path
        self.templates_path = templates_path

    def get_model_names(self):
        models = []
        for model_path in self.get_model_paths():
            models.append(model_path.split(os.path.sep)[-1].split(".")[0])
        return models

    def get_model_paths(self):
        return glob.glob(os.path.join(self.model_package_path, "*.java"))

    def render_template(self, model_name, template_name):
        t = Template(open(os.path.join(self.templates_path, template_name), "r").read())
        return t.render({"model_name": model_name})

    def generate(self):
        templates = [f for f in listdir(self.templates_path) if isfile(join(self.templates_path, f))]
        for model_name in self.get_model_names():
            for template_name in templates:
                if "Dao" in template_name:
                    self.make_dir("../out/dao/%s/" % model_name.lower())
                    open("../out/dao/%s/%s%s.java" % (model_name.lower(), model_name, template_name.split(".")[-2]), "w").write(
                        self.render_template(model_name, template_name))
                elif "Service" in template_name:
                    self.make_dir("../out/service/%s/" % model_name.lower())
                    open("../out/service/%s/%s%s.java" % (model_name.lower(), model_name, template_name.split(".")[-2]), "w").write(
                        self.render_template(model_name, template_name))
                elif "Controller" in template_name:
                    self.make_dir("../out/controller/%s/" % model_name.lower())
                    open("../out/controller/%s/%s%s.java" % (model_name.lower(), model_name, template_name.split(".")[-2]), "w").write(
                        self.render_template(model_name, template_name))

    def make_dir(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)



if __name__ == "__main__":
    base_package = os.path.join("..", "code", "recenzija")
    model_package_path = os.path.join(base_package, "model")
    dao_package_path = os.path.join(base_package, "dao")
    service_package_path = os.path.join(base_package, "service")
    templates_path = os.path.join("..", "templates")

    generator = Generator(base_package, model_package_path, dao_package_path, service_package_path, templates_path)

    generator.generate()
