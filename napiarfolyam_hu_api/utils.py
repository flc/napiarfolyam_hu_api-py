def convert_date(date):
    return "".join(date.isoformat().split("-"))


def parse_item_element(element):
    nodes = element.childNodes
    data = {}
    for node in nodes:
        if node.nodeType == node.TEXT_NODE:
            continue
        data[node.tagName] = node.childNodes[0].data
    return data
