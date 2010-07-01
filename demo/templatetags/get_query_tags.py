# encoding: utf-8
from django import template
from django.template import TemplateSyntaxError, VariableDoesNotExist
from django.http import QueryDict

from django_getquery.demo.get_query import GetQuery


register = template.Library()


class GurlNode(template.Node):
    def __init__(self, gq, mod):
        self.gq = template.Variable(gq)

        if mod:
            for x in mod.keys():
                list = mod.getlist(x)
                list = [template.Variable(zz) for zz in list]
                mod.setlist(x, list)

        self.mod = mod

    def render(self, context):
        def make_in_context(a):
            try:
                return a.resolve(context)
            except:
                return str(a)

        try:
            actual_gq = self.gq.resolve(context)
            if self.mod:
                for x in self.mod.keys():
                    list = self.mod.getlist(x)
                    list = map(make_in_context, list)
                    self.mod.setlist(x, list)

            return actual_gq.to_query_safe(self.mod)

        except template.VariableDoesNotExist:
            return ''


def gurl(parser, token):
    """
    Devuelve el path hacia la pagina actual segun el contenido del objeto GetQuery dado. Esta variable ha debido crearse
    previamente desde la vista, por ejemplo con:

        gq = GetQuery(request)

    Esto generara un objeto GetQuery que contendra todas las variables GET presentes en la request actual. Sin embargo 
    tambien es posible escoger que variables hay que incluir y cuales no con las siguientes sintaxis:

        * gq = GetQuery(request, only=['page'])         -> Tan solo captura el parametro GET 'page'.
        * gq = GetQuery(request, exclude=['sk', 'uue']) -> Captura todos excepto 'sk' y 'uue'

    La sintaxis propia de este tag es:

    {% gurl gq %} -> Genera un path con los contenido del objeto GetQuery dado, del estilo "?a=1&b=2"

    {% gurl gq "a:4,b:123" %} -> Se puede añadir un parametro que haga de 'modificador'. Se trata de un string que
    permite modificar los contenidos del objeto GetQuery para cambiar un valor o añadir nuevos. La sintaxis de este
    parametro es igual a la de los diccionarios estandard de python.

        - Por defecto, su comportamiento sera el de substituir el valor dado para una determinada clave existente en la URL, o de añadir el par clave valor si esta no existia previamente.
        - Sin embargo, es posible que existan varios valores para una misma clave en un conjunto de parametros GET. Si lo que deseamos es añadir obligatoriamente un determinado par clave-valor aunque ya exista, podemos usar la sintaxis especial '$'. 

    Ejemplo: Tenemos gq que incluye los valores "a=1, b=2"
        - Llamamos a {% gurl gq "a:24" %}  -> "a=24 & b=2"
        - Llamamos a {% gurl gq "$a:24" %}  -> "a=1 & a=24 & b=2"
        - Llamamos a {% gurl gq "a:24, c:3" %}  -> "a=24 & b=2 & c=3"

        Tambien es posible especificar un mismo parametro con y sin sintaxis de obligacion '$' a la vez.
        Por ejemplo:
        - Llamamos a {% gurl gq "a:55, $a:99" %} -> "a=55 & a=99 & b=2"
            Con esto conseguimos que el parametro original 'a' sea modificado con el nuevo valor que quieras
            darle, y además añadir otro parametro 'a' con otro valor fijo.

    Además, tambien es posible dar variables como parametros. Todos los valores dados se intentaran convertir
    a variables y ser resueltas en el contexto actual. Si se resuelve con éxito, se usara el valor de esa
    variable.

    Ejemplo: Tenemos gq con "a=1, b=2" y otra variable de contexto "foo = [11,22,33,44]" generada en la vista.
        - Llamamos a {% gurl gq "a:foo.1" %} -> "a=22 & b=2"
    """
    bits = token.split_contents()
    get_query = bits[1]

    if len(bits) > 2:
        mod = bits[2]

        if mod[0] == mod[-1] and mod[0] in ['"', "'"]:
            mod = mod[1:-1]

        if not GetQuery.validate_mod(mod):
        	raise TemplateSyntaxError("Error de sintaxi en el modificador. Sintaxis valida del tipo 'a:1,b:45,c:texto' ")

        a = QueryDict(mod.replace(':', '=').replace(',' , '&'), mutable=True)

    else:
        a = None


    return GurlNode(get_query, a)

gurl = register.tag(gurl)
