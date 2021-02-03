from ariadne import ObjectType

from wdt.menu.models import Section

section_query = ObjectType("Query")
section_type = ObjectType("Section")


@section_query.field("section")
def resolve_section(obj, info, *, id):
    try:
        return Section.objects.get(pk=id)
    except Section.DoesNotExist:
        return None


@section_query.field("sections")
def resolve_sections(_, info):
    return Section.objects.order_by("name")


@section_type.field("items")
def resolve_section_items(section, info):
    return section.sectionitem_set.all().order_by("display_order")
