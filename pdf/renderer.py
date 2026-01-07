import os
from jinja2 import Environment, FileSystemLoader, select_autoescape


class TRMLRenderer:
    def __init__(self, templates_dir: str):
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(enabled_extensions=("trml", "xml","html"))
        )

    def render(self, template_name: str, context: dict) -> str:
        """
        this method gets context values and combines them with a template

        :param template_name: name of the template to be used
        :param context: dictionary of context values
        :return: string of the rendered template
        """
        template = self.env.get_template(template_name)
        return template.render(**context)
