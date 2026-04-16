SET search_path TO transactions;

DO $$
DECLARE
    -- Input parameters
    p_current_invoice_sequence CONSTANT INTEGER := 2026002;
    p_product_id CONSTANT INTEGER := 1;
    
    -- Variables for processing
    v_item RECORD;
    v_invoice_ref RECORD;
    v_new_credit_id INTEGER;
    v_invoice_id INTEGER;

BEGIN
    -- Verify invoice exists in the DB.
    SELECT id, invoice_number, users_id, payment_methods_id 
    INTO v_invoice_ref
    FROM Invoices i
    WHERE i.invoice_number = p_current_invoice_sequence;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Error: invoice number: % does not match any known invoice', 
        p_current_invoice_sequence;
    END IF;
    
    -- Increase the stock of the product in the amount registered in the purchase.
    SELECT d.products_id, d.price_at_sale, d.quantity
    INTO v_item
    FROM Details d
    JOIN Invoices i ON i.id = d.invoices_id  
    WHERE d.products_id = p_product_id
    AND i.id = v_invoice_ref.id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Error: Product with id % not found in specified invoice', p_product_id;
    END IF;

    -- Restore inventory 
    UPDATE Products p
    SET stock_quantity = stock_quantity + v_item.quantity
    WHERE p.id = p_product_id;
    
    -- Modify the original invoice and mark it as "RETURNED".
    UPDATE Invoices i
    SET status = 'RETURNED'
    WHERE i.id = v_invoice_ref.id;

    -- Emit a credit note for the article
    INSERT INTO Invoices (type, invoice_number, total, payment_methods_id, users_id) 
    VALUES (
        'CREDIT',
         p_current_invoice_sequence + 1,
         -1 * v_item.quantity * v_item.price_at_sale,
         v_invoice_ref.payment_methods_id, v_invoice_ref.users_id
    )
    RETURNING id INTO v_new_credit_id;

    INSERT INTO Details (price_at_sale, quantity, invoices_id, products_id) 
    VALUES (
        v_item.price_at_sale,
        v_item.quantity,
        v_new_credit_id,
        v_item.products_id
    );

    RAISE NOTICE 'Product return completed successfully.';
 
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'An error occurred: %', SQLERRM;
END $$;
