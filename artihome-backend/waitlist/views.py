from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import WaitlistEntry
from products.models import Product
from .serializers import WaitlistEntrySerializer
from django.db.models import F

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_waitlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    entry, created = WaitlistEntry.objects.update_or_create(
        user=request.user,
        product=product,
        defaults={
            'name': request.data.get('name', ''),
            'phone': request.data.get('phone', ''),
            'city': request.data.get('city', ''),
            'requirements': request.data.get('requirements', ''),
            'is_pledge': bool(request.data.get('is_pledge', False)),
        }
    )

    if created:
        product.waitlist_count = F('waitlist_count') + 1
        product.save(update_fields=['waitlist_count'])

    product.refresh_from_db(fields=['waitlist_count'])
    return Response({
        'status': 'joined' if created else 'updated',
        'waitlist_count': product.waitlist_count,
        'entry': WaitlistEntrySerializer(entry).data,
    }, status=201 if created else 200)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def leave_waitlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    deleted, _ = WaitlistEntry.objects.filter(user=request.user, product=product).delete()
    if deleted:
        product.waitlist_count = F('waitlist_count') - 1
        product.save(update_fields=['waitlist_count'])
    return Response(status=204)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_waitlists(request):
    entries = WaitlistEntry.objects.filter(user=request.user).select_related('product')
    serializer = WaitlistEntrySerializer(entries, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_pledge(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    entry, created = WaitlistEntry.objects.get_or_create(user=request.user, product=product)
    if created:
        product.waitlist_count = F('waitlist_count') + 1
        product.save(update_fields=['waitlist_count'])
    entry.is_pledge = not entry.is_pledge
    entry.save(update_fields=['is_pledge'])

    product.refresh_from_db(fields=['waitlist_count'])
    pledge_count = WaitlistEntry.objects.filter(product=product, is_pledge=True).count()
    return Response({
        'pledged': entry.is_pledge,
        'pledge_count': pledge_count,
        'waitlist_count': product.waitlist_count,
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pledge_count(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    count = WaitlistEntry.objects.filter(product=product, is_pledge=True).count()
    return Response({'pledge_count': count})
