from html import escape
def label(text):
    return "<p>" + escape(text) + "</p>"
