from django.shortcuts import render, redirect
from .forms import UrlForm
from .models import UrlPair
from .baseconvert import baseconvert, BASE10, BASE62


class ShortenResultMessage:
    OK = "A new URL has been generated!"
    INVALID_PARAMS = "Parameters for shortening are invalid. Try again!"

# generate URL identifier by calculating Base62 on the database ID
def get_url_identifier(database_id):
    return baseconvert(database_id, BASE10, BASE62)


def create_report_message(short_url, long_url):
    short_url_len = len(short_url)
    long_url_len = len(long_url)
    message = "Long URL has " + str(long_url_len) + " characters and Short URL has " \
              + str(short_url_len) + " characters."
    # show warning if generated URL is longer than the original one
    if short_url_len > long_url_len:
        message += " NOTE: Generated URL is longer than the original one!"

    return message


def obtain_url_pair(long_url):
    url_list = list(UrlPair.objects.filter(long_url=long_url))
    if len(url_list) > 0:
        return url_list[0]
    else:
        return generate_url_pair(long_url)


def generate_url_pair(long_url):
    # Create and save a new UrlPair.
    # saving is necessary in order to get the ID of the Model instance
    new_url_pair = UrlPair.create("", long_url)
    new_url_pair.save()
    new_url_pair.short_url = get_url_identifier(new_url_pair.id)
    # Save short URL identifier. Saving the short URL identifier
    # is not strictly necessary but avoids having to convert a short URL
    # identifier to its corresponding Model ID in every redirection request.
    new_url_pair.save(update_fields=['short_url'])
    return new_url_pair


def index(request):
    form= UrlForm()
    return render(request, 'short_urls/index.html', {'form': form})


def shorten(request):
    form= UrlForm()
    if request.method == 'GET':
        form = UrlForm(request.GET)
        if form.is_valid():
            long_url = form.cleaned_data['long_url']
            url_pair = obtain_url_pair(long_url)
            short_url = 'http://' + request.get_host() + '/' + url_pair.short_url
            report_message = create_report_message(short_url, long_url)
            return render(request, 'short_urls/shorten_result_ok.html', {
                'form': UrlForm(),
                'message': ShortenResultMessage.OK,
                'report': report_message,
                'long_url': long_url,
            	'short_url': short_url
            })
        else:
            return render(request, 'short_urls/shorten_result_error.html', {
                'form': UrlForm(),
                'message': ShortenResultMessage.INVALID_PARAMS
            })

    return redirect('index')


def redirect_to_long(request):
    # Search any entry having the short url requested in 'request'.
    # Remove slash character ('/') from the beginning of 'request' 
    # string before comparing
    url_list = list(UrlPair.objects.filter(short_url=request.path[1:]))
    if len(url_list) > 0:   # there should be only one match
        # Redirect to the original URL with 301 Moved Permanently 
        return redirect(url_list[0].long_url, permanent=True)
    else:
        # No match
        return render(request, 'short_urls/index.html', {'form': UrlForm()})