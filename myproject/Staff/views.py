# Staff/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import IntegrityError, models
from django.http import Http404
from .models import Staff
from .serializers import StaffSerializer

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    lookup_field = 'phone'  # Use phone as lookup field since it's the primary key
    
    def create(self, request, *args, **kwargs):
        """Create a new staff member"""
        try:
            # Use the data as-is since frontend already maps city to region
            data = request.data.copy()
            print(f"Received staff data: {data}")  # Debug logging
            
            serializer = self.get_serializer(data=data)
            
            if serializer.is_valid():
                staff_member = serializer.save()
                return Response({
                    'success': True,
                    'message': 'Staff member created successfully',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'success': False,
                    'message': 'Validation failed',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except IntegrityError as e:
            if 'email' in str(e).lower():
                return Response({
                    'success': False,
                    'message': 'Email address already exists',
                    'errors': {'email': ['This email is already registered']}
                }, status=status.HTTP_400_BAD_REQUEST)
            elif 'phone' in str(e).lower():
                return Response({
                    'success': False,
                    'message': 'Phone number already exists',
                    'errors': {'phone': ['This phone number is already registered']}
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error creating staff member: {str(e)}")  # Debug logging
            return Response({
                'success': False,
                'message': f'An error occurred while creating staff member: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request, pk=None):
        """Update a staff member"""
        try:
            staff = Staff.objects.get(phone=pk)
            serializer = self.get_serializer(staff, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Staff.DoesNotExist:
            return Response({'error': 'Staff member not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, pk=None):
        """Delete a staff member"""
        try:
            staff = Staff.objects.get(phone=pk)
            staff.delete()
            return Response({'message': 'Staff member deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Staff.DoesNotExist:
            return Response({'error': 'Staff member not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search staff members"""
        try:
            query = request.GET.get('q', '')
            salary_filter = request.GET.get('salary_filter', '')
            salary_amount = request.GET.get('salary_amount', '')
            
            queryset = self.get_queryset()
            
            if query:
                queryset = queryset.filter(
                    models.Q(firstName__icontains=query) |
                    models.Q(lastName__icontains=query) |
                    models.Q(position__icontains=query) |
                    models.Q(email__icontains=query) |
                    models.Q(phone__icontains=query) |
                    models.Q(address__icontains=query) |
                    models.Q(region__icontains=query)
                )
            
            if salary_filter and salary_amount:
                try:
                    amount = float(salary_amount)
                    if salary_filter == 'gt':
                        queryset = queryset.filter(salary__gt=amount)
                    elif salary_filter == 'lt':
                        queryset = queryset.filter(salary__lt=amount)
                    elif salary_filter == 'gte':
                        queryset = queryset.filter(salary__gte=amount)
                    elif salary_filter == 'lte':
                        queryset = queryset.filter(salary__lte=amount)
                except ValueError:
                    pass
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StaffListViewSet(viewsets.ModelViewSet):
    """
    Separate ViewSet specifically for staff list operations
    This provides a different endpoint for staff list functionality
    """
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    lookup_field = 'phone'
    
    def list(self, request):
        """Get all staff members with formatted data for frontend"""
        try:
            staff_queryset = Staff.objects.all()
            
            # Custom formatting for frontend
            staff_data = []
            for staff in staff_queryset:
                staff_dict = {
                    'id': staff.phone,  # Using phone as ID since it's the primary key
                    'name': f"{staff.firstName} {staff.lastName}",  # Combine first and last name
                    'position': staff.position,
                    'email': staff.email,
                    'phone': staff.phone,
                    'address': staff.address,
                    'city': staff.region,  # Mapping region to city for frontend
                    'salary': float(staff.salary),  # Convert Decimal to float for JSON
                }
                staff_data.append(staff_dict)
            
            return Response(staff_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': f'Failed to fetch staff data: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def retrieve(self, request, pk=None):
        """Get a specific staff member by phone"""
        try:
            staff = Staff.objects.get(phone=pk)
            staff_dict = {
                'id': staff.phone,
                'name': f"{staff.firstName} {staff.lastName}",
                'position': staff.position,
                'email': staff.email,
                'phone': staff.phone,
                'address': staff.address,
                'city': staff.region,
                'salary': float(staff.salary),
            }
            return Response(staff_dict, status=status.HTTP_200_OK)
        except Staff.DoesNotExist:
            raise Http404("Staff not found")
        except Exception as e:
            return Response(
                {'error': f'Failed to fetch staff: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def update(self, request, pk=None):
        """Update a staff member"""
        try:
            staff = Staff.objects.get(phone=pk)
            serializer = self.get_serializer(staff, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Staff.DoesNotExist:
            return Response({'error': 'Staff member not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, pk=None):
        """Delete a staff member"""
        try:
            staff = Staff.objects.get(phone=pk)
            staff.delete()
            return Response({'message': 'Staff member deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Staff.DoesNotExist:
            return Response({'error': 'Staff member not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)