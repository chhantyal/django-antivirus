This project intent to provide an application that uses python-clamav library to integrate with ClamAV antivirus, and provide a template filter that check a a file for virus and saves this information, returning if that file can or not be downloaded.

Depends on **pyClamAV** and **jQuery** libraries to work.

**How to use:**

**1.** First you need to add the application to your INSTALLED\_APPS setting;

**2.** Add the following node to your project urlpatterns:

```
(r'^antivirus/', include('apps.antivirus.urls')),
```

**3.** Considering you have an object called "document" that has a field "file" of FileField type, you shall follows this example:

```
{% load antivirus %}

{{ document|check_for_virus:"file" }}
```

This will show a message like "Wait for file checking..." and make an Ajax request, returning the download link or message that found a virus depending on result.

The file scanning is made just once time, that is stored in database and used for next times.