def make_export(document):
    return (
        f"Title: {document['title']}\n"
        f"Owner: {document['owner']}\n"
        f"Content: {document['content']}"
    )