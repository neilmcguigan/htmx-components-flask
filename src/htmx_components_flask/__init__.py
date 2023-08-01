import werkzeug
from flask import Blueprint, request
from lxml import etree, html

htmx_components_flask = Blueprint(
    "htmx_components_flask", __name__, template_folder="templates"
)


@htmx_components_flask.app_context_processor
def jinja_globals():
    return dict(int=int)


@htmx_components_flask.app_template_filter("url_encode")
def url_encode(s: str) -> str:
    return werkzeug.urls.url_encode(s)


@htmx_components_flask.app_template_filter("partition")
def partition(value: str, missing: str, sep: str = ",") -> tuple[str, str]:
    a, _, b = str(value).partition(sep)
    return (a or missing, b or missing)


parser = etree.HTMLParser(encoding="utf-8")


@htmx_components_flask.after_app_request
def after_app_request(response):
    if "HX-Request" in request.headers:
        data = response.get_data()
        tree = html.fromstring(data, parser=parser)
        target = request.headers["HX-Target"]
        target_elem = tree.xpath(f"//*[@id='{target}']")[0]
        oob_elems = tree.xpath("//*[@hx-swap-oob]")
        elems = [target_elem] + oob_elems
        response.data = "".join([html.tostring(elem, encoding=str) for elem in elems])

    return response
