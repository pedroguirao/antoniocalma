odoo.define('website_wallet.wallet', function (require) {
"use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');

    $(document).ready(function() {
        $('input.add_amount').on('input.add_amount', function() {
            this.value = this.value.replace(/[^0-9.]/g, '').replace(/(\..*)\./g, '$1');
        });

        $('.oe_sale_acquirer_button').each(function() {
            if ($(this).find('input[name=data_set]')) {
                var url = $(this).find('input[name=data_set]').attr('data-action-url');
                $(this).find('form').attr('action', url);
            }
        });

        $('input[type=radio][name=payment_acquirer]').change(function() {
            var value = this.value;
            if (this.value == 'stored_card'){
                $('#acquirers_list .oe_sale_acquirer_button').addClass('d-none');
                $('#acquirers_list #stored_card').removeClass('d-none');
                $('#acquirers_list #stored_card').find('input[name=stored_card_id]').val($(this).attr('data-store_card_id'));
            } else {
                $('#acquirers_list .oe_sale_acquirer_button').addClass('d-none');
                $('#acquirers_list > div[data-id=' + this.value + ']').removeClass('d-none');
            }
        });

        $('#add_amount').on('input',function(e){
            var amount = $(this).val();
            $('#acquirers_list').find('input[name=amount]').val(amount);
            $('#acquirers_list').find('input[name=vpc_Amount]').val(amount); 
            if (amount) {
                $('#acquirers_list input[name=submit]').removeClass('d-none');
            } else {
                $('#acquirers_list input[name=submit]').addClass('d-none');
            }
        });

        $('#acquirers_list').on("click", 'input.external[name="submit"]', function (ev) {
            // ev.preventDefault();
            // ev.stopPropagation();
            var $form = $(ev.currentTarget).parents('form');

            // Check paypal then set return url
            if ($form.hasClass('paypal')) {
                $form.find('input[name=return]').val('/wallet/payment/validate');
                $form.find('input[name=item_name]').val('Add into Wallet');
                var obj = $form.find('input[name=custom]').val()
                var return_url = jQuery.parseJSON(obj).return_url;
                $form.find('input[name=return]').val(return_url);
            }

            // Create Transaction using acquirer id and amount
            var acquirer_id = $(ev.currentTarget).parents('div.oe_sale_acquirer_button').first().data('id');
            if (! acquirer_id) {
                return false;
            }
            var amount = $(ev.currentTarget).parents('form').find('input[name=amount]').val();
            if (! amount) {
                var amount = $(ev.currentTarget).parents('form').find('input[name=vpc_Amount]').val();
                if (! amount)
                    return false;
            }
            ajax.jsonRpc('/wallet/payment/transaction', 'call',
                         {'acquirer_id': acquirer_id, 'amount': amount}).then(function (data) {
                if (data){ 
                    if ($form.hasClass('paypal')) {
                        $form.find('input[name=item_number]').val(data.tx_reference);
                    }
                    $form.submit();
                }
                else {
                    return false;
                }
            });
        });

    });

});
