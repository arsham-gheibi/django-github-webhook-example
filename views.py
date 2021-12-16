from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import hmac
import hashlib


@csrf_exempt
def deploy_webhook(request):
    if request.method == 'POST':

        WEBHOOK_SECRET = 'supersecretkey'

        # Verify the request is from GitHub

        if "X-Hub-Signature-256" not in request.headers:
            return JsonResponse({'error': 'Invalid Request'}, status=400)

        digest_name, signature = \
            request.META["HTTP_X_HUB_SIGNATURE_256"].split("=")

        if digest_name != "sha256":
            return JsonResponse(
                {'error':
                    f"Unsupported X-HUB-SIGNATURE digest mode found: \
                        {digest_name}"}, status=400)

        mac = hmac.new(
            WEBHOOK_SECRET.encode("utf-8"),
            msg=request.body,
            digestmod=hashlib.sha256)

        if not hmac.compare_digest(mac.hexdigest(), signature):
            return JsonResponse(
                {'error': 'Invalid X-HUB-SIGNATURE header found'},
                status=400)

        # Do somthing
        # example :

        """
        subprocess.call(
            'cd /examplerepo && \
                git fetch --all && \
                    git checkout --force "origin/main"')
        """

        return JsonResponse({}, status=202)
