from ariadne import ObjectType

section_item_type = ObjectType("SectionItem")


@section_item_type.field("id")
def resolve_id(sectionitem, info):
    return sectionitem.item_id


@section_item_type.field("name")
def resolve_name(sectionitem, info):
    return sectionitem.item.name


@section_item_type.field("description")
def resolve_description(sectionitem, info):
    return sectionitem.item.description


@section_item_type.field("photo")
def resolve_photo(sectionitem, info):
    return sectionitem.item.photo


@section_item_type.field("displayOrder")
def resolve_display_order(sectionitem, info):
    return sectionitem.display_order
