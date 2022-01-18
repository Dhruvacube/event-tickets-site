import asyncio
from django.http import HttpResponsePermanentRedirect
from django.utils.decorators import sync_and_async_middleware


@sync_and_async_middleware
def redirect_middleware(get_response):
    if asyncio.iscoroutinefunction(get_response):

        async def middleware(request):
            response = await get_response(request)
            full_url = await request.build_absolute_uri()
            if await request.user.is_superuser:
                return response
            if "tgl2.herokuapp.com".lower() in full_url.lower():
                return HttpResponsePermanentRedirect(
                    full_url.replace("tgl2.herokuapp.com", "tanzanitelpu.com"))
            return response

    else:

        def middleware(request):
            response = get_response(request)
            full_url = request.build_absolute_uri()
            if request.user.is_superuser:
                return response
            if "tgl2.herokuapp.com".lower() in full_url.lower():
                return HttpResponsePermanentRedirect(
                    full_url.replace("tgl2.herokuapp.com", "tanzanitelpu.com"))
            return response

    return middleware
