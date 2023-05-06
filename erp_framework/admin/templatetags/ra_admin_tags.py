from __future__ import unicode_literals

from django import template
from django.template.loader import get_template, render_to_string
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe

from erp_framework.base import app_settings

register = template.Library()


@register.simple_tag(takes_context=True)
def render_navigation_menu(context):
    navigation_class = import_string(app_settings.RA_NAVIGATION_CLASS)
    request = context["request"]
    admin_site = context["admin_site"]
    return mark_safe(navigation_class.get_menu(context, request, admin_site))


@register.simple_tag(takes_context=True)
def render_reports_menu(context):
    request = context["request"]
    is_in_reports = False
    active_base_model = ""
    if request.path.startswith("/reports/"):
        is_in_reports = True
        active_base_model = [x for x in request.path.split("/") if x][1]

    from erp_framework.reporting.registry import report_registry

    base_models = report_registry.get_base_models_with_reports()
    if base_models:
        t = get_template(f"erp_framework/reports_menu.html")
        output = render_to_string(
            "erp_framework/reports_menu.html",
            {
                "base_models_reports_tuple": base_models,
                "is_report": context.get("is_report", False),
                "base_model": context.get("base_model", False),
                "report_slug": context.get("report_slug", False),
                "current_base_model_name": context.get(
                    "current_base_model_name", False
                ),
            },
            request,
        )
        return mark_safe(output)
    return ""


@register.simple_tag(takes_context=True)
def get_report(context, base_model, report_slug):
    from erp_framework.reporting.registry import report_registry

    return report_registry.get(namespace=base_model, report_slug=report_slug)