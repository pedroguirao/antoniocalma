# -*- coding: utf-8 -*-

import requests
import base64
import json
import swagger_client
from swagger_client.rest import ApiException
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.osv import osv


class x_marketpayuser(models.Model):
    _inherit = 'res.partner'


    x_marketpayuser_id= fields.Char(string="Marketpay User")
    x_marketpaywallet_id = fields.Char(string="Marketpay Wallet")
    x_nombreprovincia_id = fields.Char(string="Código Región",related='state_id.name')
    x_codigopais_id = fields.Char(string="Código País",related='country_id.code')
    x_inversor = fields.Boolean(string="Es Inversor",default=False)
    x_dni_file = fields.Binary(string='Foto DNI')

    @api.multi
    def _get_wallet(self):
        # Variables definidas

        marketpay_key = "73a4d867-aeec-4e89-a295-64f14dc25ab9"
        marketpay_secret = "kFNm3CQU-ynHaM5g4OZ4MsSxOqmM85j4lgOVLkCgQYY="
        marketpay_domain = "https://api-sandbox.marketpay.io"

        # Configuración CLiente

        token_url = 'https://api-sandbox.marketpay.io/v2.01/oauth/token'
        key = 'Basic %s' % base64.b64encode(
            b'73a4d867-aeec-4e89-a295-64f14dc25ab9:kFNm3CQU-ynHaM5g4OZ4MsSxOqmM85j4lgOVLkCgQYY=').decode('ascii')
        data = {'grant_type': 'client_credentials'}
        headers = {'Authorization': key, 'Content-Type': 'application/x-www-form-urlencoded'}

        r = requests.post(token_url, data=data, headers=headers)

        rs = r.content.decode()
        response = json.loads(rs)
        token = response['access_token']

        # Configuración default de Swagger
        config = swagger_client.Configuration()
        config.host = marketpay_domain
        config.access_token = token
        client = swagger_client.ApiClient(configuration=config)
        api_instance = swagger_client.Configuration.set_default(config)
        apiUser = swagger_client.UsersApi()

        ############# Función Create User and Wallet #####################

        address = swagger_client.Address(address_line1=self.street, address_line2=self.street2,
                                         city=self.city, postal_code=self.zip,
                                         country=self.x_codigopais_id, region=self.x_nombreprovincia_id)

        user_natural = swagger_client.UserNaturalPost(address=address)
        user_natural.email = self.email
        user_natural.first_name = self.name
        user_natural.occupation = self.function
        user_natural.tag = self.comment
        user_natural.country_of_residence = self.x_codigopais_id
        user_natural.nationality = self.x_codigopais_id

        try:

            api_response = apiUser.users_post_natural(user_natural=user_natural)
            #self.x_marketpayuser_id'] = api_response.id
            self.x_marketpayuser_id = api_response.id

        except ApiException as e:
            print("Exception when calling UsersApi->users_post: %s\n" % e)

        ###########Create wallet for the user########################

        apiWallet = swagger_client.WalletsApi()
        ownersList = [api_response.id]
        wallet = swagger_client.WalletPost(owners=ownersList, description="wallet en EUR", currency='EUR')

        try:

            api_response = apiWallet.wallets_post(wallet=wallet)
            #self.x_marketpaywallet_id'] = api_response.id
            self.x_marketpaywallet_id=api_response.id
            self.x_inversor = True


        except ApiException as e:
            print("Exception when calling WalletApi->Wallet_post: %s\n" % e)


    @api.multi
    def marketpay_validate(self):
        #self. super(x_marketpayuser, self).create(values)



            if self.country_id == False:
                raise osv.except_osv(('x_codigopais_id'),
                                     ('El campo pais es obligatorio'))
            if self.state_id == False:
                raise osv.except_osv(('x_nombreprovincia_id'),
                                     ('El campo provincia es obligatorio'))


            if self.email == False:
                raise osv.except_osv(('email'),
                                     ('El campo mail es obligatorio'))
            if self.city == False:
                raise osv.except_osv(('city'),
                                     ('El campo ciudad es obligatorio'))
            if self.street == False:
                raise osv.except_osv(('street'),
                                     ('El campo calle es obligatorio'))
            if self.zip == False:
                raise osv.except_osv(('zip'),
                                     ('El campo C.P es obligatorio'))

            self._get_wallet()

            #print(marketpay)







    @api.onchange('name','email')
    def updateuser(self):
        if self.name != False:
            if self.x_marketpayuser_id != False:
                # Variables definidas

                marketpay_key = "73a4d867-aeec-4e89-a295-64f14dc25ab9"
                marketpay_secret = "kFNm3CQU-ynHaM5g4OZ4MsSxOqmM85j4lgOVLkCgQYY="
                marketpay_domain = "https://api-sandbox.marketpay.io"

                # Configuración CLiente

                token_url = 'https://api-sandbox.marketpay.io/v2.01/oauth/token'
                key = 'Basic %s' % base64.b64encode(
                    b'73a4d867-aeec-4e89-a295-64f14dc25ab9:kFNm3CQU-ynHaM5g4OZ4MsSxOqmM85j4lgOVLkCgQYY=').decode('ascii')
                data = {'grant_type': 'client_credentials'}
                headers = {'Authorization': key, 'Content-Type': 'application/x-www-form-urlencoded'}

                r = requests.post(token_url, data=data, headers=headers)

                rs = r.content.decode()
                response = json.loads(rs)
                token = response['access_token']

                # Configuración default de Swagger
                config = swagger_client.Configuration()
                config.host = marketpay_domain
                config.access_token = token
                client = swagger_client.ApiClient(configuration=config)
                api_instance = swagger_client.Configuration.set_default(config)
                

                
                apiUser = swagger_client.UsersApi()
                print(self.x_codigopais_id)
                address = swagger_client.Address(address_line1=self.street, address_line2=self.street2, city=self.city, postal_code=self.zip,
                                             country=self.x_codigopais_id, region=self.x_nombreprovincia_id)

                user_id = self.x_marketpayuser_id
                user_natural = swagger_client.UserNaturalPut(address=address)
                user_natural.email = self.email
                user_natural.first_name = self.name
                user_natural.occupation = self.function
                user_natural.tag = self.comment
                user_natural.country_of_residence = self.x_codigopais_id
                user_natural.nationality = self.x_codigopais_id

                try:

                    api_response = apiUser.users_put_natural(user_id, user_natural=user_natural)

                except ApiException as e:
                    print("Exception when calling UsersApi->users_put: %s\n" % e)