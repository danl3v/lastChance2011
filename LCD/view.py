import os
# finish this later.
def renderTemplate(self, template_file, template_values):

    template_values = dict(getNavData(self), **template_values)

    path = os.path.join(os.path.dirname(__file__), 'templates/header.html')
    self.response.out.write(template.render(path, template_values))
    
    path = os.path.join(os.path.dirname(__file__), 'templates/' + template_file)
    self.response.out.write(template.render(path, template_values))
    
    path = os.path.join(os.path.dirname(__file__), 'templates/footer.html')
    self.response.out.write(template.render(path, template_values))

