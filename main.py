#!/usr/bin/env python
import os
import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")


class ResultHandler(BaseHandler):
    def post(self):
        dna_sequence = self.request.get("dna")

        hair = {
            'black': 'CCAGCAATCGC',
            'brown': 'GCCAGTGCCG',
            'blonde': 'TTAGCTATCGC'
        }

        face = {
            'square': 'GCCACGG',
            'round': 'ACCACAA',
            'oval': 'AGGCCTCA'
        }

        eyes = {
            'blue': 'TTGTGGTGGC',
            'green': 'GGGAGGTGGC',
            'brown': 'AAGTAGTGAC'
        }

        gender = {
            'female': 'TGAAGGACCTTC',
            'male': 'TGCAGGAACTTC'
        }

        race = {
            'white': 'AAAACCTCA',
            'black': 'CGACTACAG',
            'asian': 'CGCGGGCCG'
        }

        hair_color = ""
        eye_color = ""
        face_shape = ""
        gender_type = ""
        race_type = ""

        for key, value in hair.iteritems():
            if value in dna_sequence:
                hair_color = key

        for key, value in eyes.iteritems():
            if value in dna_sequence:
                eye_color = key

        for key, value in race.iteritems():
            if value in dna_sequence:
                race_type = key

        for key, value in gender.iteritems():
            if value in dna_sequence:
                gender_type = key

        for key, value in face.iteritems():
            if value in dna_sequence:
                face_shape = key

        params = {"hair_color": hair_color, "eye_color": eye_color, "face_shape": face_shape, "gender": gender_type, "race": race_type}

        return self.render_template("result.html", params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/result', ResultHandler),
], debug=True)

