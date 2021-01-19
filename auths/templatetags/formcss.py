from django import template
register = template.Library()

@register.filter(name='addplaceholder')
def addplaceholder(field, placeholder):
    print(field)
    return field.as_widget(attrs={"placeholder":placeholder,"class":"form-control"})



