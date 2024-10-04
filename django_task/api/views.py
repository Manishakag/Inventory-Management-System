import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Item
from .serializers import ItemSerializer

# Create your views here.

# set up logger
logger = logging.getLogger(__name__)


class CreateItem(APIView):
    def post(self, request):
        try:
            serializer = ItemSerializer(data=request.data)
            item_name = request.data.get("name")
            if Item.objects.filter(name=item_name):
                logger.warning(
                    f"Attempt to create an item that already exists: {item_name}"
                )
                return Response(
                    "Item already exists", status=status.HTTP_400_BAD_REQUEST
                )
            else:
                if serializer.is_valid():
                    serializer.save()
                logger.info(f"Item created successfully: {item_name}")

                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(
                f"Error while creating item: {str(e)}",
            )
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReadItem(APIView):
    def get(self, _):
        try:
            items = Item.objects.all()
            serializer = ItemSerializer(items, many=True)
            logger.info("Items retrieved successfully")
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving items: {str(e)}")
            return Response(data="Item not found", status=status.HTTP_404_NOT_FOUND)


class UpdateItem(APIView):
    def put(self, request, pk):
        try:
            item = Item.objects.get(pk=pk)
            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Item updated successfully: {item.name}")
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            logger.error(f"Item not found: {pk}")
            return Response(data="Item not found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating item {pk}: {str(e)}")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteItem(APIView):
    def delete(self, request, pk):
        try:
            item = Item.objects.get(pk=pk)
            item.delete()
            logger.info(f"Item deleted successfully: {item.name}")
            return Response(
                data={"message": "Item deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Item.DoesNotExist:
            logger.error(f"Item not found for deletion: {pk}")
            return Response(
                data={"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error deleting item {pk}: {str(e)}")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
