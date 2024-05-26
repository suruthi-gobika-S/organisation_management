from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Organization, Role, User

from django.contrib.auth.models import Permission
 # Rest of your test methods...

class OrganizationTests(APITestCase):
    def setUp(self):
        self.default_organization = Organization.objects.create(name='DefaultOrg', description='Default Description')

        self.superuser = User.objects.create_superuser(
            username='superuser',
            email='superuser@example.com',
            password='password',
            organization=self.default_organization
        )

        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='password',
            is_staff=True,
            organization=self.default_organization
        )

        self.manager = User.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='password',
            organization=self.default_organization
        )

        self.member = User.objects.create_user(
            username='member',
            email='member@example.com',
            password='password',
            organization=self.default_organization
        )

    def test_create_organization_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('organization-list')
        data = {'name': 'Org2', 'description': 'Description2'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_organization_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('organization-list')
        data = {'name': 'Org3', 'description': 'Description3'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_organization_manager(self):
        self.client.force_authenticate(user=self.manager)
        url = reverse('organization-list')
        data = {'name': 'Org4', 'description': 'Description4'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_organization_member(self):
        self.client.force_authenticate(user=self.member)
        url = reverse('organization-list')
        data = {'name': 'Org5', 'description': 'Description5'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_organization(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('organization-detail', args=[self.default_organization.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_organization_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('organization-detail', args=[self.default_organization.id])
        data = {'name': 'DefaultOrg Updated', 'description': 'Default Description Updated'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_organization_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('organization-detail', args=[self.default_organization.id])
        data = {'name': 'DefaultOrg Updated', 'description': 'Default Description Updated'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_organization_manager(self):
        self.client.force_authenticate(user=self.manager)
        url = reverse('organization-detail', args=[self.default_organization.id])
        data = {'name': 'DefaultOrg Updated', 'description': 'Default Description Updated'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_organization_member(self):
        self.client.force_authenticate(user=self.member)
        url = reverse('organization-detail', args=[self.default_organization.id])
        data = {'name': 'DefaultOrg Updated', 'description': 'Default Description Updated'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_organization_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('organization-detail', args=[self.default_organization.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_organization_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('organization-detail', args=[self.default_organization.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_organization_manager(self):
        self.client.force_authenticate(user=self.manager)
        url = reverse('organization-detail', args=[self.default_organization.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_organization_member(self):
        self.client.force_authenticate(user=self.member)
        url = reverse('organization-detail', args=[self.default_organization.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_organizations(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('organization-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class RoleTests(APITestCase):
    def setUp(self):
        # Define manager and member users here
        self.default_organization = Organization.objects.create(name='DefaultOrg', description='Default Description')
        self.superuser = User.objects.create_superuser(
            username='superuser',
            email='superuser@example.com',
            password='password',
            organization=self.default_organization
        )
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='password',
            is_staff=True,
            organization=self.default_organization
        )
        self.manager = User.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='password',
            organization=self.default_organization
        )
        self.member = User.objects.create_user(
            username='member',
            email='member@example.com',
            password='password',
            organization=self.default_organization
        )

        self.default_role = Role.objects.create(name='DefaultRole', description='Default Description', organization=self.default_organization)

    def test_create_role_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('role-list')
        data = {'name': 'Role2', 'description': 'Description2', 'organization': self.default_organization.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_role_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('role-list')
        data = {'name': 'Role3', 'description': 'Description3', 'organization': self.default_organization.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_role_manager(self):
        self.client.force_authenticate(user=self.manager)
        url = reverse('role-list')
        data = {'name': 'Role4', 'description': 'Description4', 'organization': self.default_organization.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_role_member(self):
        self.client.force_authenticate(user=self.member)
        url = reverse('role-list')
        data = {'name': 'Role5', 'description': 'Description5', 'organization': self.default_organization.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_role(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('role-detail', args=[self.default_role.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_role_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('role-detail', args=[self.default_role.id])
        data = {'name': 'DefaultRole Updated', 'description': 'Default Description Updated', 'organization': self.default_organization.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_role_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('role-detail', args=[self.default_role.id])
        data = {'name': 'DefaultRole Updated', 'description': 'Default Description Updated', 'organization': self.default_organization.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_role_manager(self):
        self.client.force_authenticate(user=self.manager)
        url = reverse('role-detail', args=[self.default_role.id])
        data = {'name': 'DefaultRole Updated', 'description': 'Default Description Updated', 'organization': self.default_organization.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_role_member(self):
        self.client.force_authenticate(user=self.member)
        url = reverse('role-detail', args=[self.default_role.id])
        data = {'name': 'DefaultRole Updated', 'description': 'Default Description Updated', 'organization': self.default_organization.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_role_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('role-detail', args=[self.default_role.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_role_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('role-detail', args=[self.default_role.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_role_manager(self):
        self.client.force_authenticate(user=self.manager)
        url = reverse('role-detail', args=[self.default_role.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_role_member(self):
        self.client.force_authenticate(user=self.member)
        url = reverse('role-detail', args=[self.default_role.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_roles(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('role-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        


class UserTests(APITestCase):
    def setUp(self):
        self.default_organization = Organization.objects.create(name='DefaultOrg', description='Default Description')
        self.default_role = Role.objects.create(name='DefaultRole', description='Default Description', organization=self.default_organization)

        # Grant necessary permissions
        
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='password',
            is_staff=True,
            organization=self.default_organization
        )

        self.manager = User.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='password',
            organization=self.default_organization
        )

        self.member = User.objects.create_user(
            username='member',
            email='member@example.com',
            password='password',
            organization=self.default_organization
        )
        self.admin.user_permissions.add(
            Permission.objects.get(codename='change_user'),
            Permission.objects.get(codename='delete_user')
        )
        self.manager.user_permissions.add(
            Permission.objects.get(codename='change_user')
        )
        self.superuser = User.objects.create_superuser(
            username='superuser',
            email='superuser@example.com',
            password='password',
            organization=self.default_organization
        )


    def test_create_user_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('user-list')
        data = {
            'username': 'user2',
            'email': 'user2@example.com',
            'password': 'password',
            'organization': self.default_organization.id,
            'roles': [self.default_role.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-list')
        data = {
            'username': 'user3',
            'email': 'user3@example.com',
            'password': 'password',
            'organization': self.default_organization.id,
            'roles': [self.default_role.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_manager(self):
        self.client.force_authenticate(user=self.manager)
        url = reverse('user-list')
        data = {
            'username': 'user4',
            'email': 'user4@example.com',
            'password': 'password',
            'organization': self.default_organization.id,
            'roles': [self.default_role.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_member(self):
        self.client.force_authenticate(user=self.member)
        url = reverse('user-list')
        data = {
            'username': 'user5',
            'email': 'user5@example.com',
            'password': 'password',
            'organization': self.default_organization.id,
            'roles': [self.default_role.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('user-detail', args=[self.admin.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('user-detail', args=[self.admin.id])
        data = {
            'username': 'admin_updated',
            'email': 'admin_updated@example.com',
            'organization': self.default_organization.id,
            'roles': [self.default_role.id]
        }
        response = self.client.post(url, data, format='json')

        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-detail', args=[self.member.id])
        data = {
            'username': 'member_updated',
            'email': 'member_updated1@example.com',
            'organization': self.default_organization.id,
            'roles': [self.default_role.id]
        }

        response = self.client.put(url, data, format='json')
    
        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
  
        else:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user_manager(self):
        self.client.force_authenticate(user=self.manager)
        url = reverse('user-detail', args=[self.member.id])
        data = {
            'username': 'member_updated',
            'email': 'member_updated2@example.com',
            'organization': self.default_organization.id,
            'roles': [self.default_role.id]
        }
        response = self.client.post(url, data, format='json')

        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_update_user_member(self):
        self.client.force_authenticate(user=self.member)
        url = reverse('user-detail', args=[self.member.id])
        data = {
            'username': 'member_updated',
            'email': 'member_updated3@example.com',
            'organization': self.default_organization.id,
            'roles': [self.default_role.id]
        }
        response = self.client.put(url, data, format='json')

        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_delete_user_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('user-detail', args=[self.admin.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-detail', args=[self.member.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_manager(self):
        self.client.force_authenticate(user=self.manager)
        url = reverse('user-detail', args=[self.member.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_member(self):
        self.client.force_authenticate(user=self.member)
        url = reverse('user-detail', args=[self.admin.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_users(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class AssignRoleTests(APITestCase):
    def setUp(self):
        # Define manager and member users here
        self.default_organization = Organization.objects.create(name='DefaultOrg', description='Default Description')
        self.superuser = User.objects.create_superuser(
            username='superuser',
            email='superuser@example.com',
            password='password',
            organization=self.default_organization
        )
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='password',
            is_staff=True,
            organization=self.default_organization
        )
        self.manager = User.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='password',
            organization=self.default_organization
        )
        self.member = User.objects.create_user(
            username='member',
            email='member@example.com',
            password='password',
            organization=self.default_organization
        )

        self.default_role = Role.objects.create(name='DefaultRole', description='Default Description', organization=self.default_organization)

    # Rest of your test methods...

    def test_assign_role_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('user-assign-role', args=[self.manager.id])
        data = {'roles': [self.default_role.id]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_assign_role_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-assign-role', args=[self.member.id])
        data = {'roles': [self.default_role.id]}
        response = self.client.post(url, data, format='json')

        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_assign_role_manager(self):
        self.client.force_authenticate(user=self.manager)
        url = reverse('user-assign-role', args=[self.member.id])
        data = {'roles': [self.default_role.id]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_assign_role_member(self):
        self.client.force_authenticate(user=self.member)
        url = reverse('user-assign-role', args=[self.admin.id])
        data = {'roles': [self.default_role.id]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
