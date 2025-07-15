from monitor import logging as log, static
from category import product, order, ship, payment, sex, members
from processed import processed
from datetime import datetime 

class DataValidator(metaclass=static):

    def validate_product():
        """Validates product type"""
        products = processed.data()
        products = products['product_type']
        products = products.compute()
        valid = product.standard_product
        invalid = products[~products.isin(valid)]

        try:
            log.info("🔄 Validating product types...")
            if not invalid.empty:
                log.info("Invalid product types found")
                log.info(invalid)
            else:
                log.info("✅ Product types are valid")
        except Exception as e:  
            log.error(f"❌ Error validating product types: {e}")
            return None

    def validate_sku():
        """Validates skus"""
        sku = processed.data()
        sku = sku['sku']
        sku = sku.compute()
        valid = product.standard_sku
        invalid = sku[~sku.isin(valid)]

        try:
            log.info("🔄 Validating SKUs...")
            if not invalid.empty:
                log.info("Invalid SKUs found")
                log.info(invalid)
            else:
                log.info("✅ SKUs are valid")
        except Exception as e:
            log.error(f"❌ Error validating SKUs: {e}")
            return None
    
    def validate_order_status():
        """Validates order status"""
        order_status = processed.data()
        order_status = order_status['order_status']
        order_status = order_status.compute()
        valid = order.status
        invalid = order_status[~order_status.isin(valid)]

        try:
            log.info("🔄 Validating order status data...")
            if not invalid.empty:
                log.info("Invalid order status found")
                log.info(invalid)
            else:
                log.info("✅ Order statuses are valid")
        except Exception as e:
            log.error(f"❌ Error validating order status: {e}")
            return None
    
    def validate_shipping():
        """Validates shipping type"""
        shipping_type = processed.data()
        shipping_type = shipping_type['shipping_type']
        shipping_type = shipping_type.compute()
        valid = ship.standard_shipping
        invalid = shipping_type[~shipping_type.isin(valid)]

        try:
            log.info("🔄 Validating shipping types...")
            if not invalid.empty:
                log.info("Invalid shipping types found")
                log.info(invalid)
            else:
                log.info("✅ Shipping types are valid")
        except Exception as e:
            log.error(f"❌ Error validating shipping types: {e}")
            return None
        
    def validate_payment():
        """Validates payment method"""
        payment_method = processed.data()
        payment_method = payment_method['payment_method']
        payment_method = payment_method.compute()
        valid = payment.method
        invalid = payment_method[~payment_method.isin(valid)]

        try:
            log.info("🔄 Validating payment methods...")
            if not invalid.empty:
                log.info("Invalid payment methods found")
                log.info(invalid)
            else:
                log.info("✅ Payment methods are valid")
        except Exception as e:
            log.error(f"❌ Error validating payment methods: {e}")
            return None
        
    def validate_gender():
        """Validates gender category"""
        gender = processed.data()
        gender = gender['gender']
        gender = gender.compute()
        valid = sex.gender_category
        invalid = gender[~gender.isin(valid)]

        try:
            log.info("🔄 Validating gender category...")
            if not invalid.empty:
                log.info("Invalid gender category found")
                log.info(invalid)
            else:
                log.info("✅ Gender categories are valid")
        except Exception as e:
            log.error(f"❌ Error validating gender categories: {e}")
            return None
        
    def validate_membership():
        """Validates memmbership category"""
        membership = processed.data()
        membership = membership['loyalty_member']
        membership = membership.compute()
        valid =  members.membership_class
        invalid = membership[~membership.isin(valid)]

        try:
            log.info("🔄 Validating membership category...")
            if not invalid.empty:
                log.info("Invalid membership catgories found")
                log.info(invalid)
            else:
                log.info("✅ Membership categories are valid")
        except Exception as e:
            log.error(f"❌ Error validating membership categories: {e}")
            return None
        
    def validate_addontotal():
        """Validates add-on_total"""
        add_on_total = processed.data()
        add_on_total = add_on_total['add-on_total']
        add_on_total = add_on_total.compute()   
        valid = r"^\d+(\.\d+)?$"
        valid = add_on_total.str.match(valid)
        invalid = add_on_total[~valid]

        try:
            log.info("🔄 Validating add-on_totals...")
            if not invalid.empty:
                log.info("Invalid values found")
                log.info(invalid)
            else:
                log.info("✅ Add-on_totals are valid")
        except Exception as e:
            log.error(f"❌ Error validating values: {e}")
            return None
    
    def validate_age():
        """Validates age values"""
        age = processed.data()
        age = age['age']
        age = age.compute()
        valid = r"^\d+$"
        valid = age.str.match(valid)
        invalid = age[~valid]

        try:
            log.info("🔄 Validating age values...")
            if not invalid.empty:
                log.info("Invalid age values found")
                log.info(invalid)
            else:
                log.info("✅ Age values are valid")
        except Exception as e:
            log.error(f"❌ Error validating age values: {e}")
            return None
    
    def validate_id():
        """Validates customer id values"""
        id = processed.data()
        id = id['customer_id']
        id = id.compute()
        valid_format = id.str.match(r"^\d+$") 
        valid_numeric = id[valid_format].astype(int)
        valid_range = valid_numeric >= 1000
        invalid = id[~valid_format | ~valid_range]

        try:
            log.info("🔄 Validating customer ids...")
            if not invalid.empty:
                log.info("Invalid customer ids found")
                log.info(invalid)
            else:
                log.info("✅ Customer ids are valid")
        except Exception as e:
            log.error(f"❌ Error validating customer ids: {e}")
            return None
    
    def validate_date():
        """Validates date values values"""
        date = processed.data()
        date = date['purchase_date']
        date = date.compute()
        valid_format = date.str.match(r"^\d{4}-\d{2}-\d{2}$") 
        valid_date = date[valid_format].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
        valid_range = valid_date >= datetime(2023, 1, 1)
        invalid = date[~valid_format | ~valid_range]

        try:
            log.info("🔄 Validating date values...")
            if not invalid.empty:
                log.info("Invalid date values found")
                log.info(invalid)
            else:
                log.info("✅ Date values are valid")
        except Exception as e:
            log.error(f"❌ Error validating dating values: {e}")
            return None
    
    def validate_rating():
        """Validates rating values"""
        rating = processed.data()
        rating = rating['rating']
        rating = rating.compute()
        valid_format = rating.str.match(r"^\d+$")  
        valid_rating = rating[valid_format].astype(int)
        valid_range = (valid_rating >= 1) & (valid_rating <= 5)
        invalid = rating[~valid_format | ~valid_range]

        try:
            log.info("🔄 Validating rating values...")
            if not invalid.empty:
                log.info("Invalid rating values found")
                log.info(invalid)
            else:
                log.info("✅ Rating values are valid")
        except Exception as e:
            log.error(f"❌ Error validating rating values: {e}")
            return None
    
    def validate_totalprice():
        """Validates total price values"""
        total_price = processed.data()
        total_price = total_price['total_price']
        total_price = total_price.compute()
        valid = r"^\d+(\.\d+)?$"
        valid = total_price.str.match(valid)
        invalid = total_price[~valid]

        try:
            log.info("🔄 Validating total price values...")
            if not invalid.empty:
                log.info("Invalid total price values found")
                log.info(invalid)
            else:
                log.info("✅ Total price values are valid")
        except Exception as e:
            log.error(f"❌ Error validating values: {e}")
            return None
    
    def validate_unitprice():
        """Validates unit price values"""
        unit_price = processed.data()
        unit_price = unit_price['unit_price']
        unit_price = unit_price.compute()
        valid = r"^\d+(\.\d+)?$"
        valid = unit_price.str.match(valid)
        invalid = unit_price[~valid]

        try:
            log.info("🔄 Validating unit price values...")
            if not invalid.empty:
                log.info("Invalid unit price values found")
                log.info(invalid)
            else:
                log.info("✅ Unit price values are valid")
        except Exception as e:
            log.error(f"❌ Error validating values: {e}")
            return None
