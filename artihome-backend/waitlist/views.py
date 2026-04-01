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
    pledged = request.data.get('pledged_price')
    
    entry, created = WaitlistEntry.objects.get_or_create(
        user=request.user, product=product,
        defaults={'pledged_price': pledged}
    )
    
    if created:
        product.waitlist_count = F('waitlist_count') + 1
        product.save(update_fields=['waitlist_count'])
        return Response({'status': 'joined', 'waitlist_count': product.waitlist_count + 1}, status=201)
    
    if pledged and entry.pledged_price != pledged:
        entry.pledged_price = pledged
        entry.save()
    return Response({'status': 'already_joined'}, status=200)

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
