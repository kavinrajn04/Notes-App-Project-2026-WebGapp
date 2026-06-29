import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Note


def landing_page(request):
    return render(request, "notes-app.html")


@csrf_exempt
def notes_list(request):
    if request.method == "GET":
        notes = Note.objects.all()
        data = [
            {
                "id": note.id,
                "title": note.title,
                "content": note.content,
                "created_at": note.created_at,
            }
            for note in notes
        ]
        return JsonResponse(data, safe=False)

    if request.method == "POST":
        body = json.loads(request.body)
        note = Note.objects.create(
            title=body.get("title", "Untitled"),
            content=body.get("content", ""),
        )
        return JsonResponse(
            {
                "id": note.id,
                "title": note.title,
                "content": note.content,
                "created_at": note.created_at,
            },
            status=201,
        )

    if request.method == "PUT":
        body = json.loads(request.body)
        note = Note.objects.get(id=body["id"])
        note.title = body.get("title", note.title)
        note.content = body.get("content", note.content)
        note.save()
        return JsonResponse(
            {
                "id": note.id,
                "title": note.title,
                "content": note.content,
                "created_at": note.created_at,
            }
        )
    if request.method == "DELETE":
        body = json.loads(request.body)
        Note.objects.filter(id=body["id"]).delete()
        return JsonResponse({"deleted": True})

    return JsonResponse({"error": "Method not allowed"}, status=405)
