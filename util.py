import wikipedia
import wikipedia.exceptions as exc
import youtube_dl


def search_wiki(message):
    try:
        message = wikipedia.summary(message, sentences=4,
                                    auto_suggest=True, redirect=True)
    except exc.DisambiguationError as e:
        list_options = e.options[:10]
        list_options = "\n".join(list_options)

        text = "Please be more specific.... Do you mean?:\n" + " " * 10 + "\n"

        message = text + list_options

    except exc.PageError:
        text = "Sorry, couldn't fetch any information on that"
        message = text

    except exc.RedirectError as e:
        text = "Can only fetch information on " + e.title
        text += "\n" + " " * 1000 + "\n"
        message = text + e.message

    return message


def find_photo(item):
    photo = ""

    try:
        photo_request = wikipedia.page(item)
        photo = photo_request.images
        photo = [img for img in photo if not img.endswith('.svg')]
        photo = [img for img in photo if not img.endswith('.ogg')][:10]
        response = "Here are the photos that you have requested: \n"

    except exc.PageError:
        response = "Sorry, couldn't fetch any information on that \n"

    except exc.DisambiguationError as e:
        list_options = e.options[:10]
        list_options = "\n".join(list_options)
        response = "Please be more specific, do you mean? \n" + list_options

    except exc.RedirectError as e:
        response = "Can only fetch information on " + e.title

    if photo:
        return photo, response

    else:
        return photo, response


def polite_address(author):
    title = ""
    name = ""
    author = str(author)
    female = {'aliham#2055': 'Alicia', 'maccat550#5522': 'MacKenzie',
              'meowslayer6485': 'Kathleen'}
    male = {'aquila#0990': 'Aquila', 'jules#4478': 'Jules'}

    if author in male:
        title = 'sir'
        name = male[author]

    if author in female:
        title = 'madame'
        name = female[author]

    return title, name


def ydl_source(title):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True',
                   'download': 'False'}

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(f'ytsearch:{title}',
                                download=False)['entries'][0]
        url2 = info['formats'][0]['url']
        song_title = info['title']
        duration = info['duration']

        return url2, song_title, duration
