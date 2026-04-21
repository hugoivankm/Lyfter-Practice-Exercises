SET search_path TO transactions;

DO $$
DECLARE
    -- Input parameters
    p_cart_id CONSTANT INTEGER := 1;
    p_app_user_id CONSTANT INTEGER := 1;
    p_payment_method_id CONSTANT INTEGER := 2;
    p_current_invoice_sequence CONSTANT INTEGER := 2026001;

    -- Variables for processing
    v_item RECORD;
    v_db_user_id INTEGER;
    v_new_invoice_id INTEGER;
    v_total_amount DECIMAL(10, 2) := 0;

BEGIN
    -- Validate that the user exists
    SELECT id INTO v_db_user_id FROM Users WHERE id = p_app_user_id LIMIT 1; 

    IF v_db_user_id IS NULL THEN
        RAISE EXCEPTION 'ERROR: User with id % does not match any known user.', p_app_user_id;
    END IF;

    -- Calculate the total for the cart
    SELECT SUM(p.current_price * cp.quantity)
    INTO v_total_amount
    FROM Products p
    JOIN Cart_Products cp ON p.id = cp.products_id
    WHERE cp.cart_id = p_cart_id
    FOR UPDATE OF p;

    -- Guard against invalid totals
    IF v_total_amount IS NULL OR v_total_amount <= 0 THEN
        RAISE EXCEPTION 'ERROR: Cannot process an empty cart.';
    END IF;

    -- Insert the invoice
    INSERT INTO Invoices (invoice_number, total, payment_methods_id, users_id) 
    VALUES (p_current_invoice_sequence + 1, v_total_amount, p_payment_method_id, p_app_user_id)
    RETURNING id INTO v_new_invoice_id;
    
    -- Loop through cart items to create details and update stock
    FOR v_item IN 
        SELECT cp.products_id, cp.quantity, p.stock_quantity, p.current_price, p.name
        FROM Cart_Products cp
        JOIN Products p ON cp.products_id = p.id
        WHERE cp.cart_id = p_cart_id;
    LOOP
        -- Check if there is enough stock of the product
        IF v_item.quantity > v_item.stock_quantity THEN
            RAISE EXCEPTION 'ERROR: Product % is out of stock. Requested %, Available %',
            v_item.name, v_item.quantity, v_item.stock_quantity;
        END IF;

        -- Add details for the invoice that was generated
        INSERT INTO Details (price_at_sale, quantity, invoices_id, products_id) VALUES 
        (v_item.current_price, v_item.quantity, v_new_invoice_id, v_item.products_id );

        -- Reduce the stock of the product by the quatity of the order.
        UPDATE Products
        SET stock_quantity = stock_quantity - v_item.quantity
        WHERE Products.id = v_item.products_id;

    END LOOP;

    -- clean up cart products
    DELETE FROM Cart_Products WHERE cart_id = p_cart_id;

    RAISE NOTICE 'Purchase completed successfully. Invoice ID: %', v_new_invoice_id;
 
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'An error occurred: %', SQLERRM;
END $$;