from __future__ import print_function
from mailmerge import MailMerge
from datetime import date

template = "implant_report.docx"

document = MailMerge(template)
print(document.get_merge_fields())