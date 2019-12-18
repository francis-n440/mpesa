import logging

from django.shortcuts import render
from django.http import HttpResponse

from .services import extract_from_pdf, parse_mpesa_content, exec_analytics

logger = logging.getLogger(__name__)


def upload(request):
	num_pages = 0
	error = ''
	if request.method == 'POST':
		try:
			num_pages, content = extract_from_pdf(
				request.FILES['file'], request.POST.get('password'))
		except Exception:
			error = 'Invalid password'
		else:
			content = parse_mpesa_content(content)
			if content:
				content2 = exec_analytics(content)

			response = HttpResponse()
			response['Content-Disposition'] = 'attachment; filename="summary.xlsx"'
			response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

			response.write(content2.getvalue())
			return response


	return render(request, 'index.html', {'num_pages': num_pages, 'error': error})
