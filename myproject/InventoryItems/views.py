from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import IntegrityError, models
from django.http import Http404
from .models import InventoryItems
from .serializers import InventoryItemsSerializer

class InventoryItemsViewSet(viewsets.ModelViewSet):
    queryset = InventoryItems.objects.all()
    serializer_class = InventoryItemsSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new inventory item entry"""
        try:
            data = request.data.copy()
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                inventory_item = serializer.save()
                return Response({
                    'success': True,
                    'message': 'New inventory item entry created',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'success': False,
                    'message': 'Validation failed',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error creating inventory item: {str(e)}")
            return Response({
                'success': False,
                'message': f'An error occurred while creating inventory item: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def perform_create(self, serializer):
        """
        Perform the creation of the inventory item
        """
        serializer.save()
    
    def update(self, request, pk=None):
        """Update an inventory item"""
        try:
            inventory_item = InventoryItems.objects.get(pk=pk)
            serializer = self.get_serializer(inventory_item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except InventoryItems.DoesNotExist:
            return Response({'error': 'Inventory item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, pk=None):
        """Delete an inventory item"""
        try:
            inventory_item = InventoryItems.objects.get(pk=pk)
            inventory_item.delete()
            return Response({'message': 'Inventory item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except InventoryItems.DoesNotExist:
            return Response({'error': 'Inventory item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search inventory items"""
        try:
            query = request.GET.get('q', '')
            date_filter = request.GET.get('date_filter', '')
            
            queryset = self.get_queryset()
            
            if query:
                queryset = queryset.filter(
                    models.Q(item_name__icontains=query) |
                    models.Q(unit_of_measure__icontains=query)
                )
            
            if date_filter:
                queryset = queryset.filter(date=date_filter)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class InventoryItemsListViewSet(viewsets.ModelViewSet):
    """
    Separate ViewSet specifically for inventory items list operations
    This provides a different endpoint for inventory list functionality
    """
    queryset = InventoryItems.objects.all()
    serializer_class = InventoryItemsSerializer

    def calculate_running_totals(self, transactions):
        """
        Calculate running totals for a list of transactions.
        Returns list of tuples (transaction, running_total)
        """
        result = []
        
        # Convert QuerySet to list to avoid multiple database hits
        transactions = list(transactions)
        print(f"\nCalculating running totals for {len(transactions)} transactions")
        
        # Calculate cumulative total for each transaction
        running_total = 0
        for transaction in transactions:
            quantity = getattr(transaction, 'quantity', 0)
            if quantity is None:
                quantity = 0
            running_total += quantity
            result.append((transaction, running_total))
            print(f"Transaction {transaction.id}: {transaction.item_name}, Quantity: {quantity}, Running Total: {running_total}")
        
        print(f"Final running total: {running_total}\n")
        return result
    
    def list(self, request):
        """Get all inventory items with formatted data for frontend"""
        try:
            print("Starting list view processing...")
            
            # Get all inventory items ordered by date with related Item data
            inventory_items = InventoryItems.objects.select_related('itemID').all().order_by('-date')
            
            print(f"Total inventory items found: {inventory_items.count()}")
            
            if not inventory_items.exists():
                print("No inventory items found in database")
                return Response([], status=status.HTTP_200_OK)
            
            # Get all unique item names
            unique_items = inventory_items.values('item_name').distinct()
            print(f"Found unique items: {[item['item_name'] for item in unique_items]}")
            
            # Initialize data structures
            inventory_data = []
            grand_total_quantity = 0
            grand_total_onhand = 0
            
            # Process each unique item
            for unique_item in unique_items:
                item_name = unique_item['item_name']
                try:
                    # Get all transactions for this item in chronological order with related data
                    item_transactions = InventoryItems.objects.select_related('itemID').filter(
                        item_name=item_name
                    ).order_by('-date')
                    
                    print(f"Processing item: {item_name}, found {item_transactions.count()} transactions")
                    
                    # Get the first transaction for category and unit info
                    first_transaction = item_transactions.first()
                    if not first_transaction:
                        print(f"No transactions found for item: {item_name}")
                        continue
                        
                    print(f"First transaction details - ID: {first_transaction.id}, Date: {first_transaction.date}, Quantity: {first_transaction.quantity}")
                except Exception as e:
                    print(f"Error processing item {item_name}: {str(e)}")
                    continue
                
                # Get item details safely
                category = ''
                unit_of_measure = ''
                
                if first_transaction.itemID:
                    print(f"Related Item found for {item_name}: ID={first_transaction.itemID.itemID}")
                    category = getattr(first_transaction.itemID, 'category', '')
                    unit_of_measure = getattr(first_transaction.itemID, 'unitOfMeasure', '')
                    print(f"Category: {category}, Unit of Measure: {unit_of_measure}")
                
                item_total_quantity = 0
                
                # Calculate running totals
                transactions_with_totals = self.calculate_running_totals(item_transactions)
                
                # Add all transactions for this item
                first_transaction = True
                item_total_quantity = 0
                final_onhand = 0
                
                for transaction, running_total in transactions_with_totals:
                    # Add transaction with running total as on-hand
                    item_dict = {
                        'id': str(transaction.id),  # Convert to string to ensure serializable
                        'date': transaction.date.strftime('%Y-%m-%d') if transaction.date else '',
                        'item_name': str(transaction.item_name),
                        'category': str(category),
                        'unit_of_measure': str(unit_of_measure),
                        'quantity': float(transaction.quantity) if transaction.quantity else 0,  # Convert to float for consistency
                        'onhand': float(running_total),  # Convert to float for consistency
                        'isTransaction': True
                    }
                    print(f"Processing transaction - ID: {item_dict['id']}, Item: {item_dict['item_name']}, Quantity: {item_dict['quantity']}, Onhand: {item_dict['onhand']}")
                    
                    if first_transaction:
                        final_onhand = running_total
                        first_transaction = False
                    
                    inventory_data.append(item_dict)
                    item_total_quantity += transaction.quantity
                
                # Add subtotal for this item
                subtotal = {
                    'id': f'subtotal_{item_name}',
                    'date': 'Subtotal',
                    'item_name': str(item_name),
                    'category': str(category),
                    'unit_of_measure': str(unit_of_measure),
                    'quantity': float(item_total_quantity),
                    'onhand': float(final_onhand),
                    'isSubtotal': True
                }
                inventory_data.append(subtotal)
                print(f"Added subtotal - Item: {item_name}, Total Quantity: {item_total_quantity}, Final Onhand: {final_onhand}")
                
                grand_total_quantity += item_total_quantity
                grand_total_onhand += final_onhand
                
                print(f"Item {item_name}: Total Quantity: {item_total_quantity}, Final Onhand: {final_onhand}")
            
            # Add grand total at the end
            grand_total = {
                'id': 'grand_total',
                'date': 'GRAND TOTAL',
                'item_name': 'TOTAL',
                'category': '',
                'unit_of_measure': '',
                'quantity': float(grand_total_quantity),
                'onhand': float(grand_total_onhand),
                'isGrandTotal': True
            }
            inventory_data.append(grand_total)
            print(f"\nAdded grand total - Total Quantity: {grand_total_quantity}, Total Onhand: {grand_total_onhand}")
            
            # Log the final data structure
            print("Final inventory data structure:")
            for item in inventory_data:
                print(f"Item: {item['item_name']}, Quantity: {item['quantity']}, Onhand: {item['onhand']}, Type: {'Transaction' if item.get('isTransaction') else 'Subtotal' if item.get('isSubtotal') else 'Grand Total'}")
            
            return Response(inventory_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            import traceback
            print("Exception occurred in list view:", traceback.format_exc())
            return Response(
                {'error': f'Failed to fetch inventory data: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def retrieve(self, request, pk=None):
        """Get a specific inventory item by ID"""
        try:
            item = InventoryItems.objects.get(pk=pk)
            item_dict = {
                'id': item.id,
                'date': item.date,
                'item_name': item.item_name,
                'unit_of_measure': item.unit_of_measure,
            }
            return Response(item_dict, status=status.HTTP_200_OK)
        except InventoryItems.DoesNotExist:
            raise Http404("Inventory item not found")
        except Exception as e:
            return Response(
                {'error': f'Failed to fetch inventory item: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def update(self, request, pk=None):
        """Update an inventory item"""
        try:
            item = InventoryItems.objects.get(pk=pk)
            serializer = self.get_serializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except InventoryItems.DoesNotExist:
            return Response({'error': 'Inventory item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, pk=None):
        """Delete an inventory item"""
        try:
            item = InventoryItems.objects.get(pk=pk)
            item.delete()
            return Response({'message': 'Inventory item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except InventoryItems.DoesNotExist:
            return Response({'error': 'Inventory item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
