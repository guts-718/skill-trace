def format_report_text(report):
    lines = []
    lines.append(f"Daily Report - {report['date']}")
    lines.append("")
    lines.append(f"Total Time: {report['total_time_sec']//60} minutes")
    lines.append(f"Sessions: {report['session_count']}")
    lines.append("")
    lines.append("Category Breakdown:")

    for k, v in report["category_breakdown"].items():
        lines.append(f"- {k}: {v//60} min")

    lines.append("")
    lines.append("Top Domains:")
    for d in report["top_domains"]:
        lines.append(f"- {d['domain']}: {d['time']//60} min")

    return "\n".join(lines)
