import os
import trml2pdf
from weasyprint import HTML
from pdf.renderer import TRMLRenderer
from pdf.exceptions import PDFGenerationError


class PDFGenerator:
    def __init__(self, templates_dir: str):
        self.renderer = TRMLRenderer(templates_dir)

    def generate(
        self,
        *,
        template_name: str,
        output_filename: str,
        context: dict,
    ) -> str:
        """
        this method generates a PDF file based on a template


        :param template_name: file name of the template to be used
        :param output_filename: name of the output file
        :param context: a dictionary of variables to pass to the template
        :return: the generated PDF filename
        """
        try:
            rendered = self.renderer.render(template_name, context)


            if template_name.endswith(".trml"):
                pdf_data = trml2pdf.parseString(rendered)
                if not pdf_data:
                    raise PDFGenerationError("Generated PDF is empty")

                with open(output_filename, "wb") as f:
                    f.write(pdf_data)

            elif template_name.endswith(".html"):
                HTML(string=rendered).write_pdf(output_filename)

            else:
                raise PDFGenerationError("Unsupported template type")

            return output_filename

        except Exception as e:
            raise PDFGenerationError(str(e)) from e
