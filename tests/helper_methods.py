from flask import current_app

def user_registration(self, data):
        """User registration"""
        return self.client.post(
                'api/v1/register',
                data=data,
                content_type='application/json')

def user_login(self, data):
        """User registration"""
        return self.client.post(
                'api/v1/login',
                data=data,
                content_type='application/json')

def user_logout(self, token):
        return self.client.post(
                'api/v1/logout',
                content_type='application/json', 
                headers=dict(Authorization="Bearer " + token))

def create_product(self, data, token):
        return self.client.post(
                '/api/v1/products',
                data=data,
                content_type='application/json', 
                headers=dict(Authorization="Bearer " + token))

def get_all_products(self, token):
        return self.client.get(
                '/api/v1/products',
                content_type='application/json', 
                headers=dict(Authorization="Bearer " + token))

def get_specific_product(self, token):
        return self.client.get(
                '/api/v1/products/1',
                content_type='application/json', 
                headers=dict(Authorization="Bearer " + token))

def get_non_existing_product(self, token):
        return self.client.get(
                '/api/v1/products/100',
                content_type='application/json', 
                headers=dict(Authorization="Bearer " + token))

def product_update(self, data, token):
        return self.client.put(
                '/api/v1/products/1',
                data=data,
                content_type='application/json', 
                headers=dict(Authorization="Bearer " + token))

def make_sale(self, data, token):
        return self.client.post(
                '/api/v1/sales',
                data=data,
                content_type='application/json', 
                headers=dict(Authorization="Bearer " + token))

def get_all_sales(self, token):
        return self.client.get(
                '/api/v1/sales',
                content_type='application/json', 
                headers=dict(Authorization="Bearer " + token))

def get_specific_sale(self, token):
        return self.client.get(
                '/api/v1/sales/1',
                content_type='application/json', 
                headers=dict(Authorization="Bearer " + token))

def delete_specific_product(self, token):
        return self.client.delete(
                '/api/v1/products/1',
                content_type='application/json',
                headers=dict(Authorization="Bearer " + token))