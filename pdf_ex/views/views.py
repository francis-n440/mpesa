import logging

from django.shortcuts import render
from django.http import HttpResponse

from .services import extract_from_pdf, parse_mpesa_content, filter

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
			filter_str = request.POST.get('filter')
			if filter_str:
				content = filter(content, filter_str)
			response = HttpResponse()
			response['Content-Disposition'] = 'attachment; filename="extractfile.xlsx"'
			response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

			response.write(content.getvalue())
			return response


	return render(request, 'index.html', {'num_pages': num_pages, 'error': error})
